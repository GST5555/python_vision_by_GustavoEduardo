#!/usr/bin/python
#coding: utf-8

from PIL import Image
from numpy import array
import numpy as np
import math
from time import time
import cv

def main():
    t_inicial = time()
 
    im = Image.open('starman.png')
    im.show()
    
    arr_rgb = array(im)

    (i,j) = (arr_rgb.shape[0],arr_rgb.shape[1])
    
    arr_ton_r = np.zeros(shape = (i,j,3))
    arr_ton_g = np.zeros(shape = (i,j,3))
    arr_ton_b = np.zeros(shape = (i,j,3))

    for n in xrange(i):
      for m in xrange(j):
        prom = int((np.sum(arr_rgb[n,m]))/3)
        arr_ton_r[n,m] = 255,prom,prom
        arr_ton_g[n,m] = prom,255,prom
        arr_ton_b[n,m] = prom,prom,255
    
    cv.SaveImage("ton_r_starman.png",cv.fromarray(arr_ton_r))
    cv.SaveImage("ton_g_starman.png",cv.fromarray(arr_ton_g))
    cv.SaveImage("ton_b_starman.png",cv.fromarray(arr_ton_b))

    im_r = Image.open('ton_r_starman.png')
    im_g = Image.open('ton_g_starman.png')
    im_b = Image.open('ton_b_starman.png')

    im_r.show()    
    im_g.show()
    im_b.show()

    t_final = time()
    t_total = t_final - t_inicial
    print "Tiempo de ejecución: ",t_total

if __name__ == '__main__':
    main()
