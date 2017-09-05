import moby2, cPickle
import numpy as np
from moby2.instruments import actpol
from moby2.scripting import get_filebase

db = actpol.TODDatabase()
ids = db.select_tods()
fb = get_filebase()

meta = {}
n = 0
ardata = moby2.scripting.get_array_dta({'season':'2016', 'array_name': 'AR3'})

glitchp = {'nSig':10, 'tGlitch':0.007, 'minSeparation': 30, 'maxGlitch': 50000,
    'highPassFc': 6.0, 'buffer':0}

for n in range(0, len(ids)):
    try:
        tod_name = ids[n].basename
        print(str(n) + ': ' + tod_name)
        tod_dir = fb.filename_from_name(tod_name, single = True)
        print("Get TOD dir success")
        data = moby2.scripting.get_tod({'filename':tod_dir, 'repair_pointing': True})
        print("Get TOD success")
        
        cuts = moby2.tod.get_glitch_cuts(tod = data, params = glitchp)
        print("Get cuts success")
        
        print("Generating list of cuts")
        
        for det in range(0,1055):
            cut_array = np.empty((0))
            cut = cuts.cuts[det]
            i = 0
            while i < len(cut):
                calc = cuts.cuts[det][i][1]-cuts.cuts[det][i][0]
                
                if calc <= 20:
                    cut_array = np.append(cut_array, [cuts.cuts[det][i]])
                i +=1
                
            a = cut_array.reshape((len(cut_array)/2, 2)).tolist()
            pol_family = ardata['pol_family']
            nom_freq = ardata['nom_freq']
            if cut_array != np.empty((0)):
                meta[det] = {
                    'det_id' : det,
                    'cuts' : a,
                    'freq_channel' : nom_freq[det],
                    'pol_channel' : pol_family[det],
                    'TOD_name' : tod_name
                }
        with open("outputs/" + str(n) + ".txt", "wb") as f:
            cPickle.dump(meta, fb)
        print("File for TOD " + str(n) + " written successfully")
    except Exception as e:
        if type(e) == IOError:
            print("TOD " + str(n) + " has no cuts!")
        if type(e) == TypeError:
            print("TOD " + str(n) + " file cannot be found!")
        else:
            print(e)
            print(type(e))
