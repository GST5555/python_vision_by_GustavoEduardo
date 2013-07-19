#!/usr/bin/python
#coding: utf-8

from numpy import array
import cv
import math
from time import time
import os, sys

try:
    import PIL
    from PIL import Image, ImageChops
    from PIL.GifImagePlugin import getheader, getdata
except ImportError:
    PIL = None

try:
    import numpy as np
except ImportError:
    np = None    

try:
    from scipy.spatial import cKDTree
except ImportError:
    cKDTree = None

def readGif(filename, asNumpy=True):
    """ readGif(filename, asNumpy=True)    
    Read images from an animated GIF file.  Returns a list of numpy arrays, or, if asNumpy is false, a list if PIL images.
    """
    
    # Check PIL
    if PIL is None:
        raise RuntimeError("Need PIL to read animated gif files.")
    
    # Check Numpy
    if np is None:
        raise RuntimeError("Need Numpy to read animated gif files.")
    
    # Check whether it exists
    if not os.path.isfile(filename):
        raise IOError('File not found: '+str(filename))
    
    # Load file using PIL
    pilIm = PIL.Image.open(filename)    
    pilIm.seek(0)
    
    # Read all images inside
    images = []
    try:
        while True:
            # Get image as numpy array
            tmp = pilIm.convert() # Make without palette
            a = np.asarray(tmp)
            if len(a.shape)==0:
                raise MemoryError("Too little memory to convert PIL image to array")
            # Store, and next
            images.append(a)
            pilIm.seek(pilIm.tell()+1)
    except EOFError:
        pass

    # Done
    return images

def main():

    t_inicial = time()

    ima_gif = readGif(sys.argv[1])

    #print ima_gif #Ver que esta arrojando la rutina anterior
    #a =  len(ima_gif) #Revise la longitud de la lista
                       #el mumero fue 32 lo que indica que 
                       #que es el numero de cuadros del video GIF
                       #se revisaron los cuadros y el numero
                       #coincide.
    #print a #revision del valor de a
    frame = ima_gif[10] #los frames estan seccionados
    #c = frame.shape
    #print c #despues de esto, el arreglo esta ordenado de manera peculiar, se tiene un arrgle lineal de 51 que debería ser la altura, despues se tiene otro arreglo linear que debe ser el ancho es de 59 para la imagen de nuestro tangela, ese arreglo contiene del 0 al 59 los cuatro valores que corresponden a una imagen RGBA (R,G,B,A)
    c = frame(3,3)
    print c
    print frame

    t_final = time()
    t_total = t_final - t_inicial
    print "Tiempo de procesamiento: ",t_total

    cv.WaitKey(0)

if __name__ == '__main__':
    main()
