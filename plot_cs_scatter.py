import cPickle
from matplotlib.colors import LogNorm
import glob
import matplotlib
matplotlib.use('GTKAgg')
from matplotlib import pyplot as plt
import numpy as np

scatter = []
#files =glob.glob("outputs/plot_cs_scatter/*.tmp")

# For filtered plot
files =glob.glob("outputs/plot_cs_scatter_filter/*.tmp")
fCounter = 0
for f in files:
    fCounter += 1
    with open(f, "rb") as _f:
        scatter.extend(cPickle.load(_f))
    print '[INFO] Number of files processed:', fCounter
        
#print scatter
x = [item[0] for item in scatter]
y = [item[1] for item in scatter]

#plt.scatter(np.log(x), y)
plt.hist2d(np.log(x)/np.log(10), y, bins=[40,40], norm=LogNorm())
plt.colorbar()
#plt.xscale('log')
plt.xlabel("Coincident Signal Duration (sampling points)")
plt.ylabel("Number of Pixels Affected")
plt.show()
