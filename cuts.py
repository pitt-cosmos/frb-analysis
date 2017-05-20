import moby2, json
import numpy as np
from moby2.instruments import actpol
from moby2.scripting import get_filebase

#Objects that allow access to moby2 data. See .moby2 for details
db = actpol.TODDatabase()
ids = db.select_tods()
fb = moby2.scripting.get_filebase()

#The following will allow you to call specific TOD's from the database by adjusting
#the range on the for loop. This is also the first in a series of loops that will
#allow the script to pour over all the data for a given TOD (or all TOD's if you're crazy)
for n in range (0, 1):
    tod_name = ids[n].basename
    tod_dir = fb.filename_from_name(tod_name, single = True)
    data = moby2.scripting.get_tod({'filename': tod_dir, 'repair_pointing': True})
    cuts = moby2.scripting.gt_cuts({'depot':'/mnt/act3/users/lmaurin/depot','tag':
    'MR1_PA2_2014'},tod = data)
    
    #Labels the season for the sake of the dictionary, however THIS DOES NOT CHANGE
    #WHICH SEASON MOBY2 AND .CUTS USES. You have to manually change those in your
    #.moby2 script and which depot you use for "cuts" above or BAD THINGS HAPPEN 
    #(you may die...)
    season = "2014"
    
    #list that tores the numbers of all live detectors in a given TOD
    lds = cuts.get_uncut()
    
    #Empty dictionary and loop variables
    meta = {}
    ld = 0
    i = 0
    
    #The first loop that iterates through every cut in a live detector and appends
    #them to a list that will be added to "meta"
    for ld in lds:
        temp_list =[]
        cut = cuts.cuts[ld]
        while i < len(cut):
            #this next part calculates the time over which a cut was made
            calc = cuts.cuts[ld][i][1]-cuts.cuts[ld][i][0]
            #bound on the calculations to only append the cuts that are at the 
            #timescale you need. Note 1 unit=2.5 ms
            if calc < 4:
                temp_list.append(cuts.cuts[ld][i])
            i += 1
        a = temp_list.tolist()
        #Dictionary entry for detector "ld"
        meta[ld] = {
            'TOD' : str(n),
            'detector' : str(ld),
            'array' : str(ids[ld].array),
            'season' : season,
            'cuts' : a
        }
#Writes everything to a file. Depending on how many TOD's you chose, this will
#either be modest, or gargantuan in size. +1 internets if you run the whole shabang
s = json.dumps(meta)
with open("/mnt/act3/users/vjm126/test.txt", "w") as f:
    f.write(s)