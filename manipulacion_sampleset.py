import math
import numpy as np
import random
import dimod
from QA_barrido_cuadrada import m

X=np.loadtxt("QAsolucion71e-071.dat", delimiter=" ")

n=7
M=0
total=0
for i in range(0,len(X)):
    v=[]
    for j in range(0, len(X[i])-1):
        v.append(X[i][j])
    total=total+X[i][n*n]
    M=M+abs(m(v))
print(M, M/(n*n*total))

