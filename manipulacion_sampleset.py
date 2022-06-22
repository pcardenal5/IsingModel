import math
import numpy as np
import random
import dimod
from true_hamiltoniano import n, m

X=np.loadtxt("solucion.dat", delimiter=" ")

M=0
total=0
for i in range(0,len(X)):
    v=[]
    for j in range(0, len(X[i])-1):
        v.append(X[i][j])
    total=total+X[i][n*n]
    M=M+abs(m(v))
print(M, M/(n*n*total))

