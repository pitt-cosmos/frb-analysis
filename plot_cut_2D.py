import pickle
from itertools import izip_longest
import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

INPUTDIR = "outputs/plot_cuts_hist/"
data_files = os.listdir(INPUTDIR)
data_files.sort()

# Stack histogram to form combined histogram
counter = 0
for data in data_files[:1000]:
    counter += 1
    print "[INFO] Filling %d histogram ... " % counter

    if counter == 1: #first file
        with open(os.path.join(INPUTDIR, data), "rb") as f:
            cut_hist = pickle.load(f)
    else:
        with open(os.path.join(INPUTDIR, data), "rb") as f:
            temp_cut_hist = pickle.load(f)
            cut_hist = np.concatenate((cut_hist, temp_cut_hist), axis=0)

# Filter
cut_hist = cut_hist[cut_hist[:,1]<400]
cut_hist = cut_hist[cut_hist[:,0]<40]
cut_count = [cut_hist[cut_hist[:,0]==i][:,1].mean() for i in range(40)]
#cut_hist = cut_hist[cut_hist[:,0]>1]
            
# Make two subplots: 1 - 2D, 1 - 1D
#fig, axs = plt.subplots(2,1, sharex=True)
fig, axs = plt.subplots(3,1, sharex=True)

# Upper plot
axs[0].hist2d(cut_hist[:,0], cut_hist[:,1],bins=(40, 100), norm=colors.LogNorm())
axs[0].set_ylabel("Length of cuts")
#axs[0].scatter(cut_hist[:,0], cut_hist[:,1],s=0.1)
axs[1].plot(cut_count)
axs[1].set_ylabel("Mean length of cuts")

axs[2].hist(cut_hist[:,0], bins=40)
axs[2].set_ylabel("Number of cuts")
axs[2].set_xlabel("Number of detectors affected")
plt.tight_layout()

#axs[1].bar(np.arange(1, len(cut_hist[:,0])+1), len(cut_hist[:,0]), color='red')
#axs.set_title('Number of cuts that affect a fixed number of detectors (AR1)')
#ax.set_ylabel('Number of cuts')
#ax.set_xlabel('Number of detectors affected')
#plt.savefig('hist_cuts_2D_ave.png', bbox_inches='tight')

plt.show()
