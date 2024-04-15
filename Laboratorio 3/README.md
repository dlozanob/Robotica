# Laboratorio 3

## Integrantes:

- Oscar Julian Olivos Aguirre
- Daniel Lozano Barrero

## Introducción


## Implementación de ROS con Matlab

[Livescript de Matlab](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%203/Programas/lab3.mlx)

Paquete requerido:
- ROS Toolbox

### Primera parte

Creación de un tópico `turtle1/cmd_vel` de tipo `turtlesim/Pos` en el nodo principal.
Se crea un mensaje y se modifican sus parámetros, se envía el mensaje por medio del tópico creado anteriormente.

>[!Note]
>El nodo _turtlesim_ ya está suscrito por defecto al tópico `turtle1_cmd_vel`

>[!Note]
>El nodo principal iniciado por `rosint` para el toolbox de Matlab es `matlab_global_node_47801`

_Procedimiento:_
1. Se inicializa el nodo maestro: `rosinit`
2. Creación del tópico: `velPub = rospublisher('/turtle1/cmd_vel', 'geometry_msgs/Twist');`
3. Creación del mensaje: `velMsg = rosmessage(velPub);`
4. Se modifica uno de los parámetros del mensaje: `velMsg.Linear.X = 1;`
5. Se envía el mensaje por medio del tópico creado: `send(velPub,velMsg);`

---

Se puede verificar la creación del tópico mediante: `rosnode info matlabglobal_node_47801` :

![](Imagenes/Pasted%20image%2020240414172515.png)

El tipo de mensaje asignado posee los siguientes parámetros:

![](Imagenes/Pasted%20image%2020240414172917.png)

Por tanto, los otros parámetros también pudieron haber sido modificados en caso de necesitarlo.

Ahora bien, este es un mensaje que modifica la velocidad de la tortuga con el nodo `turtlesim`, el cual modifica la cinemática de la tortuga en la GUI provista por el paquete `hello_turtle`.
Por tanto, el nodo debe estar suscrito al tópico `turtle1/cmd_vel` para poder recibir el mensaje. No obstante, ya lo está.

![](Imagenes/Pasted%20image%2020240414173318.png)

El mensaje es recibido correctamente y se puede observar en la GUI el movimiento de la tortuga.

![](Imagenes/Pasted%20image%2020240414173405.png)

### Segunda parte

Suscripción del nodo global al tópico `turtle1/pos` publicado por el nodo `turtlesim` y obtener el último mensaje emitido por este tópico.

_Procedimiento:_
1. Suscribir el nodo global al tópico: `posSus = rossubscriber('/turtle1/pose');`
2. Se genera una variable que contiene el último mensaje emitido por este tópico: `LM = posSus.LatestMessage;`

### Tercera parte

Se quiere modificar la pose de la tortuga desde el nodo global. Se puede utilizar el servicio `turtle1/teleport_absolute` emitido por el nodo `turtlesim`, el cual permite establecer las coordenadas absolutas de la tortuga dentro de la ventana gráfica.

_Procedimiento:_
1. Se crea un cliente a este servicio en el nodo global: `turtle_client = rossvcclient('/turtle1/teleport_absolute');`
2. Se genera un mensaje por el lado del cliente: `request_msg = rosmessage(turtle_client);` 
3. Se modifican los argumentos que contiene el mensaje:
``` Matlab
request_msg.X = 5;
request_msg.Y = 5;
request_msg.Theta = 45;
```
4. Breve Visualización del mensaje enviado: `request_msg.showdetails;`

![](Imagenes/Pasted%20image%2020240414174908.png)

5. Emitir el mensaje por el canal del cliente del servicio utilizado: `response = call(turtle_client, request_msg, 'Timeout', 3);`

---

>[!Note]
>El tipo de mensaje (argumentos que contiene) se define al vincularlo con el cliente, el cual utiliza un servicio que contiene mensajes de cierto tipo determinado

