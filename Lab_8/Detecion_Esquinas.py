#!/usr/bin/python
#coding: utf-8

from PIL import Image, ImageDraw
from numpy import array
import cv
import numpy as np
import math
from time import time

def main():
    t_inicial = time()

    im = Image.open('Gray_Stop.png')
    im.show()
    arr_gry = array(im)
    
    (i,j) = (arr_gry.shape[0],arr_gry.shape[1])

    #Creo arreglo que contendra las medias de la original
    arr_medias = np.zeros( shape = (i,j) )
    arr_esq = np.zeros( shape = (i,j,3) )
    for x in xrange(i):
        for y in xrange(j):
            
            cola = list()
            #Barrido de los ocho vecinos
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    #condición para no salir del arreglo
                    if y+dy>=0 and y+dy<j and x+dx>=0 and x+dx<i:
                        #dirección de n-vecino
                        vecino = (x+dx,y+dy) 
                        #guardo valor de pixel en cola
                        cola.append(arr_gry[vecino])
            #Supongo tengo cola con 9 elementos
            #Los ordeno a continuación: 
            cola = sorted(cola)
            #saco la media y la copio al nuevo arreglo:
            #print x,y
            #print cola
            media = int(len(cola) / 2)
            arr_medias[x,y] = cola[media]
            diferencia = arr_medias[x,y]-arr_gry[x,y]
            #print diferencia
            diferencia = abs(diferencia)
            print diferencia
            if diferencia > 70:
                arr_esq[x,y] = 100,50,255
            else:
                gray = arr_gry[x,y]
                arr_esq[x,y]=gray,gray,gray

    #se supone que ya tengo la matris de medias
    #la mostrare para saber que estoy haciendo:
    im_medias = Image.fromarray(arr_medias)
    im_medias.show()

    #se supone que ya tengo la imagen con esquinas
    #la mostrare para saber que estoy haciendo usando OpenCV:
    cv.SaveImage("Esquina_Stop1.png",cv.fromarray(arr_esq))    
    im_esq = cv.LoadImage("Esquina_Stop1.png")
    cv.ShowImage('Esquinas',im_esq)

    #mi numpy no puede manejar arreglos como las dos lineas de 
    #abajo ¬¬
    #im_esq = Image.fromarray(arr_esq)
    #im_esq.show()

    t_final = time()
    t_total = t_final - t_inicial
    print "Tiempo de ejecución: ",t_total

    cv.WaitKey(0)

if __name__ == '__main__':
    main()
