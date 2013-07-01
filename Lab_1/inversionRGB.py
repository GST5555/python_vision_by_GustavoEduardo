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

    for n in xrange(i):
      for m in xrange(j):
        r,g,b = arr_rgb[n,m]
        arr_rgb[n,m] = r,g,b
    
    cv.SaveImage("inverted_starman.png",cv.fromarray(arr_rgb))

    im_inv = Image.open('inverted_starman.png')
    im_inv.show()    

    t_final = time()
    t_total = t_final - t_inicial
    print "Tiempo de ejecución: ",t_total

if __name__ == '__main__':
    main()
