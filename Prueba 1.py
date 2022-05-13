import math
import random
from dwave.system import DWaveSampler, EmbeddingComposite
import dimod
import dwave.inspector
from true_hamiltoniano import m, n

N=n*n
v=[]
l=[]

arch=open("solucion.dat", "w")
for i in range(0,n):
    for j in range(0,n):
        l.append((-1)**(i+j))
    v.append(l)
    l=[]

for i in range (0,len(v)):
    for j in range(0,len(v[i])):
        arch.write(str(v[i][j]))
        arch.write('\n')
arch.close()

arch2=open("solucion.dat", "r")

lineas=arch2.readlines()
for i in lineas:
    if (i!="\n"):
        print(float(i))
        print("jsadok")
        print("asd")
