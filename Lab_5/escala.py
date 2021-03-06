#!/usr/bin/python
#coding: utf-8

from PIL import Image
from numpy import array
import cv
import numpy as np
import math
from time import time

def main():
    t_inicial = time()

    #im = Image.open('inverted_starman.png')
    im = cv.LoadImage("inverted_starman.png")
    cv.ShowImage('original',im)
    #cv.Set(im)
    #im.show()
    arr_rgb = np.asarray(im[:,:])
    (i,j) = (arr_rgb.shape[0],arr_rgb.shape[1])

    (w_n) = int(raw_input('nuevo ancho: '))
    (h_n) = int(raw_input('nuevo alto: '))

    print 'Ancho x Alto original: %d x %d' % (i, j)
    print 'Ancho x Alto nuevo: %d x %d' % (w_n, h_n)

    arr_sca = np.zeros(shape = (w_n,h_n,3))
    raz_an = w_n * 1.0 / i  
    raz_al = h_n * 1.0 / j 
    print 'razon ancho: %f, razon alto: %f' % (raz_an,raz_al)
    for n in xrange(w_n):
        for m in xrange(h_n):
            x = int( (n) / (raz_an) )  
            y = int( (m) / (raz_al) ) 
            arr_sca[n,m] = arr_rgb[x,y]

    cv.SaveImage("scaled.png",cv.fromarray(arr_sca))
    im_sca = cv.LoadImage("scaled.png")
    cv.ShowImage('Escalada',im_sca)

    t_final = time()
    t_total = t_final - t_inicial
    print "Tiempo de escalado: ",t_total

    cv.WaitKey(0)

if __name__ == '__main__':
    main()
