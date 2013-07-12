#!/usr/bin/python
#coding: utf-8

from PIL import Image
from numpy import array
import cv
import numpy as np
import math
from time import time
from math import pi, atan2
import random

def RGBtoGry(Ary_RGB,i,j):
    mtz_gry = np.zeros(shape = (i,j))
    for n in xrange(i):
       for m in xrange(j):
          mtz_gry[n,m] = int((np.sum(Ary_RGB[n,m]))/3)
    cv.SaveImage("Cuadrados_Gray.png",cv.fromarray(mtz_gry))
    im_gry = cv.LoadImage("Cuadrados_Gray.png")    
    cv.ShowImage('Grises', im_gry)
    return mtz_gry

def convolucion(a,i,j,coor_grad):
    arr_bor = np.zeros(shape = (i,j))
    #Barrido para la mascara Prewitt
    mask_Prewx = array([(-1,0,1),(-1,0,1),(-1,0,1)])
    mask_Prewy = array([(1,1,1),(0,0,0),(-1,-1,-1)])
    #mask_Robx = ([0,1],[-1,0])
    #mask_Roby = ([-1,0],[0,-1])
    # Me comere las lineas de las imagnes y las reconstruire duplicando valores
    n = 1
    m = 1
    
    for n in range(i-1):   #Barremos por filas
      for m in range(j-1): #Barremos por columnas
          p_z_9 = array([(a[n-1,m-1],a[n-1,m],a[n-1,m+1]),(a[n,m-1],a[n,m],a[n,m+1]),(a[n+1,m-1],a[n+1,m],a[n+1,m+1])]) 
          
          gx = np.sum(p_z_9*mask_Prewx)
          gy = np.sum(p_z_9*mask_Prewy)
          
          xm = pow(gx,2)
          ym = pow(gy,2)
          g = int(math.sqrt(xm+ym))
          
          if g > 170: #Este numero sirve de umbral para quitar ruido
             coor_grad[(n,m)] = (gx, gy, g)
             #gx,gy,g, (x,y) todo esto es del pixel de borde
             g = 255  #Si el gradiente es mayor a 255 entonces es blanco y es borde
          elif g < 0:   #Si el gradiente es menor a 0 entonces es negro    
             g = 0
          else:       #Este tambien sirve para quitar ruido
             g = 0
          arr_bor[n,m] = g #Si es borde valdra 255 si no lo es sera 0 para fondo; ¡a sí! con esto construimos la imagen de bordes.

    cv.SaveImage("Cuadrados_bord.png",cv.fromarray(arr_bor))
    im_cv = cv.LoadImage("Cuadrados_bord.png")
    cv.ShowImage('Bordes',im_cv)    
    return coor_grad

def rectas(coor_grad,i,j):

    sec_piz = 4 #Divisiones del medio circulo

    rectas = dict() #Donde guardo dir de rectas
    
    for (n,m) in coor_grad:
        #Sacamos gradientes:
        Gx,Gy,G = coor_grad[(n,m)]
        
        #Sacamos el angulo de gradiente:
        tetha = atan2(Gy,Gx)
        
        #Convertimos a grados °:
        tetha = (tetha * 180.0) / pi
        
        if tetha < 0:
            tetha += 360

        #Si tetha es mayor que 180°
        #Le restamos 180° para su equivalente:
        if tetha > 180.0:
            tetha -= 180.0 
        #print tetha
        ang_sec_piz = 180 / sec_piz #Angulo de la sección

        #para el angulo tetha saco su pertenencia de sección
        plato = int(tetha / ang_sec_piz)
        #print plato

        if plato == sec_piz:
            plato -= 1 #le restamos 1 por si se pasa

        coordenadas = (n,m)
        if plato in rectas:
            #Sección de semi circulo ya existe guardo conjunto
            rectas[plato].append(coordenadas)
        else:
            #Sección de semi circulo aun no existe la creo
            rectas[plato] = [coordenadas]
    
    #Construyo nueva imagen que contiene las rectas diferentes
    arr_recta = np.zeros(shape = (i,j,3))

    #print (i,j)
    
    for x in xrange(sec_piz):
        le_color = random.randint(0,255)
        for n,m in rectas[x]:
            arr_recta[n,m] = 0,le_color,255

    #for (n,m) in p_bordes:
        #apunto[n,m] = 255,255,255

    cv.SaveImage("recta_Cuadrados.png",cv.fromarray(arr_recta))
    im_apun = cv.LoadImage("recta_Cuadrados.png")

    cv.ShowImage('Rectas',im_apun)

    return rectas
           
def main():
    t_inicial = time()

    im = Image.open('Cuadrados.png')
    im.show()
    arr_rgb = array(im)
    (i,j) = (arr_rgb.shape[0],arr_rgb.shape[1])
    
    arr_gry = RGBtoGry(arr_rgb,i,j) #llamamos a RGB to Gray
    coor_grad = dict()
    coor_grad = convolucion(arr_gry,i,j,coor_grad) #llamamos a convolución

    grupo_rectas = rectas(coor_grad,i,j)
    print grupo_rectas
    
    t_final = time()
    t_total = t_final - t_inicial
    print "Tiempo de ejecución: ",t_total

    cv.WaitKey(0)

if __name__ == '__main__':
    main()
