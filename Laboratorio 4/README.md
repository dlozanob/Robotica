# Laboratorio 4

## Integrantes:

- Oscar Julian Olivos Aguirre
- Daniel Lozano Barrero

Implementación: [Video](https://youtu.be/pJycmdnFGBk)

## Introducción
Habiendo realizado el acercamiento a las herramientas de ROS en Linux, su integración con Python y la ejecución de instrucciones utilizando Matlab y TurtleSim en la práctica anterior, se dispone aplicar estos conocimientos para permitir manipular y programar cinco posiciones deferentes de un robot Phantom X Pincher, junto con una interfaz de usuario que permita seleccionar la pose deseada y visibilizar la posición actual del robot mediante el uso del Robotic Toolbox de Peter Corke. 

Este laboratorio se desarrolló en una configuración de Linux nativa corriendo mediante Ubuntu y utilizando herramientas adicionales tales como Catkin, el software Dynamixel y Visual Studio Code.

## Mediciones y cinemática directa
### Mediciones

Se hizo el respectivo levantamiento metrológico de los eslabones del robot, teniendo en cuenta que la longitud de cada eslabón es la mínima distancia entre articulaciones. 

Las medidas obtenidas son:

- $L_1 = 14.1$ cm
- $L_2 = 10.5$ cm
- $L_3 = 10.55$ cm
- $L_4 = 9.1$ cm

La última longitud es la longitud desde la articulación 4 hasta la mitad del _gripper_, que es donde se encuentra el origen del _TCP_.

![image](https://github.com/dlozanob/Robotica/assets/69172002/e489ed52-3a74-427a-81b0-011714083f32)

### Cinemática directa

Se desarrolló la cinemática directa del robot, teniendo en cuanta el siguiente diagrama:

![](Imagenes/esquemarobot.png)

![image](https://github.com/dlozanob/Robotica/assets/69172002/04192852-a26f-4b9d-99cb-ca755750e081)

En donde luego de medir sus eslabones y realizar el análisis cinemático, se pudo obtener la siguiente matriz de transformación homogénea que describe la posición del efector final respecto a su base:

![](Imagenes/MTH.png)

Posteriormente se encontraron los parámetros que describen la cinemática directa del motor, siendo estos:

![](Imagenes/parametros.png)

![image](https://github.com/dlozanob/Robotica/assets/69172002/7801efc4-d633-48eb-86d3-9b0465192094)

Estos parámetros fueron utilizados para configurar los eslabones y la cadena al graficar la simulación del robot en Matlab usando el toolbox de Peter Corke.


## Implementación básica entre dos poses

### Usando tópicos

Se utiliza un script de Python, el cual utiliza el tópico `/joint_trajectory`.

El nodo `/dynamixel_workbench`se encuentra suscrito a este. 

![image](https://github.com/dlozanob/Robotica/assets/69172002/f8af987c-ba48-495d-8145-b2ceb03be80f)

Por tanto, se crea en python un nodo publicador que envía la información al tópico. Mientras que `/dynamixel_workbench` se encarga de enviar publicar estos datos a `/rosout`, el cual haciendo uso del paquete de dynamixel, hace que los motores se muevan de acuerdo a los datos enviados.


A continuación, se crea el nodo publicador, el cual publica al tópico anteriormente mencionado.

```python
pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size = 0)
rospy.init_node('joint_publisher', anonymous = False)
```

Notar que el argumento `JointTrajectory` es el tipo de mensaje que posee el tópico.

![image](https://github.com/dlozanob/Robotica/assets/69172002/684cfbda-4d84-4dc1-a8d0-bfd35bff6f21)

Este tipo de mensaje posee los siguientes campos:

![image](https://github.com/dlozanob/Robotica/assets/69172002/9f680ac9-d16a-4f21-be90-ce95886b7cfd)

El campo `positions` es donde se asignan los valores de las articulaciones.


La siguiente función envía los datos al tópico:

```python
def publish_msg(q1, q2, q3, q4, q5):
    state = JointTrajectory()
    state.header.stamp = rospy.Time.now()
    state.joint_names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5"]
    point = JointTrajectoryPoint()
    point.positions = [q1, q2, q3, q4, q5]
    point.time_from_start = rospy.Duration(0.5)
    state.points.append(point)
    pub.publish(state)
    print('State published successfully')
```


### Usando servicios

Suscripción del nodo global al tópico `turtle1/pos` publicado por el nodo `turtlesim` y obtener el último mensaje emitido por este tópico.

_Procedimiento:_
1. Suscribir el nodo global al tópico: `posSus = rossubscriber('/turtle1/pose');`
2. Se genera una variable que contiene el último mensaje emitido por este tópico: `LM = posSus.LatestMessage;`

Se utiliza el servicio `dynamixel_workbench_msgs/DynamixelCommand`.

![image](https://github.com/dlozanob/Robotica/assets/69172002/0f2016ef-0b11-41be-a0d3-72488367347f)

- id : Número de id del motor a accionar

- command : ' ' por defecto

- addr_name : 

  - 'Goal_Position' : Comando de movimiento

  - 'Torque_Limit' : Estabecer límite de torque

- value : Valor de posición del actuador

  

Función de envío de datos por el servicio:

```python
def jointCommand(command, id_num, addr_name, value, time):
    rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
    try:
        dynamixel_command = rospy.ServiceProxy(
            '/dynamixel_workbench/dynamixel_command', DynamixelCommand)
        result = dynamixel_command(command,id_num,addr_name,value)
        #rate.sleep()
        rospy.sleep(time)
        return result.comm_result
    except rospy.ServiceException as exc:
        print(str(exc))
```



Se crearon las siguientes funciones para automatizar el proceso:



```python
def setTorqueLimits(tl):
    for i in range(len(tl)):
        jointCommand('', i + 1, 'Torque_Limit', tl[i], 0)

def setPose(q, takt):
    for i in range(len(q)):
        jointCommand('', i + 1, 'Goal_Position', q[i], takt)
```



Poses y límites de torque:

```python
        torqueLimits = [600, 500, 400, 400, 300]
        p1 = [0, 398, 850, 426, 1021]
        p2 = [206, 684, 746, 742, 400]
```



## Configuración en las cinco poses deseadas

En esta sección se describe el procedimiento realizado para poder configurar cinco poses predeterminadas del robot, poder variar entre cada una de ellas mediante un menú de selección, visualizar en simulación la pose deseada y finalmente enviar la pose seleccionada al ejecutable en Python comunicado con ROS.

![](Imagenes/Pasted%20image%2020240414174649.png)

### Interfaz de usuario en Matlab

La interfaz de usuario fue desarrollada utilizando la herramienta Guide de Matlab, la cual permite configurar una GUI con elementos propios de Matlab tales como botones, menús desplegables, imágenes, gráficas, entre otros elementos.
Para desarrollarla fue necesario primero ejecutar el comando _Guide_ en la ventana de comandos, al hacer esto se abrirá la siguiente ventana:

![](Imagenes/gui.png)

Se dispusieron los siguientes elementos, cada uno configurado con un nombre o _Tag_, el cual permite referenciar el elemento en el código de Matlab mediante una función o un llamado determinado. Dentro de cada una de estas funciones se ejecutan ciertos comandos o instrucciones que se desean vincular con cada uno de los elementos de la interfaz.

![](Imagenes/estructura.png)

Para cada elemento dispuesto en la interfaz se debe usar el prefijo _handles_, el cual permite identificar que se trata de un elemento de la interfaz. Por ejemplo, para cargar el logo se usó:

![](Imagenes/logo.png)

Posteriormente la función referente al menú desplegable fue configurada para que cuando se seleccionara una de las poses dispuestas en un vector, se almacenara el índice de la pose deseada en la variable _SelectedPose_. Es importante aclarar que las variables inicialmente son locales, por lo que si se requiere que un valor obtenido dentro de una función de un elemento de la interfaz pueda usarse de manera global, es necesario llamar la función _guidata_.

![](Imagenes/popupmenu.png)

En el caso de la función del Push Button, se estableció que recuperara la información de _guidata_ para almacenarla su valor. En esta función de igual forma se realizó la definición de la cadena cinemática con el fin de que solo se actualizara la gráfica de la pose de la interfaz hasta que se pulsara el botón _Enviar_. Finalmente dentro de esta función también se guardaba la pose seleccionada en un archivo_.txt_ para su posterior lectura en Python:

![](Imagenes/push.png)

A continuación se muestra la interfaz realizada:

![](Imagenes/interfaz.png)

### Comunicación Matlab-Python
Debido a que se quería realizar la ejecución de ROS desde Matlab y que por esto el comando _rosinit_ entraba en conflicto con el comando _roslaunch_ al cada uno intentar ejecutar un nodo maestro, se optó por realizar únicamente desde Matlab la configuración de la cadena cinemática, la interfaz de usuario y la selección de pose del usuario, para finalmente exportar los ángulos deseados a un archivo de texto que posteriormente abre y lee Python con el fin de adaptarlos y enviarlos para su posterior ejecución en ROS:

  



### Comunicación Python-Ros



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


## Códigos

- [MATLAB + Python + ROS](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%204/Codigos/matlabSrv.py)
- [MATLAB GUI](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%204/Codigos/Interfaz%20Matlab/RobotControlApp.m)
- [Publicador](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%204/Codigos/jointPub1.py)
- [Cliente del servidor](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%204/Codigos/jointSrv1.py)
- [Gráfica con Matlab](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%204/Codigos/GraficaMatlab.mlx)
