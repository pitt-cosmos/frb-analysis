import moby2, json
import numpy as np
import sys
from moby2.instruments import actpol
from moby2.scripting import get_filebase
import cPickle as pickle

#Objects that allow access to moby2 data. See .moby2 for details
db = actpol.TODDatabase()
ids = db.select_tods()
fb = moby2.scripting.get_filebase()


glitchp ={ 'nSig': 10, 'tGlitch' : 0.007, 'minSeparation': 30, 'maxGlitch': 50000, 'highPassFc': 6.0, 'buffer': 0 }
#The outer loop iterates through every TOD while the inner loop iterates
#through every set of cuts in the n'th TOD. Not every TOD has cuts in the
#depot however, so it lets you know if one of the TODs cannot be analyzed in
#this way.
#for n in range(0, len(ids)):
#+Contro the start and end with commandline arguments for convenence
start = int(sys.argv[1])
end = int(sys.argv[2])
for n in range(start, end):
    try:
        tod_name = ids[n].basename
        array = ids[n].array
        print(str(n) + ': ' + tod_name)
        tod_dir = fb.filename_from_name(tod_name, single = True)
        print("Get TOD dir success")
        data = moby2.scripting.get_tod({'filename': tod_dir, 'repair_pointing': True})
        print("Get TOD success")
        # For the purpose of finding frb signals, it's partial glitch
        # signals that we should look at (unbuffered)

        # Define glitch parameters -> note buffer = 0
        cuts = moby2.tod.get_glitch_cuts(tod=data, params=glitchp)
        print("Get cuts success")

        # Save into pickle file
        meta = {"array": array, "TOD": tod_name, "glitch_param": glitchp, "cuts": cuts}
        pickle.dump(meta, open("outputs/" + str(n) + ".pickle", "wb"), pickle.HIGHEST_PROTOCOL)
        print("File for TOD " + str(n) + " written successfully")
    except Exception as e:
        if type(e) == IOError:
            print("TOD " + str(n) + " has no cuts!")
        elif type(e) == TypeError:
            print("TOD " + str(n) + " file cannot be found!")
        else:
            print(e)
            print(type(e))
