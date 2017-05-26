import moby2, json
import numpy as np
from moby2.instruments import actpol
from moby2.scripting import get_filebase

#Objects that allow access to moby2 data. See .moby2 for details
db = actpol.TODDatabase()
ids = db.select_tods()
fb = moby2.scripting.get_filebase()

#Empty dictionary and loop variables
meta = {}
ld = 0
i = 0

#Season selection for the sake of the dictionary. However, this doesn't change
#the season in moby2 or the depot, so you'll have to change those as well both
#in moby2 and further in the code.
season = "2014"

#The outer loop iterates through every TOD while the inner loop iterates
#through every set of cuts in the n'th TOD. Not every TOD has cuts in the
#depot however, so it lets you know if one of the TODs cannot be analyzed in
#this way.
for n in range(0, len(ids)):
    tod_name = ids[n].basename
    tod_dir = fb.filename_from_name(tod_name, single = True)
    data = moby2.scripting.get_tod({'filename': tod_dir, 'repair_pointing': True})
    try: 
        cuts = moby2.scripting.get_cuts({'depot':'/mnt/act3/users/lmaurin/depot','tag':
        'MR1_PA2_2014'},tod = data)
    except IOError:
        print("TOD " + str(n) + " has no cuts!")
    #list that tores the numbers of all live detectors in a given TOD
    lds = cuts.get_uncut()      
    #The first loop that iterates through every cut in a live detector and appends
    #them to a list that will be added to "meta"

    for ld in lds:
        temp_list = np.empty((0))
        cut = cuts.cuts[ld]
        while i < cut.size/2:
            #this next part calculates the time over which a cut was made
            calc = cuts.cuts[ld][i][1]-cuts.cuts[ld][i][0]
            #bound on the calculations to only append the cuts that are at the 
            #timescale you need. Note 1 unit=2.5 ms
            if calc < 4:
                temp_list.append(cuts.cuts[ld][i])
            i += 1
        a = temp_list.tolist()
        #Dictionary entry for detector "ld"
        if temp_list != np.empty((0)):
            meta[n] = {
                'TOD' : str(n),
                'detector' : str(ld),
                'array' : str(ids[ld].array),
                'season' : season,
                'cuts' : a
            }
    #Writes everything to a file. Depending on how many TOD's you chose, this will
    #either be modest, or gargantuan in size. +1 internets if you run the whole shabang
    s = json.dumps(meta)
    with open("/mnt/act3/users/bjm126/" + str(n) + ".txt", "w") as f:
        f.write(s)
