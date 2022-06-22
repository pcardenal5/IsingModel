import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import math

N=6

fig,ax=plt.subplots()
X, Y = np.loadtxt('magnetizacion71.1.dat', delimiter=' ', unpack=True)
y1=[]
y2=[]
for i in range(0, len(X)):
    y1.append(1/N)
    y2.append(1/N)

x=X
y=Y
ax.plot(x,y)
X, Y = np.loadtxt('magnetizacion72.dat', delimiter=' ', unpack=True)
ax.plot(X,Y)

intervals=x[len(x)-1]-x[0]
intervals=int(10*intervals)/100
loc = plticker.MultipleLocator(base=intervals)

ax.xaxis.set_major_locator(loc)

ax.grid(which='major', axis='both', linestyle='-')

plt.xlim([x[0], 1])
plt.ylim(0,1.1)


ax.grid(visible=True, which="major")
#plt.xlim([-10,10])

plt.show()
