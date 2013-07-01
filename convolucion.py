#!/usr/bin/python
#coding: utf-8

from PIL import Image
from numpy import array
import cv
import numpy as np
import math
from time import time

#Funcion para sacar la magnitud de gradiente
def edge_mag(gx,gy,n,m):
    xm = pow(gx,2)
    ym = pow(gy,2)
    g = int(math.sqrt(xm+ym))
    #arr_gra(n,m) = g
    if g > 255:
       g = 255  #Si el gradiente es mayor a 255 entonces es blanco
    if g < 0:   #Si el gradiente es menor a 0 entonces es negro
       g = 0
    #arr_bor(n,m) = g #Si es borde valdra 255 si no lo es sera 0

def main():
    t_inicial = time()

    im = Image.open('Gray_figuras.png')
    im.show()
    arr_gry = array(im)
    (i,j) = (arr_gry.shape[0],arr_gry.shape[1])
    arr_gra = np.zeros(shape = (arr_gry.shape[0],arr_gry.shape[1]))
    arr_bor = np.zeros(shape = (arr_gry.shape[0],arr_gry.shape[1]))
#    mask_Robx = ([0,1],[-1,0])
#    mask_Roby = ([-1,0],[0,-1])
    mask_Prewx = array([(-1,0,1),(-1,0,1),(-1,0,1)])
    mask_Prewy = array([(1,1,1),(0,0,0),(-1,-1,-1)])
    a = arr_gry #solo le cambio el nombre
    #Barrido para la mascara Prewitt

# Me comere las lineas de las imagnes y las reconstruire duplicando valores
    n = 1
    m = 1
    for n in range(i-1): #Barremos por filas
      for m in range(j-1): #Barremos por columnas
#Esto no funciona muy impractico
#        if n < 0 and m < 0: #caso espacial de esquina sup izq
#          p_z_9 = array([(255,255,255),(255,a[n,m],a[n,m+1]),(255,a[n+1,m],a[n+1,m+1])])
#          gx = np.sum(p_z_9*mask_Prewx) 
#          gy = np.sum(p_z_9*mask_Prewy)
#          edge_mag(gx,gy,n,m)
#        if n < 0 and m > #caso especial de esquina sup der
#          p_z_9 = array([(255,255,255),(a[n,m-1],a[n,m],a[n,m+1]),(255,a[n+1,m],a[n+1,m+1])])
          p_z_9 = array([(a[n-1,m-1],a[n-1,m],a[n-1,m+1]),(a[n,m-1],a[n,m],a[n,m+1]),(a[n+1,m-1],a[n+1,m],a[n+1,m+1])]) 
          gx = np.sum(p_z_9*mask_Prewx)
          gy = np.sum(p_z_9*mask_Prewy)
          #edge_mag(gx,gy,n,m)
          xm = pow(gx,2)
          ym = pow(gy,2)
          g = int(math.sqrt(xm+ym))
          #arr_gra[n,m] = g
          if g > 135: #Este numero sirve de umbral para quitar ruido
             g = 255  #Si el gradiente es mayor a 255 entonces es blanco
          elif g < 0:   #Si el gradiente es menor a 0 entonces es negro    
             g = 0
          else:       #Este tambien sirve para quitar ruido
             g = 0
          arr_bor[n,m] = g #Si es borde valdra 255 si no lo es sera 0 para fondo; ¡a sí! con esto construimos la imagen de bordes.

    cv.SaveImage("bord_figuras.png",cv.fromarray(arr_bor))
    #im_cv = cv.LoadImage("bord_n_50.png")
    im_b = Image.open('bord_figuras.png')
    im_b.show()
    #cv.ShowImage('imagen',im_cv)
    #cv.WaitKey(0)
 
    t_final = time()
    t_total = t_final - t_inicial
    print "Tiempo de convolución: ",t_total
if __name__ == '__main__':
    main()

#Referencias:
#Blog de Visión Computacional de Esteban Sifuentes Samaniego, 2013
#http://esteban-vision.blogspot.mx/

#Agradecimientos por el apoyo de Estaban Sifuentes Samaniego
