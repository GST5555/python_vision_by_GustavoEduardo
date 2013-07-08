#!/usr/bin/python
#coding: utf-8

#Advertencia: No pude usar el DFS por que no supe como guardar los diferentes conjuntos que generaba que serian los diferentes bordes, Estoy en el Wall of Shame.

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
    cv.SaveImage("Gray.png",cv.fromarray(mtz_gry))
    im_gry = cv.LoadImage("Gray.png")    
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
          
          if g > 150: #Este numero sirve de umbral para quitar ruido
             p_bordes[(n,m)] = (gx, gy, g)
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
    return p_bordes

def dfs(p_bordes,i,j):
    visitados = []
    z = 0
    for (x,y) in p_bordes:
        cola = [(x,y)]
        if not cola in visitados:
            
            while len(cola) > 0:
                
                (x,y) = cola.pop(0)
                visitados.append((x,y))
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        if dx !=0 or dy !=0:
                            #Esto es para no salirse de la imagen
                            if y+dy >= 0 and y+dy < j                                            and x+dx >= 0 and x+dx < i:
                                 vecino = (x + dx,y + dy)
                                 if vecino in p_bordes:
                                     cola.append((vecino))

def grueso(p_bordes,i,j):
    ext_bor = dict()
    for (x,y) in p_bordes:
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx !=0 or dy !=0:
                            #Esto es para no salirse de la imagen
                            if y+dy >= 0 and y+dy < j and x+dx >=                                0 and x+dx < i:
                                vecino = (x+dx,y+dy)
                                ext_bor[vecino] = 255
    p_bordes.update(ext_bor)
    new_bor = np.zeros(shape = (i,j))
    for (n,m) in p_bordes:
        new_bor[n,m] = 255

    cv.SaveImage("Borde_Grueso.png",cv.fromarray(new_bor))
    im_grue = cv.LoadImage("Borde_Grueso.png")
    cv.ShowImage('Ensanchado',im_grue)

def adelgaza(p_bordes,i,j):
    ext_bor = dict()
    for (x,y) in p_bordes:
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx !=0 or dy !=0:
                            #Esto es para no salirse de la imagen
                            if y+dy >= 0 and y+dy < j and x+dx >=                                0 and x+dx < i:
                                vecino = (x+dx,y+dy)
                                ext_bor[vecino] = 0
    p_bordes.update(ext_bor)
    new_bor = np.zeros(shape = (i,j))
    for (n,m) in p_bordes:
        new_bor[n,m] = p_bordes[n,m]

    cv.SaveImage("Borde_delgado.png",cv.fromarray(new_bor))
    im_grue = cv.LoadImage("Borde_dalgado.png")
    cv.ShowImage('Delgado',im_grue)


def main():
    t_inicial = time()

    im = Image.open('starman.png')
    im.show()
    arr_rgb = array(im)
    (i,j) = (arr_rgb.shape[0],arr_rgb.shape[1])
    
    arr_gry = RGBtoGry(arr_rgb,i,j) #llamamos a RGB to Gray
    p_bordes = dict()
    p_bordes = convolucion(arr_gry,i,j,p_bordes) #llamamos a convolución

    #dfs(p_bordes,i,j)
    print 'engordar: e'
    print 'adelgazar: a'

    get = raw_input('¿Qué hago?:')

    if get == 'e':
        grueso(p_bordes,i,j)
    elif get == 'a':
        adelgaza(p_bordes,i,j)
    else:
        print 'Nada vuelve a intentar'
        main()
        
#    print p_bordes

    t_final = time()
    t_total = t_final - t_inicial
    print "Tiempo de convolución: ",t_total

    cv.WaitKey(0)

if __name__ == '__main__':
    main()
