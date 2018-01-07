import moby2
from moby2.instruments import actpol
from moby2.scripting import get_filebase
import random
from moby2.tod import get_glitch_cuts
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from math import pow as p
import pickle

db = actpol.TODDatabase()
ids = db.select_tods()


#magnitude_list = [4,5,6,7,8]
magnitude_list = np.linspace(5000, 50000, 20)
efficiency_list = []
length_list = []
cut_index = [] 

for n in magnitude_list:
    print "[INFO] working on magnitude %d " % n
    
    #sig = np.float32(p(10, n))
    sig = n
    tod_name = ids[2000].basename
    fb = get_filebase()
    tod_dir = fb.filename_from_name(tod_name, single = True)
    tod = moby2.scripting.get_tod({'filename':tod_dir, 'repair_pointing':True})
    total_insertions = 0
    detected_insertions = 0
    fake_signals = [None]*1024 # empty array to store fake signals
                               # only for one glitch per detector
    print "[INFO] filling fake signals ... "
    for d in range(0, 1024):
        t = int(random.random()*tod.nsamps)
        tod.data[d][t] += sig
        fake_signals[d] = t
        total_insertions += 1

    print "[INFO] detecting fake signals ... "
    glitches = get_glitch_cuts(data = tod.data, dets = np.arange(tod.data.shape[0]), tod = tod, params = { 'nSig': 10.0, 'tGlitch' : 0.002, 'minSeparation' : 40, 'maxGlitch' : 50000, 'highPassFc': 5.0, 'buffer' : 0})
    cuts = glitches.extract(0, tod.nsamps)  
    #length_array = len(cuts.cuts[d]) - 1
    for i, t in enumerate(fake_signals):
        for cut in cuts.cuts[i]:
            length = cut[1] - cut[0]
	    if cut[0] <= t <= cut[1] and length <= 20:
	        #cut_index.append(c)
                detected_insertions += 1
                #length_list.append(length)
    print '[INFO] detected: %d, all: %d' % (detected_insertions, total_insertions)
    efficiency = float(detected_insertions) / total_insertions
    
    efficiency_list.append(efficiency)
result = {
    "efficiency": efficiency_list,
    "magnitude": magnitude_list
}

#plt.subplot(221)
#plt.plot(magnitude_list, efficiency_list, 'r-')
#plt.title('Efficiency vs. Magnitude')
#plt.ylabel('Efficiency of Cut Collection')
#plt.xlabel('Magnitude of Fake Signal')

#plt.subplot(222)
#plt.plot(cut_index, length_list, 'ro')
#plt.title('Cut lengths per detection')
#plt.ylabel('Length of Cut')
#plt.xlabel('Successful cut')

#plt.savefig('fake_glitch_stats2.png')
pickle.dump(result, open("minSep=40.p", "wb"))
