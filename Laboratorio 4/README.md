# Laboratorio 4

## Integrantes:

- Oscar Julian Olivos Aguirre
- Daniel Lozano Barrero

## Introducción
Habiendo realizado el acercamiento a las herramientas de ROS en Linux, su integración con Python y la ejecución de instrucciones utilizando Matlab y TurtleSim en la práctica anterior, se dispone aplicar estos conocimientos para permitir manipular y programar cinco posiciones deferentes de un robot Phantom X Pincher, junto con una interfaz de usuario que permita seleccionar la pose deseada y visibilizar la posición actual del robot mediante el uso del Robotic Toolbox de Peter Corke. 

Este laboratorio se desarrolló en una configuración de Linux nativa corriendo mediante Ubuntu y utilizando herramientas adicionales tales como Catkin, el software Dynamixel y Visual Studio Code.

## Mediciones y cinemática directa
### Mediciones
### Cinemática directa

Se desarrolló la cinemática directa del robot, teniendo en cuanta el siguiente diagrama:

![](Imagenes/esquemarobot.png)

En donde luego de medir sus eslabones y realizar el análisis cinemático, se pudo obtener la siguiente matriz de transformación homogénea que describe la posición del efector final respecto a su base:

![](Imagenes/MTH.png)

Posteriormente se encontraron los parámetros que describen la cinemática directa del motor, siendo estos:

![](Imagenes/parametros.png)

Estos parámetros fueron utilizados para configurar los eslabones y la cadena al graficar la simulación del robot en Matlab usando el toolbox de Peter Corke.


## Manipulación cíclica del Robot

Suscripción del nodo global al tópico `turtle1/pos` publicado por el nodo `turtlesim` y obtener el último mensaje emitido por este tópico.

_Procedimiento:_
1. Suscribir el nodo global al tópico: `posSus = rossubscriber('/turtle1/pose');`
2. Se genera una variable que contiene el último mensaje emitido por este tópico: `LM = posSus.LatestMessage;`

## Configuración en las cinco poses deseadas

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

### Interfaz de usuario en Matlab

Apagar el nodo principal.

_Procedimiento:_
1. Apagar el nodo principal: `rosshutdown`

>[!Note]
>El nodo global `matlab_global_node_47801` se desactiva


### Comunicación Matlab-Python

[Código](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%203/Programas/myTeleopKey.py)

[Video de su implementación](https://youtu.be/MVhyVaZZ8w4)

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

### Comunicación Python-Ros

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




Para más información sobre el algoritmo: [Código](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%203/Programas/myTeleopKey.py)
