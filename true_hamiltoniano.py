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

n=5
S=[]        #Espin 2d, matrix nxn
sigma=[]    #Espin 1d, vector n^2
J=[]        #Matriz de energías de interacción espin-espin
h=[]        #Vector con energía de campo magnético
Q={}        #Diccionario con los términos cuadraticos de Ising.
b={}        #Diccionario con los términos lineales de Ising
cQUBO={}    #Diccionario con los coeficientes QUBO
A=1         #Intensidad de acoplamiento espin-espin
Ah=1        #Intensidad de acoplamiento espin-campo magnético
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
    k=0
    for k in range(0,n**2):
        h.append(f(Ah,varh))
        if ((k+1)%n!=0 and k%n!=0):
            J[(k + 1) % n ** 2][k] = f(A,var)
            J[(k - 1) % n ** 2][k] = f(A,var)
            J[k][(k + n) % n ** 2] = f(A,var)
            J[k][(k - n) % n ** 2] = f(A,var)
        elif((k+1)%n==0):
            J[(k + 1-n) % n ** 2][k] = f(A,var)
            J[(k - 1) % n ** 2][k] = f(A,var)
            J[k][(k + n) % n ** 2] = f(A,var)
            J[k][(k - n) % n ** 2] = f(A,var)
        elif (k%n==0):
            J[(k + 1) % n ** 2][k] = f(A,var)
            J[(k - 1 + n) % n ** 2][k] = f(A,var)
            J[k][(k + n) % n ** 2] = f(A,var)
            J[k][(k - n) % n ** 2] = f(A,var)
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
    if (OnOff==1):
        bqm=dimod.binary.BinaryQuadraticModel.from_ising(b,Q)
        sampler = EmbeddingComposite(DWaveSampler(solver={'topology_type':'chimera'}))

        sampleset = sampler.sample(bqm,num_reads=500, annealing_time=ann_time)

        #dwave.inspector.show(sampleset)
        #solucion=sampleset.lowest(atol=0.1)
        arch=open("solucion.dat","w")
        for i in range(0,len(sampleset)):
            v=sampleset.record[i][0]
            for j in range(0,len(v)):
                arch.write(str(v[j]))
                arch.write("\n")
            arch.write("5")
            arch.write("\n")
        arch.close()
        #for i in range(0,len(solucion)):
            #v=sampleset.data(fields=[''])
        #print(sampleset) 
        



    #print("sigma:", sigma)
    #print("J:")
    #for i in range(0,len(sigma)):
    #    print(J[i])
