#!/usr/bin/python
#coding: utf-8

from PIL import Image
from numpy import array
import numpy as np
import math
from time import time
from math import pi

def rectas(gx,gy,i,j):
    sec_piz = 3            #Divido mi media pizza en 3 pedazos
    orientaciones = dict() #visto en clase aun no lo entiendo
    
    for x in xrange(i):
     for y in xrange(j):
      #Como la funcion se manda a llamar cuando se tiene un borde
      #Ya no se checa si el pixel es borde por que
      #Es pixel de borde
      tetha = atan2(gy,gx) #No tengo una matris de gx y gy
      #Esto se hace en el momento de detección del borde
      #Lo que sea borde, se analisara a si es recta
      tetha += pi #se le suma pi [...]
      tetha /= (2.0 * pi) #se divide entre 2pi para tener grados
      tetha *= 360.0
      if tetha > 180.0:  #Si es mayor que 180°
         tetha -= 180.0 #le restamos 180 para
                        #tener su angulo equivalente
         ang_sec_piz = 180.0 / sec_piz #angulo de la pizza
         plato = int(tetha / ang_sec_piz) % sec_piz
         #sacamos si tethan pertenece a que sec_piz con su modulo
         #nos aseguramos que sea entero
         if plato == sec_piz: #si el plato es igual a la sec_piz
            plato -= 1 #le restamos 1
         orientaciones[(x,y)] = plato #este pixel petenecera a una sección (x,y) = sec_piz_1, (x,y) = sec_piz_2, (x,y) = sec_piz_3.

    lineas = dict() #Creo que esto sirve para guardar cosas 
    #Cuando se lleno ?_¿
    for x in xrange(i):
     for y in xrange(j):
      pixel = (x,y)
      plato = orientaciones[pixel]
      if plato in lineas: 
        lineas[plato].append(pixel) #si el plato ya esta en lineas
                                    #ese pixel se guarda el lienas
                                    #dentro de una de los 3 platos
      else:
        lineas[plato] = [pixel]     #Si no hay ese plato en lineas
                                    #quiere decir que es nuevo
                                    #y tendra sus propios pixeles
    lineas = lineas.values() #regresamos una copia de los valores
    
    #Aqui queda pendiente para generar imagen de bordes rectos

def main():
           t_inicial = time()

           #Imagen a trabajar
           im = Image.open('Gray_rectas.png')
           #im.show() #porsi quieres ver lo que cargas al correr
           arr_gry = array(im) #im en arreglo de numpy
           
           (i,j) = (arr_gry.shape[0],arr_gry.shape[1])
           #Lo anterior es para sacar ancho y alto en i,j
           arr_rec = np.zeros(shape = (i,j))
           arr_bor = np.zeros(shape = (i,j))
           #Lo anterior es para cerar arreglo nuevo
           #Que sirva para guardar los bordes y rectas.
           
           mask_Prewx = array([(-1,0,1),(-1,0,1),(-1,0,1)])
           mask_Prewy = array([(1,1,1),(0,0,0),(-1,-1,-1)])
           #Los arreglos de arriba son las mascaras Prewitt
           
           #Se descarta el marco de la imagen en 1 pix de grosor
           (n,m) = (1,1)
           
           for n in xrange(i-1): #Barremos por filas sin la ultima
              for m in xrange(j-1): #Barremos j sin la ultima
                 p_z_9 = array([(a[n-1,m-1],a[n-1,m],a[n-1,m+1]),(a[n,m-1],a[n,m],a[n,m+1]),(a[n+1,m-1],a[n+1,m],a[n+1,m+1])])
                 gx = np.sum(p_z_9*mask_Prewx)
                 gy = np.sum(p_z_9*mask_Prewy) 
                 
                 xm = pow(gx,2)
                 ym = pow(gy,2)

                 g = int(math.sqrt(xm+ym))

                 if g > 200:      #Umbral anterior 135
                    g = 255       #Es borde
                    rectas(gx,gy,i,j) #Se revisara que sea recta
                 elif g < 0:
                      g = 0
                 else:
                      g = 0

                 arr_bor[n,m] = g
                 #Con lo de arriba se crea nueva imagen de bordes
                 
           t_final = time()
           t_total = t_final - t_inicial
           print "Tiempo de este codigo: ",t_total

if __name__ == '__main__':
    main()
