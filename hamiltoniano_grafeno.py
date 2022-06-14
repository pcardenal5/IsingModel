import math
import random
from dwave.system import DWaveSampler, EmbeddingComposite
import dimod
import dwave.inspector

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

n=8
N=n*n
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
OnOff=0     #Controla si se hace o no la simulación en ordenador cuántico.
ann_time=20 #Tiempo, en microsegundos, que dura cada anneal
beta=.3    #Parámetro beta, inverso de la temperatura.



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
    k=0
    for i in range(0, n):
        #Índice de filas
        for j in range(0,n):
            #Índice de columnas
            J[(k-n)%N][k]=f(A,var)
            if()
        k=k+1
    #Para poder usar los coeficientes en la QPU debo transoformar h y J en diccionarios, b y Q respectivamente
    for i in range(0, n**2):
        b[i]=h[i]
        for j in range(0,i):
            if (J[i][j]!=0):
                a=(i,j)
                Q[a]=J[i][j]

    #Una vez los coeficientes QUBO podemos empezar la simulación del sistema.
    if (OnOff==1):
        bqm=dimod.binary.BinaryQuadraticModel.from_ising(b,Q)
        sampler = EmbeddingComposite(DWaveSampler(region="na-west-1", solver={'topology__type': 'chimera'}))

        sampleset = sampler.sample(bqm,num_reads=500,chain_strength=10.0, annealing_time=ann_time, beta = beta, postprocess = "sampling")

        dwave.inspector.show(sampleset)
        #solucion=sampleset.lowest(atol=0.1)
        arch=open("solucion.dat","w")
        contador=0
        for i in range(0,len(sampleset)):
            v=sampleset.record[i][0]
            x=sampleset.record[i][3]
            if(x<1/(n*n)):
                for j in range(0,len(v)):
                    arch.write(str(v[j])+" ")
                arch.write(str(sampleset.record[i][2])+"\n")
            else:
                print(x)
                contador=contador+1
        print(contador)
        arch.close()
        #for i in range(0,len(solucion)):
            #v=sampleset.data(fields=[''])
        #print(sampleset) 
        



    #print("sigma:", sigma)
    #print("J:")
    #for i in range(0,len(sigma)):
    #    print(J[i])
