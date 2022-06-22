def f(a,var):
    return 1

n=4
m=n*n
S=[]        #Espin 2d, matrix nxn
sigma=[]    #Espin 1d, vector n^2
J=[]        #Matriz de energías de interacción espin-espin para redes cuadradas
H=[]        #Matriz de energías de interacción espin-espin para redes hexagonales
A=-1        #Intensidad de acoplamiento espin-espin. <0 favorece espines paralelos y >0 favorece antiparalelos
var=0       #Varianza de distribución de J. var=0 elimina la distribución y J toma siempre el mismo valor.


if __name__=="__main__":
    #Creación de vectores de espin y matriz J
    k=0
    for i in range(0,n):
        l=[]
        h=[]
        for j in range(0,n):
            l.append(k)
            sigma.append(k)
            k=k+1
    for i in range (0, len(sigma)):
        l=[]
        h=[]
        for j in sigma:
            l.append(0)
            h.append(k)
        J.append(l)
        H.append(l)
    #Una vez creadas las matrices y vectores es hora de asignar las energías de interacción. Para ello, debemos traducir el sistema de 2D a uno de una
    #única dimension.
    k=0
    lol=1
    if (lol==2):
        for k in range(0,n**2):
            J[(k + n) % m][k] = f(A,var)
            J[(k - n) % m][k] = f(A,var)
            if ((k+1)%n!=0 and k%n!=0):
                J[(k + 1) % m][k] = f(A,var)
                J[(k - 1) % m][k] = f(A,var)
            elif((k+1)%n==0):
                J[(k + 1-n) % m][k] = f(A,var)
                J[(k - 1) % m][k] = f(A,var)
            elif (k%n==0):
                J[(k + 1) % m][k] = f(A,var)
                J[(k - 1 + n) % m][k] = f(A,var)
    k=-1
    m=n*n
    for i in range(0, n):
        for j in range(0,n):
            k=k+1
            H[(k + n) % m][k] = f(A,var)
            H[(k - n) % m][k] = f(A,var)
            H[k][(k + n) % m] = f(A,var)
            H[k][(k - n) % m] = f(A,var)
            print(k,(k+n)%m,(k-n)%m)
            if (j%2==1):
                print ("Jota", j,k)
                if ((k+1)%n!=0):
                    print("ka int", k)
                    if (i%2==1):
                        print(k,"-", (k-1)%m)
                        H[(k-1)%m][k]=f(A,var)
                        H[k][(k-1)%m]=f(A,var)
                    else:
                        print(k,"+", (k+1)%m)
                        H[(k+1)%m][k]=f(A,var)
                        H[k][(k+1)%m]=f(A,var)
                elif ((k+1)%n==0):
                    print("ka bor", k)
                    if (i%2==1):
                        print(k,"-", (k-1)%m)
                        H[(k-1)%m][k]=f(A,var)
                        H[k][(k-1)%m]=f(A,var)
                    elif (i%2==0):
                        print(k,"+", (k+1-n)%m)
                        H[(k+1-n)%m][k]=f(A,var)
                        H[k][(k+1-n)%m]=f(A,var)

lol=1
if (lol==1):
    for i in range(0,len(H)):
        for j in range(0, len(H[i])):
            if(H[i][j]!=H[j][i]):
                print("Adasdhgalsdfuba")
        print(H[i])
