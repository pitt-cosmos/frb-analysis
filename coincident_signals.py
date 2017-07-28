import moby2
import math
import cPickle
import numpy as np
ardata = moby2.scripting.get_array_data({'season':'2016', 'array_name':'AR3'})
cut_meta = cPickle.load(open("outputs/277.cut","rb"))
cuts = cut_meta['cuts']

first = lambda x: x[0]

def merge_cuts(cut1, cut2):
    '''
    input cuts have to be CutVector ttype 
    '''
    if len(cut1) == 0:
        return cut2
    if len(cut2) == 0:
        return cut1

    nsamps = max(cut1[-1][1], cut2[-1][1])
    c1m = cut1.get_mask(nsamps=nsamps)
    c2m = cut2.get_mask(nsamps=nsamps)
    cm = np.logical_or(c1m, c2m)
    merged = moby2.tod.CutsVector.from_mask(mask=cm)
    return merged
        
def common_cuts(cut1, cut2):
    '''
    Input cuts must be of CutVectors type
    '''

    if len(cut1) == 0:
        return cut1
    if len(cut2) == 0:
        return cut2
    nsamps = max(cut1[-1][1], cut2[-1][1])
    c1m = cut1.get_mask(nsamps=nsamps)
    c2m = cut2.get_mask(nsamps=nsamps)
    cm = np.logical_and(c1m, c2m)
    common = moby2.tod.CutsVector.from_mask(mask=cm)
    return common

# Understand the structure of the array_data
'''
for i in range(1055):
    print ardata['row'][i], ardata['col'][i], ardata['nom_freq'][i], ardata['array_x'][i], ardata['array_y'][i]
'''

# Get a unique list of lixels
pixel_indexes = [index for index in range(1056) if math.floor(index / 32)%4 ==0 and math.floor(index/32)<32]

# Check if the pixels_indexes are correct
'''
for i in pixel_indexes: 
    print ardata['row'][i], ardata['col'][i], ardata['nom_freq'][i], ardata['array_x'][i], ardata['array_y'][i], ardata['det_type'][i]
'''
for i in pixel_indexes:
    print '[INFO] Looking at pixel %d ' % i
    det_f90 = []
    det_f150 = []
    has_f90 = True
    has_f150 = True
    for det in [i, i+32]:
        if ardata['det_type'][det] == 'tes':
            det_f90.append(det)

    for det in [i+64, i+96]:
        if ardata['det_type'][det] == 'tes':
            det_f150.append(det)

    # Merge cuts at two polarization detectors of f90
    if len(det_f90) == 2:
        cuts_A = cuts.cuts[det_f90[0]]
        cuts_B = cuts.cuts[det_f90[1]]
        cuts_f90 = merge_cuts(cuts_A, cuts_B)
            
    elif len(det_f90) == 1:
        cuts_f90 = cuts.cuts[det_f90[0]]
            
    else:
        cuts_f90 = None
        has_f90 = False

    # Merge cuts at two polarization detectors of f150
    if len(det_f150) == 2:
        cuts_A = cuts.cuts[det_f150[0]]
        cuts_B = cuts.cuts[det_f150[1]]
        cuts_f150 = merge_cuts(cuts_A, cuts_B)
        
    elif len(det_f150) == 1:
        cuts_f150 = cuts.cuts[det_f150[0]]
        
    else:
        cuts_f150 = None
        has_f150 = False
    
    if has_f90 and has_f150:
        print common_cuts(cuts_f90, cuts_f150)
