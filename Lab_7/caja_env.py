#!/usr/bin/python
#coding: utf-8

from PIL import Image, ImageDraw
from numpy import array
import cv
import numpy as np
import math
from time import time

def convolucion(a,i,j):
    arr_bor = np.zeros(shape = (i,j))
    #Barrido para la mascara Prewitt
    mask_Prewx = array([(-1,0,1),(-1,0,1),(-1,0,1)])
    mask_Prewy = array([(1,1,1),(0,0,0),(-1,-1,-1)])
    #mask_Robx = ([0,1],[-1,0])
    #mask_Roby = ([-1,0],[0,-1])
    # Me comere las lineas de las imagnes y las reconstruire duplicando valores
    n = 1
    m = 1
    dirc_x = list()
    dirc_y = list()
    borde = dict()
    for n in range(i-1):   #Barremos por filas
      for m in range(j-1): #Barremos por columnas
          p_z_9 = array([(a[n-1,m-1],a[n-1,m],a[n-1,m+1]),(a[n,m-1],a[n,m],a[n,m+1]),(a[n+1,m-1],a[n+1,m],a[n+1,m+1])]) 
          
          gx = np.sum(p_z_9*mask_Prewx)
          gy = np.sum(p_z_9*mask_Prewy)
          
          xm = pow(gx,2)
          ym = pow(gy,2)
          g = int(math.sqrt(xm+ym))
          
          if g > 150: #Este numero sirve de umbral para quitar ruido
             dirc_x.append(n)
             dirc_y.append(m)
             borde[n,m]=255
             #gx,gy,g, (x,y) todo esto es del pixel de borde
             g = 255  #Si el gradiente es mayor a 255 entonces es blanco y es borde
          elif g < 0:   #Si el gradiente es menor a 0 entonces es negro    
             g = 0
          else:       #Este tambien sirve para quitar ruido
             g = 0
          arr_bor[n,m] = g #Si es borde valdra 255 si no lo es sera 0 para fondo; ¡a sí! con esto construimos la imagen de bordes.

    cv.SaveImage("bord.png",cv.fromarray(arr_bor))
    im_cv = cv.LoadImage("bord.png")
    cv.ShowImage('Bordes',im_cv)    
    return dirc_x,dirc_y,borde

def main():
    t_inicial = time()

    im = Image.open('Gray1.png')
    im.show()
    arr_gry = array(im)
    
    (i,j) = (arr_gry.shape[0],arr_gry.shape[1])

    p_bordes_x = list() #genero listas de x y y
    p_bordes_y = list()
    p_bordes = dict()

    (p_bordes_x,p_bordes_y,p_bordes) = convolucion(arr_gry,i,j) #llamamos a convolución y extraemos coordendas de los bordes

    #print p_bordes_x,p_bordes_y #para saber que valores tienen

    max_x = max(p_bordes_x)
    min_x = min(p_bordes_x)
    max_y = max(p_bordes_y)
    min_y = min(p_bordes_y)

    #print max_x,min_x,max_y,min_y

    new_im = Image.new('RGB',(j,i),(0,0,0))
    draw = ImageDraw.Draw(new_im)
    
   # draw.line((min_x,min_y, max_x,min_y), fill=(0,255,115))
   # draw.line((min_x,min_y, min_x,max_y), fill=(0,255,115))
   # draw.line((min_x,max_y, max_x,max_y), fill=(0,255,115))
   # draw.line((max_x,min_y, max_x,max_y), fill=(0,255,115))
    
    draw.line((min_y,min_x, max_y,min_x), fill=(0,255,115))
    draw.line((min_y,min_x, min_y,max_x), fill=(0,255,115))
    draw.line((min_y,max_x, max_y,max_x), fill=(0,255,115))
    draw.line((max_y,min_x, max_y,max_x), fill=(0,255,115))


    new_im.show()

    #arr_caj = array(new_im)
    pix = new_im.load()

    for (m,n) in p_bordes:
            #if m >= 0 and m < j and n >= 0 and n < i:
                pix[n,m] = 255,0,255
                #arr_caj[n,m] = 255,0,255

    arr_caj = array(new_im)
    new_im.show()
    cv.SaveImage("caja.png",cv.fromarray(arr_caj))
    im_caj = cv.LoadImage("caja.png")
    cv.ShowImage('envolvencia',im_caj)

    # print p_bordes 

    t_final = time()
    t_total = t_final - t_inicial
    print "Tiempo de convolución: ",t_total

    cv.WaitKey(0)

if __name__ == '__main__':
    main()
