import cPickle
from matplotlib.colors import LogNorm
import glob
import matplotlib
matplotlib.use('GTKAgg')
from matplotlib import pyplot as plt
import numpy as np
from pixels import PixelReader
from mpl_toolkits.mplot3d import Axes3D


scatter = []
files =glob.glob("outputs/hotmap/*.tmp")
fCounter = 0
for f in files:
    fCounter += 1
    with open(f, "rb") as _f:
        if fCounter == 1: #first file
            hotmap = cPickle.load(_f)
        else:
            next_hotmap = cPickle.load(_f)
            for key in next_hotmap:
                hotmap[key] += next_hotmap[key]
    print '[INFO] Number of files processed:', fCounter
        
print hotmap

pr = PixelReader()

# Added some filtering
filtering = 1000000
x = [pr.getX(int(key)) for key in hotmap if hotmap[key]<filtering]
y = [pr.getY(int(key)) for key in hotmap if hotmap[key]<filtering]
z = [hotmap[key] for key in hotmap if hotmap[key]<filtering]

# Generate filtered list
filtered_key = [key for key in hotmap if hotmap[key]<filtering]
with open("good_pixel_list.pickle", "wb") as f:
    cPickle.dump(filtered_key, f)

fig =plt.figure()
ax = Axes3D(fig)

ax.scatter(x, y, z)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("Total Cut Time")
plt.show()

#plt.hist2d(np.log(x)/np.log(10), y, bins=[40,40], norm=LogNorm())
#plt.colorbar()
#plt.xscale('log')
#plt.xlabel("Coincident Signal Duration (sampling points)")
#plt.ylabel("Number of Pixels Affected")
#plt.show()
