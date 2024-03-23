# Laboratorio 1

## Introducción

En esta práctica de laboratorio se buscaba realizar un primer acercamiento a la programación de robots industriales mediante la escritura del nombre de una marca con su respectivo texto. Para esto el equipo de trabajo debió realizar la definición del WorkObject, la definición de las trayectorias deseadas y la configuración de las entradas y salidas digitales en el software de simulación de RobotStudio y el diseño de la herramienta que permitiera sostener el marcador.


## 1- Descripción de la solución planteada

Se requiere dibujar el logotipo de una empresa haciendo uso del robot industrial IRB 140 disponible en el LAB SIR. Para programarlo se dispone del software Robot Studio, en el que se puede crear y simular la trayectoria deseada del robot. Robot Studio genera un código en RAPID (lenguaje de alto nivel interpretado por el procesador del módulo del robot) que describe las acciones del robot. Este código es cargado al módulo físico donde se ejecuta el algoritmo creado en Robot Studio.

### Configuraciones iniciales

Dentro del programa se importa el robot nombrado anteriormente al área de trabajo:

![](Imagenes/Pasted%20image%2020240301182459.png)

Adicionalmente, se debe contar con el add-in _RobotWare 6.15.05_, el cual es un controlador virtual que simula al controlador que se tiene en el laboratorio. Se activa el controlador desde la opción:

![[Pasted image 20240322214609.png]]




### Estrategia de definición de la trayectoria

Robot Studio permite que el TCP se posicione en un punto (_Target_) definido. Estos _Targets_ poseen su propio sistema de coordenadas, por lo que el robot se moverá hasta que el sistema de coordenadas del TCP coincida con el del _Target_. Siendo así, se puede crear una cadena de puntos para definir una trayectoria.

Para esto, Robot Studio dispone de herramientas donde se pueden seleccionar _Targets_ sobre los bordes o vértices de los objetos de trabajo. Por consiguiente, la superficie del Work object modelado debe representar el dibujo con un grabado para que en Robot Studio se puedan seleccionar los puntos con facilidad.


### Definición e implementación de la geometría

Es necesario dibujar un objeto con una superficie plana sobre la cual el robot pueda dibujar el logotipo. Este objeto debe encontrarse dentro del espacio de trabajo del robot para garantizar que el TCP pueda posicionarse sobre cada punto de la superficie de dibujo.

Se elige el logotipo de _Mitsubishi Motors_ para ser representado.

![](Imagenes/Pasted%20image%2020240322185946.png)

Para delimitar el espacio de trabajo se midió uno de los cuadrantes en los que se encuentra el robot en el laboratorio.

![](Imagenes/Pasted%20image%2020240322190812.png)

Sabiendo esto, se dimensiona la pieza de tal manera que pueda ser posicionada dentro de este cuadrante.
Se seleccionan dimensiones de $90$ x $42$ $cm$. Ahora bien, se modela la geometría en el software Autodesk Inventor.

![](Imagenes/Pasted%20image%2020240322191737.png)

>![Note]
>Se genera un Sketch y dentro de este se dibuja el logotipo y el nombre la empresa, tras esto, se usa la herramienta _Emboss_ que dispone el software, para generar un grabado sobre la superficie.

