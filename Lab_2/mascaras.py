#!/usr/bin/python
#coding: utf-8

from PIL import Image
from numpy import array
import cv
import numpy as np
import math
from time import time

'''
def normalización(matriz):

  #Toma valor minimo de matriz a ______
  a = matriz.min()
  #Toma valor maximo de matriz ______ b
  b = matriz.max()
  #valor de la convolución x
  
'''

def main():

 t_inicial = time()

 RobertsX = array([[0, 1], [-1, 0]])
 RobertsY = array([[1, 0], [0, -1]])
 SobelX   = array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
 SobelY   = array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
 PrewittX = array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
 PrewittY = array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
 Filter_gauss = array([[1, 2, 1],[2, 8, 2],[1, 2, 1]])
 F_pas_alt = array([[-1,-1, -1],[-1,8,-1],[-1,-1,-1]]) 

 im = Image.open('Gray_starman.png')
 im.show()
 arr_gry = array(im)
 (i,j) = (arr_gry.shape[0],arr_gry.shape[1])
 
 arr_rob = np.zeros(shape = (i,j))
 arr_sob = np.zeros(shape = (i,j))
 arr_pre = np.zeros(shape = (i,j))
 arr_f_g = np.zeros(shape = (i,j))
 arr_p_a = np.zeros(shape = (i,j))

 (n,m) = (1,1)
 a = arr_gry

 #Para el filtro pasa altos:
 for n in xrange(i-1):
  for m in xrange(j-1):
    p_z_9 = array([(a[n-1,m-1],a[n-1,m],a[n-1,m+1]),(a[n,m-1],a[n,m],a[n,m+1]),(a[n+1,m-1],a[n+1,m],a[n+1,m+1])]) 
    conv = np.sum(p_z_9*F_pas_alt)
    arr_p_a[n,m] = conv
 #Para el filtro gaussiano
 for n in xrange(i-1):
  for m in xrange(j-1):
    p_z_9 = array([(a[n-1,m-1],a[n-1,m],a[n-1,m+1]),(a[n,m-1],a[n,\
m],a[n,m+1]),(a[n+1,m-1],a[n+1,m],a[n+1,m+1])])
    conv = np.sum(p_z_9*Filter_gauss)
    arr_f_g[n,m] = int(conv/20)
 #Prewitt de detección de bordes
 for n in xrange(i-1):
  for m in xrange(j-1):
    p_z_9 = array([(a[n-1,m-1],a[n-1,m],a[n-1,m+1]),(a[n,m-1],a[n,m],a[n,m+1]),(a[n+1,m-1],a[n+1,m],a[n+1,m+1])])
    gx = np.sum(p_z_9*PrewittX)
    gy = np.sum(p_z_9*PrewittY)
    xm = pow(gx,2)
    ym = pow(gy,2)
    g = int(math.sqrt(xm+ym))

    #Dada la informcaión de g se podra sacar lo que es el borde

    if g > 135:
       g = 255
    elif g < 0:
         g = 0
    else:
         g = 0 #no se pero quita lineas tenues lol
    arr_pre[n,m] = g
  
 cv.SaveImage("pasa_altos.png",cv.fromarray(arr_p_a))
 im_p_a = Image.open('pasa_altos.png')
 im_p_a.show(title="pasa altos")
 
 cv.SaveImage("gauss.png",cv.fromarray(arr_f_g))
 im_gau = Image.open('gauss.png')
 im_gau.show(im_gau,'gauss')

 cv.SaveImage("Prewitt.png",cv.fromarray(arr_pre))
 im_gau = Image.open('Prewitt.png')
 im_gau.show(im_gau,"lol")
 
 t_final = time()
 t_total = t_final - t_inicial
 print "Tiempo de ejecución: ",t_total

if __name__ == '__main__':
    main()
