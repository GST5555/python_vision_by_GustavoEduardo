#!/usr/bin/python
#coding: utf-8

from PIL import Image
from numpy import array
import cv
import numpy as np
import math
from time import time

def normalizacion(matriz,i,j):
  arr_n = np.zeros(shape = (i,j))
  #Toma valor minimo de matriz a ______
  a = matriz.min()
  #Toma valor maximo de matriz ______ b
  b = matriz.max()
  #valor de la convolución x
  for n in xrange(i):
   for m in xrange(j):
    arr_n[n,m] = int(255*(matriz[n,m] - a) / (b-a)) 

  return arr_n

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
 arr_sol = np.zeros(shape = (i,j))
 arr_sol_x = np.zeros(shape = (i,j))
 arr_sol_y = np.zeros(shape = (i,j))

 (n,m) = (1,1)
 a = arr_gry

 #Para el filtro pasa altos:
 for n in xrange(i-1):
  for m in xrange(j-1):
    p_z_9 = array([(a[n-1,m-1],a[n-1,m],a[n-1,m+1]),(a[n,m-1],a[n,m],a[n,m+1]),(a[n+1,m-1],a[n+1,m],a[n+1,m+1])]) 
    conv = np.sum(p_z_9*F_pas_alt)
    arr_p_a[n,m] = conv
 arr_p_a_n = normalizacion(arr_p_a,i,j)
 #Para el filtro gaussiano
 for n in xrange(i-1):
  for m in xrange(j-1):
    p_z_9 = array([(a[n-1,m-1],a[n-1,m],a[n-1,m+1]),(a[n,m-1],a[n,\
m],a[n,m+1]),(a[n+1,m-1],a[n+1,m],a[n+1,m+1])])
    conv = np.sum(p_z_9*Filter_gauss)
    arr_f_g[n,m] = int(conv)
 arr_gua_n = normalizacion(arr_f_g,i,j)
 #Prewitt de detección de bordes
 for n in xrange(i-1):
  for m in xrange(j-1):
    p_z_9 = array([(a[n-1,m-1],a[n-1,m],a[n-1,m+1]),(a[n,m-1],a[n,m],a[n,m+1]),(a[n+1,m-1],a[n+1,m],a[n+1,m+1])])
    gx = np.sum(p_z_9*PrewittX)
    gy = np.sum(p_z_9*PrewittY)
    xm = pow(gx,2)
    ym = pow(gy,2)
    g = int(math.sqrt(xm+ym))

    arr_pre[n,m] = g
 arr_pre_n = normalizacion(arr_pre,i,j) 

 for n in xrange(i-1):
  for m in xrange(j-1):
    p_z_9 = array([(a[n-1,m-1],a[n-1,m],a[n-1,m+1]),(a[n,m-1],a[n,m],a[n,m+1]),(a[n+1,m-1],a[n+1,m],a[n+1,m+1])])
    gx = np.sum(p_z_9*SobelX)
    gy = np.sum(p_z_9*SobelY)
    xm = pow(gx,2)
    ym = pow(gy,2)
    g = int(math.sqrt(xm+ym))
    arr_sol_x[n,m] = gx
    arr_sol_y[n,m] = gy
    arr_sol[n,m] = g
 arr_sol_n = normalizacion(arr_sol,i,j)
 arr_sol_xn = normalizacion(arr_sol_x,i,j) 
 arr_sol_yn = normalizacion(arr_sol_y,i,j)
 
 cv.SaveImage("pasa_altos.png",cv.fromarray(arr_p_a))
 im_p_a = cv.LoadImage('pasa_altos.png')
 cv.ShowImage('pasa altos',im_p_a)
 
 cv.SaveImage("gauss.png",cv.fromarray(arr_f_g))
 im_gau = cv.LoadImage('gauss.png')
 cv.ShowImage('gauss',im_gau)
  
 cv.SaveImage("Prewitt.png",cv.fromarray(arr_pre))
 im_pre = cv.LoadImage('Prewitt.png')
 cv.ShowImage('Prewitt',im_pre)
 
 cv.SaveImage("gauss_norm.png",cv.fromarray(arr_gua_n))
 im_gau_n = cv.LoadImage('gauss_norm.png')
 cv.ShowImage('Gauss Normalizado',im_gau_n)

 cv.SaveImage("Pasa_alto.png",cv.fromarray(arr_p_a_n))
 im_p_a_n = cv.LoadImage('Pasa_alto.png')
 cv.ShowImage('Pasa Altos Normailizado',im_p_a_n)

 cv.SaveImage("Prewitt_n.png",cv.fromarray(arr_pre_n))
 im_pwtt_n = cv.LoadImage('Prewitt_n.png')
 cv.ShowImage('Prewitt Normalizado',im_pwtt_n)
 
 cv.SaveImage("Sobel.png",cv.fromarray(arr_sol))
 im_sobel = cv.LoadImage('Sobel.png')
 cv.ShowImage('Sobel',im_sobel)

 cv.SaveImage("Sobel_n.png",cv.fromarray(arr_sol_n))
 im_sol_n = cv.LoadImage('Sobel_n.png')
 cv.ShowImage('Sobel Normalizado',im_sol_n)

 cv.SaveImage("Sobel_x.png",cv.fromarray(arr_sol_x))
 im_sol_x = cv.LoadImage('Sobel_x.png')
 cv.ShowImage('Sobel X',im_sol_x)

 cv.SaveImage("Sobel_y.png",cv.fromarray(arr_sol_y))
 im_sol_y = cv.LoadImage('Sobel_y.png')
 cv.ShowImage('Sobel Y',im_sol_y)

 cv.SaveImage("Sobel_x_n.png",cv.fromarray(arr_sol_xn))
 im_sol_x_n = cv.LoadImage('Sobel_x_n.png')
 cv.ShowImage('Sobel X Normalizado',im_sol_x_n)

 cv.SaveImage("Sobel_y_n.png",cv.fromarray(arr_sol_yn))
 im_sol_y_n = cv.LoadImage('Sobel_y_n.png')
 cv.ShowImage('Sobel Y Normalizado',im_sol_y_n)

 t_final = time()
 t_total = t_final - t_inicial
 print "Tiempo de ejecución: ",t_total
 cv.WaitKey(0)
if __name__ == '__main__':
    main()
