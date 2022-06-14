import numpy as np
import matplotlib.pyplot as plt
import math

N=10
X, Y = np.loadtxt('magnetizacion2.dat', delimiter=' ', unpack=True)
y1=[]
y2=[]
for i in range(0, len(X)):
    y1.append(1/N)
    y2.append(2/N)

x=1/X
plt.plot(x,1/Y)
plt.plot(x,y1)
plt.plot(x,y2)



plt.xlim([0, 40])
#plt.xlim([-10,10])

plt.show()
