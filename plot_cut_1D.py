import pickle
from itertools import izip_longest
import os
import numpy as np
from matplotlib import pyplot as plt

INPUTDIR = "cuts_fixed_detector"
data_files = os.listdir(INPUTDIR)
data_files.sort()

# Stack histogram to form combined histogram
cut_hist = [0]
counter = 0
for data in data_files[:1000]:
    counter += 1
    print "[INFO] Filling %d histogram ... " % counter
    with open(os.path.join(INPUTDIR, data), "rb") as f:
        temp_hist = pickle.load(f)
        cut_hist = [x+y for x,y in izip_longest(cut_hist, temp_hist, fillvalue=0)]

fig, ax = plt.subplots()
ax.bar(np.arange(1, len(cut_hist)+1)[:100], cut_hist[:100], color='red')
ax.set_title('Number of cuts that affect a fixed number of detectors (AR1)')
ax.set_ylabel('Number of cuts')
ax.set_xlabel('Number of detectors affected')
plt.savefig('cuts_fixed_detector_hist.png', bbox_inches='tight')
plt.show()
