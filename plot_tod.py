import moby2
from moby2.instruments import actpol
from moby2.scripting import get_filebase
import matplotlib
matplotlib.use('GTKAgg') # This is necessary to show plots over ssh
import matplotlib.pyplot as plt


# Initialization
db = actpol.TODDatabase()
ids = db.select_tods()
fb = get_filebase()

# Selection
#TOD = 117
TOD = 8162

# Plot TOD
tod = ids[TOD]
tod_name = tod.basename
tod_dir = fb.filename_from_name(tod_name, single=True)

data =moby2.scripting.get_tod({'filename':tod_dir, 'repair_pointing': True})
for i in range(len(data.data)):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(data.ctime[10000:11000], data.data[i][10000:11000])
    fig.savefig('outputs/plot_tod/' + str(i) + '.png')
    print "[INFO] %d saved" % i


'''
# Plot cuts together with TOD
glitchp ={ 'nSig': 10, 'tGlitch' : 0.007, 'minSeparation': 30, 'maxGlitch': 50000, 'highPassFc': 6.0, 'buffer': 0 }

#cuts = moby2.tod.get_glitch_cuts(tod=data, params=glitchp)
#cuts = moby2.tod.get_mce_cuts(data)
cuts = moby2.scripting.get_cuts({'depot':'/mnt/act3/users/lmaurin/depot', 'tag':'MR1_PA2_2014'},tod=data)
_mask = cuts.cuts[DET].get_mask()
print cuts.get_cut()
plt.plot(data.ctime[_mask], data.data[DET][_mask], 'r-')
plt.plot(data.data[DET][~_mask], 'r-')
plt.show()
'''