>[!Note]
>El parámetro `'Timeout'` en la función `call()` determina el número de segundos que espera el proceso a la confirmación del envío del mensaje. Si este parámetro es $-1$, el proceso esperará hasta que el nodo se desactive ([ROS Services](https://docs.ros.org/en/diamondback/api/roscpp/html/namespaceros_1_1service.html))

De este modo se verifican los argumentos del mensaje:

![](Imagenes/Pasted%20image%2020240414174649.png)

### Parte cuatro

Apagar el nodo principal.

_Procedimiento:_
1. Apagar el nodo principal: `rosshutdown`

>[!Note]
>El nodo global `matlab_global_node_47801` se desactiva


## Implementación de ROS con Python

Software requerido:
- Python 3.8.10
- rospy
- numpy

_Objetivo:_ Modificar la pose de la tortuga con el teclado.

La configuración de las teclas es la siguiente:
- `W` : Mover tortuga hacia adelante
- `A` : Mover tortuga hacia su izquierda
- `S` : Mover tortuga hacia atrás
- `D` : Mover tortuga hacia su derecha
- `R` : Retornar tortuga a su pose incial por defeto
- `SPACE` : Rotar la tortuga $180°$

Adicionalmente se implementaron las siguientes funciones:
- `Q` : Girar tortuga en sentido antihorario
- `E` : Girar tortuga en sentido horario
- `M` : Aumentar la velocidad de la tortuga
- `N` : Reducir la velocidad de la tortuga
- `Z` : Terminar el proceso

---

### Reconocimiento de eventos

El programa se ejecuta en un bucle donde las primeras tareas es el reconocimiento de los eventos de teclado. La tecla presionada determina la función a ejecutar.

El reconocimiento de eventos se realiza mediante la función:

```Python
def getKey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    c = str(c)[2]
    return c
```

La cual utiliza la librería `sys` que viene por defecto en la versión de _Python_ instalada. Esta librería de bajo nivel permite reconocer los eventos de teclado, en la función se traducen estos eventos a un caracter.

### Actualización de Pose

Tras reconocer la tecla presionada, se actualiza la pose de la tortuga de acuerdo a la función correspondiente.

```Python
def updateState(x, y, th, status):
    vel_msg.linear.x = x
    vel_msg.linear.y = y
    vel_msg.angular.z = th
    vel_pub.publish(vel_msg)
    if(status == 1):
        tp_abs(initPose[0], initPose[1], 0)
    elif(status == -1):
        tp_rel(0, np.pi)
```

>[!Note]
>La variable `status` determina el uso de los servicios `tp_abs` y `tp_rel` los cuales son utilizados para reiniciar pose de la tortuga y rotarla $180°$ respectivamente


### Comunicación con ROS

1. _Python_ debe poseer un nodo propio que le permita recibir y emitir datos a los otros nodos. Se inicializa el nodo que cumple con este propósito: `rospy.init_node('jog_node')`

2. Se crea una publicación al tópico `turtle1/cmd_vel` encargado de modificar la velocidad de la tortuga por un periodo corto de tiempo: `vel_pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)`

3. Se genera un mensaje de tipo `geometry_msgs/Twist` : `vel_msg = Twist()`

4. Se genera un cliente para el servicio `turtle1/teleport_absolute` : `tp_abs = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)`

5. Se genera un cliente para el servicio `turtle1/teleport_relative` : `tp_rel = rospy.ServiceProxy('turtle1/teleport_relative', TeleportRelative)`

Por medio del publicador generado se emiten los mensajes que llegan al nodo `turtlesim` el cual al recibir esta información modifica la velocidad de la tortuga con los argumentos: `X`, `Y`, `Theta`. Esto genera el movimiento deseado de la tortuga.

>[!Note]
>Percatarse que el envío de mensajes por el tópico `turle1/cmd_vel` fue implementado también en Matlab ([Procedimiento en Matlab](#Primera+parte))

Los servicios `teleport_absolute` y `teleport_relative` hacen posible modificar la pose de la tortuga de manera global y relativa respectivamente. De esta manera pueden implementarse las funciones asignadas para las teclas: `R` y `SPACE`.

>[!Note]
>La tortuga posee su propio sistema de coordenadas. El tópico `turtle1/vel` modifica la velocidad de la tortuga en su propio sistema de referencia

>[!Note]
>Al cambiar el sentido de la tortuga con la tecla `SPACE`, es necesario cambiar el sentido de la velocidad para que las teclas de movimiento satisfagan su función como se describió en: [Configuración de las teclas](#Implementación+de+ROS+con+Python)

### Funciones adicionales

Al detectar las teclas: `Q` o `E`, la tortuga rota en sentido antihorario u horario respectivamente. Por lo que se modifica el argumento `Theta` que se envía por el tópico `turtle1/cmd_vel`.

>[!Note]
>Rotar la tortuga $180°$ usando estas funciones no hará que su frente sea el mismo por el que se desplaza hacia adelante. Esto no se implementó

Las teclas `M` y `N` aumentan y reducen la velocidad de la tortuga respectivamente, al modificar la variable de velocidad `vf` que comienza siendo $1$.
- Límite de velocidad mínimo: $\mid1\mid$
- Límite de velocidad máximo: $\mid50\mid$

>[!Note]
>Se usó una aceleración de $2$

Para más información sobre el algoritmo: [Código](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%203/Programas/myTeleopKey.py)


