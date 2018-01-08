import cPickle
from matplotlib.colors import LogNorm
import glob
import matplotlib
matplotlib.use('GTKAgg')
from matplotlib import pyplot as plt
import numpy as np

total = []
#files =glob.glob("outputs/plot_cs_scatter/*.tmp")

# For filtered plot
files =glob.glob("outputs/plot_ns_scatter_v2/*.tmp")
fCounter = 0
for f in files:
    fCounter += 1
    with open(f, "rb") as _f:
        total.append(len(cPickle.load(_f)))
    print '[INFO] Number of files processed:', fCounter
        
bins = np.linspace(0, 10, 5)
plt.hist(total,bins)
plt.show()
