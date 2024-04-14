# Laboratorio 3

## Integrantes:

- Oscar Julian Olivos Aguirre
- Daniel Lozano Barrero

## Introducción


## Implementación de ROS con Matlab

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

![[Pasted image 20240414172515.png]]

El tipo de mensaje asignado posee los siguientes parámetros:

![[Pasted image 20240414172917.png]]

Por tanto, los otros parámetros también pudieron haber sido modificados en caso de necesitarlo.

Ahora bien, este es un mensaje que modifica la velocidad de la tortuga con el nodo `turtlesim`, el cual modifica la cinemática de la tortuga en la GUI provista por el paquete `hello_turtle`.
Por tanto, el nodo debe estar suscrito al tópico `turtle1/cmd_vel` para poder recibir el mensaje. No obstante, ya lo está.

![[Pasted image 20240414173318.png]]

El mensaje es recibido correctamente y se puede observar en la GUI el movimiento de la tortuga.

![[Pasted image 20240414173405.png]]

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

![[Pasted image 20240414174908.png]]

5. Emitir el mensaje por el canal del cliente del servicio utilizado: `response = call(turtle_client, request_msg, 'Timeout', 3);`

---

>[!Note]
>El tipo de mensaje (argumentos que contiene) se define al vincularlo con el cliente, el cual utiliza un servicio que contiene mensajes de cierto tipo determinado

>[!Note]
>El parámetro `'Timeout'` en la función `call()` determina el número de segundos que espera el proceso a la confirmación del envío del mensaje. Si este parámetro es $-1$, el proceso esperará hasta que el nodo se desactive ([ROS Services](https://docs.ros.org/en/diamondback/api/roscpp/html/namespaceros_1_1service.html))

De este modo se verifican los argumentos del mensaje:

![[Pasted image 20240414174649.png]]

### Parte cuatro

Apagar el nodo principal.

_Procedimiento:_
1. Apagar el nodo principal: `rosshutdown`

>[!Note]
>El nodo global `matlab_global_node_47801` se desactiva


## Implementación de ROS con Python


