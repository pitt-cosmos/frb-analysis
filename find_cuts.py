import moby2, json
import numpy as np
import sys
from moby2.instruments import actpol
from moby2.scripting import get_filebase
import cPickle as pickle

# Pickled tod list
with open("tods.pickle", "r") as f:
    tods = pickle.load(f)
print len(tods)

glitchp ={ 'nSig': 10, 'tGlitch' : 0.007, 'minSeparation': 30, 'maxGlitch': 50000, 'highPassFc': 6.0, 'buffer': 0 }

start = int(sys.argv[1])
end = int(sys.argv[2])

for n in range(start, end):
    try:
        tod_dir = tods[n]
        tod_name = tod_dir.split('/')[-1]
        print '[INFO] Looking at TOD:', tod_name
        data = moby2.scripting.get_tod({'filename': tod_dir, 'repair_pointing': True})
        print '[INFO] Get TOD successfully'
        # For the purpose of finding frb signals, it's partial glitch
        # signals that we should look at (unbuffered)

        # Define glitch parameters -> note buffer = 0
        # Test if detrend and remove_mean affect the tod
        #moby2.tod.remove_mean(data)
        #moby2.tod.detrend_tod(data) 
        cuts = moby2.tod.get_glitch_cuts(tod=data, params=glitchp)
        print "[INFO] Get cuts success"

        # Save into pickle file
        meta = {"TOD": tod_name, "glitch_param": glitchp, "cuts": cuts}
        pickle.dump(meta, open("outputs/cuts/" + str(n) + ".cut", "wb"), pickle.HIGHEST_PROTOCOL)
        print("File for TOD " + str(n) + " written successfully")
    except Exception as e:
        if type(e) == IOError:
            print("TOD " + str(n) + " has no cuts!")
        elif type(e) == TypeError:
            print("TOD " + str(n) + " file cannot be found!")
        else:
            print(e)
            print(type(e))
