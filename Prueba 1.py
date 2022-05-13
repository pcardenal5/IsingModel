import math
import random
from dwave.system import DWaveSampler, EmbeddingComposite
import dimod
import dwave.inspector
from true_hamiltoniano import solucion, m

for i in range(0,len(solucion)):
    v=solucion.record[i][0]
    print(v, m(v))
