#!/usr/bin/python
#coding: utf-8

from PIL import Image
from numpy import array
import cv
import numpy as np
import math
from time import time

def RGBtoGry(Ary_RGB,i,j):
    mtz_gry = np.zeros(shape = (i,j))
    for n in xrange(i):
       for m in xrange(j):
          mtz_gry[n,m] = int((np.sum(Ary_RGB[n,m]))/3)
    cv.SaveImage("Gray_1.png",cv.fromarray(mtz_gry))
    im_gry = cv.LoadImage("Gray_1.png")    
    cv.ShowImage('Grises', im_gry)
    return mtz_gry

def convolucion(a,i,j,p_bordes):
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
             p_bordes[(n,m)] = (gx, gy, g)
             #gx,gy,g, (x,y) todo esto es del pixel de borde
             g = 255  #Si el gradiente es mayor a 255 entonces es blanco y es borde
          elif g < 0:   #Si el gradiente es menor a 0 entonces es negro    
             g = 0
          else:       #Este tambien sirve para quitar ruido
             g = 0
          arr_bor[n,m] = g #Si es borde valdra 255 si no lo es sera 0 para fondo; ¡a sí! con esto construimos la imagen de bordes.

    cv.SaveImage("bord_1.png",cv.fromarray(arr_bor))
    im_cv = cv.LoadImage("bord_1.png")
    cv.ShowImage('Bordes',im_cv)    
    return p_bordes

def circulos(p_bordes,i,j):
    r = -24 #Debe estar dado en pixeles
    circulo = dict()
    
    for (n,m) in p_bordes:
        Gx,Gy,G = p_bordes[(n,m)]
        xc = int(  n - ( r * (Gy/G) ) )
        yc = int(  m + ( r * (Gx/G) ) )
        xo = int(  n + ( r * (Gy/G) ) )
        yo = int(  m - ( r * (Gx/G) ) )
       
        #if xc < 0 or xo < 0 or yc < 0 or yo < 0 or xc >= i or xo >= i or yc >= j or yo >= j:
        #if xc >= 0 and yc >= 0 and xc < i and yc < j:
        if (xc,yc) in circulo:
                circulo[(xc,yc)] += 1
        else:
                circulo[(xc,yc)] = 0            
            
        #if xo >= 0 and yo >= 0 and xo < i and yo < j:
        if (xo,yo) in circulo:
                circulo[(xo,yo)] += 1
        else:
                circulo[(xo,yo)] = 0
        #print xc,yc,xo,yo
        #print circulo
        #print Gx,Gy,G
    apunto = np.zeros(shape = (i,j,3))
    #print (i,j)
    for (n,m) in circulo:
        #x = n
        #y = m
        #print (x,y)
        if n>=0 and m>=0 and n<i and m<j:
            apunto[n,m] = 255,255,0

    for (n,m) in p_bordes:
        apunto[n,m] = 255,255,255
        
    for (n,m) in circulo:
        if circulo[n,m] > 0:
            apunto[n,m] = 140,0,255

    cv.SaveImage("apunto_6.png",cv.fromarray(apunto))
    im_apun = cv.LoadImage("apunto_6.png")
    cv.ShowImage('Votos XD',im_apun)
           
def main():
    t_inicial = time()

    im = Image.open('ciruculo_az.png')
    im.show()
    arr_rgb = array(im)
    (i,j) = (arr_rgb.shape[0],arr_rgb.shape[1])
    
    arr_gry = RGBtoGry(arr_rgb,i,j) #llamamos a RGB to Gray
    p_bordes = dict()
    p_bordes = convolucion(arr_gry,i,j,p_bordes) #llamamos a convolución

    circulos(p_bordes,i,j)
    
    # print p_bordes    

    t_final = time()
    t_total = t_final - t_inicial
    print "Tiempo de procesamiento: ",t_total

    cv.WaitKey(0)

if __name__ == '__main__':
    main()
