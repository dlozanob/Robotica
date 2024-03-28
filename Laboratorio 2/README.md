# Laboratorio 2

## Integrantes:

- Oscar Julian Olivos Aguirre
- Daniel Lozano Barrero

## Introducción

## Desarrollo de la práctica

La guía propuesta para el desarrollo de la práctica de laboratorio en las instalaciones de CDM, dispones de instrucciones para la programación de un robot _SCARA T6_ de la marca _Epson_. No obstante, en la visita se dispuso únicamente de un robot de 6 ejes de la serie _VT_.

Por este motivo, tuvo que verse modificado el código de la guía realizado previamente por el equipo, con la finalidad de que el robot dispuesto ejecutase las mismas rutinas que un robot _Scara_.

El algoritmo desarrollado por el robot se descompone en $3$ rutinas principales:
- _Paletizado en z_
- _Paletizado en s_
- _Paletizado externo_

El programa se comunica con el controlador mediante USB, seleccionando la opción en la interfaz de usuario:

![[Pasted image 20240327222047.png]]

En la pestaña de administrador del robot, se mueve la máquina a una posición de _Home_, se enseña la posición y se le da el nombre de _Origen_.
Así mismo, moviendo el efector final del robot mediante los ejes coordenados globales, se establecen dos posiciones más:

- _Eje x_ : Punto distanciado de _Home_ únicamente por el eje _x_
- _Eje y_ : Punto distanciado de _Home_ únicamente por el eje _y_

>[!Note]
>Las distancias a _Home_ fueron arbitrarias, siempre y cuando el robot no colisionase con algún objeto, y las coordenadas estuviesen dentro del espacio de trabajo del efector final

![[Pasted image 20240327222615.png]]

![[Pasted image 20240327222813.png]]

Procedimiento de enseñanza de coordenadas:
1. Establecer pose de origen del robot
2. Enseñar el punto y llamarlo _Origen_
3. Establecer pose del robot variando únicamente su posición en el eje _x_
4. Enseñar el punto y llamarlo _Eje x_
5. Ir a la pestaña _Ejecutar movimiento_, seleccionar el punto de destino como _Origen_ y ejecutar
6. Establecer pose del robot variando únicamente su posición en el eje _y_
7. Enseñar el punto y llamarlo _Eje y_
8. Ir a la pestaña _Ejecutar movimiento_, seleccionar el punto de destino como _Origen_ y ejecutar

Se poseen los siguientes puntos:

![[Pasted image 20240327222832.png]]

Ahora bien, se modifica el código _SPEL+_ del programa en el archivo `Main.prg`.

Se declaran variables globales, como la variable `altura`, la cual define el desplazamiento en el eje $z$ en las funciones de paletizado.
La función principal `main` ordena el encendido de motores y el nivel de potencia, así mismo, se establecen los valores de velocidad y aceleración. 

Al inicio el robot se desplaza a su posición _Home_ y entra un bucle de tipo _Do While_. Se hace llamado a las funciones de _paletizado en z_, _paletizado en s_ y _paletizado externo_, en ese mismo orden.

![[Pasted image 20240327224327.png]]

>[!Note]
>`Out_11` y `Out_12` son variables de salidas digitales, en la práctica no se usan

>[!Warning]
>Al ejecutar un programa por primera vez, debe utilizarse el comando `Power Low`, ya que, el movimiento del robot debe ser lo suficiéntemente lento para poder detenerlo en caso de riesgo de colisión. 
>
>Se recomienda que una vez ejecutado por primera vez y usar la opción de potencia alta, la velocidad y la aceleración no excedan valores de $40$

Las funciones de paletizado se caracterizan por brindar el índice del elemento de la cuadrícula.
`Go Pallet(<# instancia paletizado>, <índice del elemento>)`

Para el paletizado en $z$ se instancia el objeto _Pallet_ con una cuadrícula de $3$ x $3$, planteando como base a los 3 puntos anteriormente generados.

![[Pasted image 20240327230046.png]]

Se itera sobre los índices desde el elemento $1$ hasta el $9$.

Cada iteración debe estar inicialmente en un valor mayor de $z$, de tal manera que posteriormente el _TCP_ descienda a un valor menor de $z$ y finalmente vuelva a la coordenada de $z$ inicial.

![[Pasted image 20240327225144.png]]

>[!Note]
>Debido a que el robot es de tipo 6 ejes, deben ajustarse los valores de $z$ por iteración, este ajuste adicional no habría que hacerlo con un robot _Scara_







![[Pasted image 20240327225203.png]]

![[Pasted image 20240327225251.png]]



