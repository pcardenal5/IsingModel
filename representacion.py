import numpy as np
import matplotlib.pyplot as plt
import math
from true_hamiltoniano import m, n
import random
import shelve


N=n*n
mag=0
random.seed()
v=[]            #Vector de variable aleatoria
V=[]            #Matriz de espines solución
for i in range (0,N):
    x=random.random()
    if (x>=0.55):
        v.append(1)
    else:
        v.append(-1)
arch=open("solucion.dat", "r")
lineas=arch.readlines()
v=[]
print(lineas)
for i in range(0,len(lineas)):
    if(lineas[i]=="5"):
        V.append(v)
        v=[]
    else:
        
        v.append(float(lineas[i]))
        

print(V)
#ax = plt.figure().add_subplot(projection='3d')
fig, ax2=plt.subplots()

s=0.00001
h=0
for i in range(0, n):
    for j in range(0,n):
        if (v[h]>0):
            colorines="red"
        else:
            colorines="blue"
        y=s*v[h]
        #ax.quiver(float(i), float(j), z, 0, 0, 0.25*v[h],color=colorines,  length=l, arrow_length_ratio=1, normalize=True)
        ax2.quiver(float(i), float(j),0,v[h],color=colorines, units="height", pivot="mid")
        h=h+1

print(v)
#ax.set_zlim(-1,1)
#ax.set_title("Modelo de Ising Bidimensional con magnetización m="+str(m(v)))
ax2.set_xlim(-1,n)
ax2.set_ylim(-1,n)
ax2.get_xaxis().set_visible(False)
ax2.get_yaxis().set_visible(False)

ax2.set_title("Modelo de Ising Bidimensional con magnetización m="+str(m(v)))




plt.show()