Como se mencionó en la sección [Estrategia de definición de la trayectoria](#estrategia+de+definición+de+la+trayectoria), para definir los _targets_ que componen la trayectoria, es necesario que la pieza posea los bordes y vértices que la definen. No obstante, el programa solo reconocerá estos vértices si el tipo de archivo de la geometría es de tipo _.sat_. En _inventor_ se exporta la pieza creada con este tipo de extensión.

![](Imagenes/Pasted%20image%2020240322193555.png)

Ahora bien, se importa la geometría al espacio de trabajo.

![](Imagenes/Pasted%20image%2020240322193632.png)

El objeto ahora aparece dentro del programa. Se posiciona en la posición deseada:

![](Imagenes/Pasted%20image%2020240322193741.png)

![](Imagenes/Pasted%20image%2020240322193757.png)

Se ha decidido posicionar el objeto de la siguiente manera para tomar ventaja del espacio y garantizar que el robot pueda dibujar sobre la superficie sin problemas.

![](Imagenes/Pasted%20image%2020240322193836.png)

>[!Note]
>Se utilizan cajas de madera para subir la superficie de dibujo, de tal manera que no se dibuje sobre tablero, sino sobre una superficie con un pliego de papel.
>
>Por esta razón, se posiciona el _Work object_ a $15$ $cm$ en $z$, ya que, esta es la altura determinada por los objetos para elevar la superficie


### Creación del objeto _Work object_

Este objeto define un sistema de coordenadas para la trayectoria que posteriormente es generada. La ventaja de esto, es que una serie de puntos pueden ser reposicionados y reorientados con solo cambiar el sistema de coordenadas que define al _Work object_.

![](Imagenes/Pasted%20image%2020240322194944.png)

![](Imagenes/Pasted%20image%2020240322195519.png)

Se define el _Work object_ en una de las esquinas de la pieza.


### Creación de la trayectoria

Con la herramienta _Target_ se pueden definir los puntos de trayectoria:

![](Imagenes/Pasted%20image%2020240322194437.png)

![](Imagenes/Pasted%20image%2020240322194445.png)

![](Imagenes/Pasted%20image%2020240322194629.png)

Se seleccionan de manera secuencial y se crean con respecto al objeto _Work object_ generado anteriormente.

![](Imagenes/Pasted%20image%2020240322194714.png)

Una vez creados, debe modificarse la orientación del sistema de coordenadas de los _target_. 
Esto teniendo en cuenta que el sistema de coordenadas del _TCP_ debe coincidir con el de los _targets_ para poder alcanzar estos puntos.

Sistema de coordenadas del _TCP_ :

![](Imagenes/Pasted%20image%2020240322195909.png)


Basta con reorientar uno de los _targets_ creados:

![](Imagenes/Pasted%20image%2020240322195957.png)

Una vez reorientado se puede ver que el _TCP_ coincide con el _target_ modificado.

![](Imagenes/Pasted%20image%2020240322200024.png)

Se copia la orientación del _target_ :

![](Imagenes/Pasted%20image%2020240322200119.png)

Se aplica al resto de _targets_ :

![](Imagenes/Pasted%20image%2020240322200204.png)

Los puntos que conforman la trayectoria ya están creados.

Ahora se crea un objeto de tipo _Path_ :

![](Imagenes/Pasted%20image%2020240322200301.png)

Para crear una trayectoria, debe especificarse lo siguiente:

- Tipo de movimiento
	- Lineal (_MoveL_)
	- Articulación (_MoveJ_)
- Velocidad de movimiento
	- _vx_ -> _x_ es la velocidad en mm/s
- Radio de precisión
	- $zx$ -> _x_ es la distancia a partir del punto de destino hasta el punto actual del _TCP_ donde el robot comienza a hacer una curva
- _Work object_

>[!Note]
>Si el robot tuviese un radio de precisión nulo, la dirección de la posición cambiaría de manera abrupta, por tanto, la velocidad sería un delta de dirac, en órdenes mayores de posición esto exige un esfuerzo muy grande al robot, lo que puede suponer un daño en los motores

Seleccionadas estas opciones:

![](Imagenes/Pasted%20image%2020240322201030.png)

Se arrastran todos los _targets_ al _path_ generado.

![](Imagenes/Pasted%20image%2020240322201045.png)

La trayectoria queda definida en el orden en el aparecen los _targets_ y con las configuraciones establecidas antes de arrastrarlos.

Se debe crear un _path_ llamado _main_, el cual será la función de inicio del programa _RAPID_.

![](Imagenes/Pasted%20image%2020240301205522.png)

Se arrastra aquí el _path_ generado.

### Generación del programa y simulación

Se genera el código _RAPID_ al sincronizar los _paths_ de la estación al controlador virtual.

![](Imagenes/Pasted%20image%2020240322201315.png)

![](Imagenes/Pasted%20image%2020240301204948.png)

Se puede simular el código de la siguiente manera:

![](Imagenes/Pasted%20image%2020240322204759.png)

### Entradas y salidas

El programa puede recibir señales digitales para ejecutar un proceso o emitir señales digitales para encender una lámpara de indicación.


Para acceder a las señales de entrada y de salida en Robot Studio:

![](Imagenes/Pasted%20image%2020240301205211.png)

![](Imagenes/Pasted%20image%2020240301205229.png)

Se crean las señales:

![](Imagenes/Pasted%20image%2020240301205247.png)

![](Imagenes/Pasted%20image%2020240301205322.png)

Se pueden ver las señales creadas a continuación:

![](Imagenes/Pasted%20image%2020240301205352.png)

Ahora bien, para implementarlas en el algoritmo se deben de añadir al _path main_ .

![](Imagenes/Pasted%20image%2020240301205610.png)

![](Imagenes/Pasted%20image%2020240301205701.png)

Dentro de las opciones mostradas, se usan:
- _Wait DI_ : Espera a recibir un valor alto en la señal de entrada para ejecutar la siguiente instrucción
- _Set_ : Establece en un valor alto a la señal de salida
- _Reset_ : Establece en un valor bajo a la señal de salida


### Trayectoria de movimiento adicional (plano a $45°$)

Adicionalmente, se genera un _path_ con la misma trayectoria del primer plano, solo que esta vez se hace sobre un plano a $45°$.

>[!Note]
>En el laboratorio se disponía de este plano, pero tiene unas dimensiones más pequeñas que el primer plano, pudo haberse hecho la primer trayectoria con las mismas dimensiones del plano inclinado para solo tener que reposicionar el _Work object_, no obstante, el equipo decidió por dibujar el logotipo de ese tamaño aunque se tuviese que generar de nuevo la trayectoria para el plano inclinado

![](Imagenes/Pasted%20image%2020240301210255.png)

>[!Note]
>El plano inclinado tiene dimensiones $25$ x $25$ $cm$


### Estructura del algoritmo

Implementando las rutinas generadas, además de una posición de mantenimiento al final, y añadiendo entradas y salidas, el algoritmo queda de la siguiente manera:


![](Imagenes/Pasted%20image%2020240301205858.png)

- Espera a la señal de inicio (_DI_01_)
- Activación de la lámpara de indicación (_DO_01_)
- Trayectoria sobre la superficie plana
- Retorno a _Home_
- Trayectoria sobre la superficie a $45°$
- Retorno a _Home_
- Espera a la señal de mantenimiento (_DI_02_)
- Pose de mantenimiento
- Se desactiva la lámpara de indicación (_DO_01_)


## 2- Diagrama de flujo de acciones del robot
Posteriormente se planteó un diagrama de flujo que describirá cada una de las operaciones que deberá llevar a cabo el robot dentro del programa y las condiciones que se deben cumplir para ejecutarse:

![](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%201/Imagenes/Diagrama_Mov.robot.png)

Se puede apreciar que las condiciones de entradas digitales se evalúan de forma secuencial y no en paralelo.

## 3- Plano de planta de la ubicación de cada uno de los elementos

![[Pasted image 20240322213626.png]]


## 4- Diseño de la herramienta

Para el desarrollo de la práctica se comenzó con el diseño preliminar de la herramienta en el software de Autodesk Inventor. La herramienta fue diseñada siguiendo las dimensiones del flanche del robot ABB IRB-140 y las dimensiones del marcador que se encontrará dentro del efector final. Adicionalmente, dentro del diseño de la herramienta se tuvieron en cuenta otros factores importantes como el uso de un sistema de amortiguación que le permitiera al robot por un lado ejercer una leve presión al papel para realizar un trazo claro, adaptandose a las posibles irregularidades o desniveles de la superficie y por otro lado, evitar que la herramienta y el marcador se comporten como un cuerpo rígido permitiendo que al ejercer una presión mayor a la esperada, se produzca un movimiento amortiguado del marcador y con esto evitar que la herramienta o el robot sufran daños.

Se decidió diseñar una herramienta compuesta de dos piezas, el cuerpo en donde se alojará el marcador y el resorte y la tapa, ambas unidas mediante una unión roscada.

![](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%201/Imagenes/Herramienta-cuerpo.png)
![](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%201/Imagenes/Tapa-abajo.png)
![](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%201/Imagenes/Tapa-abajo.png)


Quedando completamente ensamblada de la siguiente forma:

![](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%201/Imagenes/Ensamble-Herramienta.png)

Finalmente, para la fabricación de la herramienta se decidió utilizar manufactura aditiva, obteniendo el siguiente resultado:

![](https://github.com/dlozanob/Robotica/blob/main/Laboratorio%201/Imagenes/Imp3D.png)


## 5- Código en RAPID


## 6- Vídeos de simulación e implementación











