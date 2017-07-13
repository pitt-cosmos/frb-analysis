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
TOD = 117
DET = 33

# Plot
tod = ids[TOD]
tod_name = tod.basename
print tod_name
tod_dir = fb.filename_from_name(tod_name, single=True)
# The role of repair pointing is not sure
data =moby2.scripting.get_tod({'filename':tod_dir, 'repair_pointing': True})
print data.nsamps
#plt.plot(data.ctime, data.data[DET])
plt.plot(data.data[DET])
plt.show()
