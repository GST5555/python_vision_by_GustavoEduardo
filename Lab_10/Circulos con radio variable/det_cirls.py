#!/usr/bin/python
#coding: utf-8

from PIL import Image, ImageDraw
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
          
          if g > 170: #Este numero sirve de umbral para quitar ruido
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

def DFS(a,i,j):
    #a contiene el diccionario con las coordenadas como key
    #los valores de las keys son gx,gy,g aun hay que guardarlos
    #para usarlos con otras cosas lol XD
    #(i,j) --> Filas,Columnas
    obj = dict()
    
    visit = []
    z = 0 #Numero de grupo o conjunto
    for (n,m) in a:
        coor = (n,m)
        
        if not coor in visit:
            obj[z] = [] #Creo el primer elemento de un objeto borde
            cola = [coor] #Creo mi lista de en cola

            while len(cola) > 0: #mientras alguien espere
                #print cola
                (x,y) = cola.pop(0) #sacamos el primer elemento
                obj[z].append((x,y))#Guardamos las direcciones en el objeto al que pertenecen                       
                visit.append((x,y)) #guardamos que ya usamos este pixel

                #barrido de 8 vecinos
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        #Esto es para no procesar el centro
                        #de la vecindad por que ya pasamos
                        if dx != 0 or dy !=0:
                            #Para no salirnos de la imagen
                            if y+dy>=0 and y+dy<j and x+dx>=0 and x+dx < i:
                                #con esto tenemos la dirección
                                #del vecino
                                vecino = ( x + dx, y + dy ) #Asegurense de que esto no tenga otra cosa que sea (x+dx,y+dy)
                                #Si el vecino es parte de
                                #bordes     
                                if not vecino in visit:
                                    if not vecino in cola:
                                        if vecino in a:
                                            #print vecino
                                            cola.append(vecino)
                #para evitar redundancias ya se tiene en cola
                #todos los vecinos que son borde del objeos
                
            z += 1
        #Aquí salimos del if pero antes indicamos que si se vuelve a entontrar otro grupo u objeto este sera el objeto 1 y así sucesvamente
    return obj
    
def circulos(cir_cor,bor_cor):
    #Diccionario donde guardare los candidatos a centro :D
    circulo = dict()
    
    #debo sacar el radio para esto haré las trampas
    #Mi argumento defensa para esto: YOLO!
    
    max_x = max(x for (x,y) in cir_cor)
    min_x = min(x for (x,y) in cir_cor)
    #obtengo el minimo y maximo en x para sacar el diametro en x
    
    max_y = max(y for (x,y) in cir_cor)
    min_y = min(y for (x,y) in cir_cor)
    #obtengo el minimo y maximo en y para sacar el diametro en y
    #print max_x,min_x,max_y,min_y
    largo = max_x - min_x #magnitud del largo del objeto
    ancho = max_y - min_y #magnitud del ancho del objeto
    #print largo,ancho
    r = -((largo + ancho)/2)/2

    for (n,m) in cir_cor:
        Gx,Gy,G = bor_cor[(n,m)]
        xc = int(  n - ( r * (Gy/G) ) )
        yc = int(  m + ( r * (Gx/G) ) )
        xo = int(  n + ( r * (Gy/G) ) )
        yo = int(  m - ( r * (Gx/G) ) )
       
        #if xc < 0 or xo < 0 or yc < 0 or yo < 0 or xc >= i or xo >= i or yc >= j or yo >= j:
        #if xc >= 0 and yc >= 0 and xc < i and yc < j:
        if (xc,yc) in circulo:
                circulo[(xc,yc)] += 1
        else:
                circulo[(xc,yc)] = 0            
            
        #if xo >= 0 and yo >= 0 and xo < i and yo < j:
        if (xo,yo) in circulo:
                circulo[(xo,yo)] += 1
        else:
                circulo[(xo,yo)] = 0
        #print xc,yc,xo,yo
        #print circulo
        #print Gx,Gy,G

        #Se supone que circulo tiene los votos
        #de paso saco largo y ancho

    return circulo,largo,ancho
           
def main():
    t_inicial = time()

    im = Image.open('circulos.png')
    im.show()
    arr_rgb = array(im)
    (i,j) = (arr_rgb.shape[0],arr_rgb.shape[1])
    
    arr_gry = RGBtoGry(arr_rgb,i,j) #llamamos a RGB to Gray
    p_bordes = dict()
    p_bordes = convolucion(arr_gry,i,j,p_bordes) #llamamos a convolución

    #Tengo los bordes a este momento

    #Debo separarlos con un DFS
    objetos = DFS(p_bordes,i,j)
    #print objetos #imprimo para saber si el DFS jala

    #despues separarlos los analiso para encontrar sus centros...
    apuntan = dict()
    larg = dict()
    anch = dict()
    #print objetos
    for a in objetos:
        #para cada objeto hay direcciones (x,y)
        #los gradientes estan en los bordes
        apun,lar,anc = circulos(objetos[a],p_bordes)
        #devolvere una lista de direcciones con "votos"
        #donde apuntan ya sea al centro o hacia fuera
        apuntan[a] = apun
        larg[a] = lar
        anch[a] = anc
        if larg[a] == anch[a]:
            print 'objeto %d: es un circulo perfecto' % a
            print 'Largo, Ancho'
            print larg[a],anch[a]
            #Solo en ancho y alto, probabilidades del 25%
            #de que este indicador sea fiable

        else:
            print 'objeto %d: no es tan circular' % a
            print 'Largo, Ancho'
            print larg[a],anch[a]
        #incremento en a
        a += 1
    #print apuntan
    #creo nueva imagen para los circulos
    #apartir de este punto se invertira las x y y como y y x
    #gracias a PIL que se pelea con OpenCV
    n_img_c = Image.new("RGB", (j,i), (0,0,0))
    #draw = ImageDraw.Draw(n_img_c)
    
    #apunto = np.zeros(shape = (i,j,3))
    #print (i,j)
    pix = n_img_c.load()
    #Dibujamos los votos
    for a in apuntan:
        obj = apuntan[a]
        #print obj
        for (n,m) in obj:
        #x = n
        #y = m
        #print (x,y)
            if obj[n,m] > 0:
                if n>=0 and m>=0 and n<i and m<j:
                    pix[m,n] = 140,0,255
                    #votos mayores de 2 pueden ser centro
            else:
                if n>=0 and m>=0 and n<i and m<j:
                    pix[m,n] = 55,255,105
                #resulto que no es candidato a centro
        #coor_label = ((anch[a]/2)+7,(larg[a]/2))        
        #draw.text(coor_label,str(a),(0,0,255))
    n_img_c.show()
    #Dibujamos los bordes
    for (m,n) in p_bordes:
        pix[n,m] = 255,255,255      

    arr_out = array(n_img_c)
    cv.SaveImage("apunto.png",cv.fromarray(arr_out))
    im_apun = cv.LoadImage("apunto.png")
    cv.ShowImage('Votos XD',im_apun)
    
    #print p_bordes    

    t_final = time()
    t_total = t_final - t_inicial
    print "Tiempo de procesamiento: ",t_total

    cv.WaitKey(0)

if __name__ == '__main__':
    main()
