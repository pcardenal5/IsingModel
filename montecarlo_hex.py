# coding=utf-8
import math
import random
import time
from parametros import beta, betaf, beta_1, beta_2, beta_step_min, par, par_step

def m(v):
    mag=0
    for i in range(0, len(v)):
        mag=mag+v[i]
    return mag

def energuia(S,J):
    n=len(S)
    E=0
    for i in range(0,n):
        for j in range(i,n):
            if (j%2==1):
                if (i%2==1):
                    E=E+J*S[i][j]*(S[i][(j+1)%n]+S[i][(j-1)%n]+S[(i-1)%n][j])
                else:
                    E=E+J*S[i][j]*(S[i][(j+1)%n]+S[i][(j-1)%n]+S[(i-1)%n][j])
            
    return -E

def mag(S):
    m=0
    for i in range (0,len(S)):
        for j in range(0,len(S)):
            m=m+S[i][j]
    return m

def sistema(n):
    import random
    S=[]
    random.seed()
    for  i in range(0,n):
        v=[]
        for j in range (0,n):
            x=random.random()
            if(x>0.5):
                v.append(1)
            else:
                v.append(-1)
        S.append(v)
    return S

B=[]
M=[]
E=[]
random.seed()
num_iter=10000
J=0.5
N=6
termal=2000*N
if termal < 5000:
    termal = 5000
while beta<beta_2:
    if(beta<beta_1):
        beta=10**par
        par=par+par_step
    elif (beta>=beta_1):
        beta_step=beta_step_min
        beta=beta+beta_step
    print(beta, time.thread_time())
    B.append(beta)
    P=[]
    P.append(math.exp(-2*J*beta))
    P.append(-6*J*beta)
    MAG=0
    ENG=0
    for j in range(0, num_iter):
        S=sistema(N)
        if (j%1000==0):
            print(j)
        for t in range(0,termal):
            x=int(math.floor(N*random.random()))
            y=int(math.floor(N*random.random()))
            if (y%2==1):
                if (x%2==1):
                    dE=2*J*S[x][y]*(S[x][(y+1)%N]+S[x][(y-1)%N]+S[(x-1)%N][y])
                else:
                    dE=2*J*S[x][y]*(S[x][(y+1)%N]+S[x][(y-1)%N]+S[(x+1)%N][y])
            else:
                if (x%2==1):
                    dE=2*J*S[x][y]*(S[x][(y+1)%N]+S[x][(y-1)%N]+S[(x+1)%N][y])
                else:
                    dE=2*J*S[x][y]*(S[x][(y+1)%N]+S[x][(y-1)%N]+S[(x-1)%N][y])
            if (dE<=0):
                S[x][y]=-S[x][y]
            else:
                p=P[int((dE-2)/(4*J))]
                q=random.random()
                if (q<p):
                    S[x][y]=-S[x][y]
        MAG=MAG+abs(mag(S))/(N*N)
        ENG=ENG+energuia(S,J)/(N*N)
    print(MAG/num_iter, ENG/num_iter)
    M.append(MAG/num_iter)
    E.append(ENG/num_iter)

while beta<betaf:
    beta=beta+beta_step_min
    print(beta, time.thread_time())
    B.append(beta)
    P=[]
    P.append(math.exp(-2*J*beta))
    P.append(-6*J*beta)
    MAG=0
    ENG=0
    for j in range(0, num_iter):
        if (j%1000==0):
            S=sistema(N)
            print(j)
        for t in range(0,termal):
            x=int(math.floor(N*random.random()))
            y=int(math.floor(N*random.random()))
            if (y%2==1):
                if (x%2==1):
                    dE=2*J*S[x][y]*(S[x][(y+1)%N]+S[x][(y-1)%N]+S[(x-1)%N][y])
                else:
                    dE=2*J*S[x][y]*(S[x][(y+1)%N]+S[x][(y-1)%N]+S[(x+1)%N][y])
            else:
                if (x%2==1):
                    dE=2*J*S[x][y]*(S[x][(y+1)%N]+S[x][(y-1)%N]+S[(x+1)%N][y])
                else:
                    dE=2*J*S[x][y]*(S[x][(y+1)%N]+S[x][(y-1)%N]+S[(x-1)%N][y])
            if (dE<=0):
                S[x][y]=-S[x][y]
            else:
                p=P[int((dE-2)/(4*J))]
                q=random.random()
                if (q<p):
                    S[x][y]=-S[x][y]
        MAG=MAG+abs(mag(S))/(N*N)
        ENG=ENG+energuia(S,J)/(N*N)
    print(MAG/num_iter, ENG/num_iter)
    M.append(MAG/num_iter)
    E.append(ENG/num_iter)

Enom="hexenergia"+str(N)+str(betaf)+str(J)+".dat"
Mnom="hexmagnetizacion"+str(N)+str(betaf)+str(J)+".dat"
fileE=open(Enom, "w")
fileM=open(Mnom, "w")
print(len(E),len(M),len(B))
for b in range(0, len(B)):
    fileE.write(str(B[b])+" "+str(E[b])+"\n")
    fileM.write(str(B[b])+" "+str(M[b])+"\n")
fileE.close()
fileM.close()
print("Terminado")
