import math
import random
from dwave.system import DWaveSampler, EmbeddingComposite
import dimod
import time
import dwave.inspector
from parametros import beta, betaf, beta_1, beta_2, beta_step_min, par, par_step

def f(a,s):
    random.seed()
    if (s!=0):
        return a*random.gauss(0,s)/(s*math.sqrt(2*math.pi))
    else:
        return a

def m(v):
    mag=0
    for i in range(0, len(v)):
        mag=mag+v[i]
    return mag

def g(x):
    k=0.3
    a=(10-2*math.sqrt(2))/(k*(k-2)+1)
    b=-2*a
    c=2*math.sqrt(2)+a
    return a*x*x+b*x+c

n=6
S=[]        #Espin 2d, matrix nxn
sigma=[]    #Espin 1d, vector n^2
J=[]        #Matriz de energías de interacción espin-espin
h=[]        #Vector con energía de campo magnético
Q={}        #Diccionario con los términos cuadraticos de Ising.
b={}        #Diccionario con los términos lineales de Ising
cQUBO={}    #Diccionario con los coeficientes QUBO
A=-1        #Intensidad de acoplamiento espin-espin. <0 favorece espines paralelos y >0 favorece antiparalelos
Ah=0        #Intensidad de acoplamiento espin-campo magnético
var=0       #Varianza de distribución de J. var=0 elimina la distribución y J toma siempre el mismo valor.
varh=0      #Varianza de distribución de h. var=0 elimina la distribución y J toma siempre el mismo valor.
OnOff=1     #Controla si se hace o no la simulación en ordenador cuántico.
ann_time=20 #Tiempo, en microsegundos, que dura cada anneal



if __name__=="__main__":
    #Creación de vectores de espin y matriz J
    k=0
    for i in range(0,n):
        l=[]
        for j in range(0,n):
            l.append(k)
            sigma.append(k)
            k=k+1
    for i in range (0, len(sigma)):
        l=[]
        for j in sigma:
            l.append(0)
        J.append(l)
        
    #Una vez creadas las matrices y vectores es hora de asignar las energías de interacción. Para ello, debemos traducir el sistema de 2D a uno de una
    #única dimension.
    k=-1
    for i in range(0, n):
        for j in range(0,n):
            k=k+1
            h.append(f(Ah,varh))
            J[(k + n) % (n*n)][k] = f(A,var)
            J[(k - n) % (n*n)][k] = f(A,var)
            J[k][(k + n) % (n*n)] = f(A,var)
            J[k][(k - n) % (n*n)] = f(A,var)
            if (j%2==1):
                if ((k+1)%n!=0):
                    if (i%2==1):
                        J[(k-1)%(n*n)][k]=f(A,var)
                        J[k][(k-1)%(n*n)]=f(A,var)
                    else:
                        J[(k+1)%(n*n)][k]=f(A,var)
                        J[k][(k+1)%(n*n)]=f(A,var)
                elif ((k+1)%n==0):
                    if (i%2==1):
                        J[(k-1)%(n*n)][k]=f(A,var)
                        J[k][(k-1)%(n*n)]=f(A,var)
                    elif (i%2==0):
                        J[(k+1-n)%(n*n)][k]=f(A,var)
                        J[k][(k+1-n)%(n*n)]=f(A,var)
    #Para poder usar los coeficientes en la QPU debo transoformar h y J en diccionarios, b y Q respectivamente
    for i in range(0, n**2):
        b[i]=h[i]
        for j in range(0,i):
            if (J[i][j]!=0):
                a=(i,j)
                Q[a]=J[i][j]

    #Una vez traducidos uso el recurso dimod.ising_to_qubo() para obtener los coeficientes QUBO del sistema.
    #cQUBO=dimod.ising_to_qubo(b,Q)


    #Una vez los coeficientes QUBO podemos empezar la simulación del sistema.
    bqm=dimod.binary.BinaryQuadraticModel.from_ising(b,Q)
    sampler = EmbeddingComposite(DWaveSampler(region="na-west-1", solver={'topology__type': 'chimera'}))
    B=[]
    M=[]
    E=[]
    num=1000
    while beta<betaf:
        if(beta<beta_1):
            ann_time=80
            beta=10**par
            par=par+par_step
        elif (beta>=beta_1 and beta<beta_2):
            ann_time=40
            beta_step=10*beta_step_min
            beta=beta+beta_step
        elif (beta>=beta_2):
            ann_time=20
            beta=beta+100*beta_step_min
        print(beta, time.thread_time())
        B.append(beta)
        sampleset = sampler.sample(bqm,num_reads=num, annealing_time=ann_time, beta = beta, postprocess = "sampling", label=str(beta))
        MAG=0
        ENG=0
        for i in range(0,len(sampleset)):
            v=sampleset.record[i][0]
            energia=sampleset.record[i][1]
            x=sampleset.record[i][2]
            MAG=MAG+abs(m(v))*x/num
            ENG=ENG+energia*x/num
        print(MAG/(n*n), ENG/(n*n))
        M.append(MAG/num)
        E.append(ENG/num)

    
    Enom="QAhexenergia"+str(n)+str(betaf)+str(abs(A))+".dat"
    Mnom="QAhexmagnetizacion"+str(n)+str(betaf)+str(abs(A))+".dat"
    fileE=open(Enom, "w")
    fileM=open(Mnom, "w")
    print(len(E),len(M),len(B))
    for b in range(0, len(B)):
        fileE.write(str(B[b])+" "+str(E[b])+"\n")
        fileM.write(str(B[b])+" "+str(M[b])+"\n")
    fileE.close()
    fileM.close()
    print("Terminado")

