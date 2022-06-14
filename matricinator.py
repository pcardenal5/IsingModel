def f(a,var):
    return 1

n=2
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

for i in range(0,len(J)):
    print(J[i])
