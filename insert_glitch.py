import moby2
from moby2.instruments import actpol
from moby2.scripting import get_filebase
import random
from moby2.tod import get_glitch_cuts
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

db = actpol.TODDatabase()
ids = db.select_tods()

c = 0
length_list = []
cut_index = []
magnitude_list = [10000,15000,20000,25000,30000,35000,40000,45000,50000]
efficiency_list = []

#Cycles through each magnitude, assigning a value for the efficiency of 
#get_glitch_cuts() of finding a signal of that magnitude
for n in magnitude_list:
    
    i = np.float32(n)
    tod_name = ids[2000].basename
    fb = get_filebase()
    tod_dir = fb.filename_from_name(tod_name, single = True)
    tod = moby2.scripting.get_tod({'filename':tod_dir, 'repair_pointing':True})
    
    #list of live detectors
    
    detected_cuts = 0
    total_cuts = 0
    #Cycles through detectors
    for d in range(0, 1055):
        
        t = int(random.random()*tod.nsamps)
        tod.data[d][t] += i
        
        glitches = get_glitch_cuts(data = tod.data, dets = np.arange(tod.data.shape[0]), tod = tod, params = { 'nSig': 10.0, 'tGlitch' : 0.005, 'minSeparation' : 30, 'maxGlitch' : 50000, 'highPassFc': 5.0, 'buffer' : 0})
        cuts = glitches.extract(0, tod.nsamps)
        
        total_cuts += 1
        length_array = len(cuts.cuts[d]) - 1
        #Cycles through all the cuts on a detector checking for our signal
        for s in range(0, length_array):            
            if cuts.cuts[d][s][0] <= t <= cuts.cuts[d][s][1]:
                length = cuts.cuts[d][s][1] - cuts.cuts[d][s][0]
                cut_index.append(c)
                c += 1
                length_list.append(length)
                print length
                print n
                print t
                detected_cuts += 1
        
    efficiency = float(detected_cuts) / total_cuts
    efficiency_list.append(efficiency)
plt.plot(magnitude_list, efficiency_list, 'ro')
plt.title('Efficiency vs. Magnitude')
plt.ylabel('Efficiency of Cut Collection')
plt.xlabel('Magnitude of Fake Signal')
plt.savefig('efficiency_vs_magnitude.png', bbox_inches = 'tight')

plt.plot(cut_index, length_list, 'ro')
plt.title('Lengths of cuts per detected signal')
plt.ylabel('Length of Cut')
plt.xlabel('Signal Index')
plt.savefig('length_of_cuts.png', bbox_inches = 'tight')
