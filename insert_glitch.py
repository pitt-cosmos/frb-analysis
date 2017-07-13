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

for n in [117]:

    i = 100000.0
    tod_name = ids[n].basename
    fb = get_filebase()
    tod_dir = fb.filename_from_name(tod_name, single = True)
    tod = moby2.scripting.get_tod({'filename':tod_dir, 'repair_pointing':True})
    
    #detector number, randomly assigned
    #x = int(random.random()*tod.data.shape[0])
    x = 33
    
    #time sample that is overwritten, randomly assigned
    y = int(random.random()*tod.nsamps)
    
    #This is fake glitch, randomly assigned to detector x on ctime y
    tod.data[x][y] += i
    
    #glitches = get_glitch_cuts(data = tod.data, dets = np.arange(tod.data.shape[0]), tod = tod,  params = { 'nSig': 10.0, 'tGlitch' : 0.002, 'minSeparaion': 30, 'maxGlitch': 50000, 'highPassFc': 5.0, 'buffer': 6 })
    
    print x
    print y
    print len(tod.ctime)
    
    plt.plot(tod.data[x])
    plt.title("Data for detector " + str(x) + " with spike at " + str(y) )
    plt.xlabel("time samples (2.5 ms)")
    plt.ylabel("Signal Intensity")
    #plt.xlim(0, len(tod.ctime))
    #plt.ylim(-20, 20)
    plt.show()
    plt.savefig('fake_signal.png', bbox_inches='tight')
