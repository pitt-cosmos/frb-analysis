'''
This script tries to generate a hotmap of the pixels
A hot map of pixels is a dictionary of pixels with
the number of cuts each pixel has as the value
The output of this script can be stacked together 
by another script and generate a heatmap across 
a large number of tods
'''

import moby2
import math
import cPickle
import numpy as np
#import matplotlib
#matplotlib.use('GTKAgg')
from pixels import PixelReader
#from matplotlib import pyplot as plt
import sys


# Utility function
first = lambda x: x[0]

def merge_cuts(cut1, cut2):
    '''
    input cuts have to be CutVector type 
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

# =============
# Main program
# =============

# Getting array data
ardata = moby2.scripting.get_array_data({'season':'2016', 'array_name':'AR3'})

# Get the cut index ( or TOD index ) that we want to work with 
cut_no = sys.argv[1]

print 'Loading cut:', cut_no
cuts_data = cPickle.load(open("outputs/cuts/"+cut_no+".cut","rb"))
cuts = cuts_data['cuts']

print cuts_data

# Load pixel database
pr = PixelReader()
pixels = pr.getPixels()

# Get nsamples
nsamps = max([cut[-1][1] for cut in cuts.cuts if len(cut)!=0])
first = True
hotmap = {} # a dictionary to store the total number of cuts of each pixel

# Loop through all pixels
for p in pixels:
    # for simplicity, let's look at one frequency channel and one polarization channel 
    det_f90 = []
    det_f150 = []
    has_f90 = True
    has_f150 = True
    for det in pr.getF90(p):
        if ardata['det_type'][det] == 'tes':
            det_f90.append(det)

    for det in pr.getF150(p):
        if ardata['det_type'][det] == 'tes':
            det_f150.append(det)

    # Merge cuts at two polarization detectors of f90
    if len(det_f90) == 2:
        cuts_A = cuts.cuts[det_f90[0]]
        cuts_B = cuts.cuts[det_f90[1]]
        #cuts_f90 = merge_cuts(cuts_A, cuts_B) #Look at polarized spike that may appera at either pol
        cuts_f90 = common_cuts(cuts_A, cuts_B) #Only look at unpolarized spike that appear at both pols

    elif len(det_f90) == 1:
        cuts_f90 = cuts.cuts[det_f90[0]]
            
    else:
        cuts_f90 = None
        has_f90 = False

    # Merge cuts at two polarization detectors of f150
    if len(det_f150) == 2:
        cuts_A = cuts.cuts[det_f150[0]]
        cuts_B = cuts.cuts[det_f150[1]]
        #cuts_f150 = merge_cuts(cuts_A, cuts_B) #Look at polarized spike that may appera at either pol
        cuts_f150 = common_cuts(cuts_A, cuts_B) #Only look at unpolarized spike that appear at both pols
        
    elif len(det_f150) == 1:
        cuts_f150 = cuts.cuts[det_f150[0]]
        
    else:
        cuts_f150 = None
        has_f150 = False
    # Loose mode -> Each frequency has to have at least one working det.
    '''
    if has_f90 and has_f150:
        cc = common_cuts(cuts_f90, cuts_f150)
        hist += cc.get_mask(nsamps=nsamps)
    '''
    # Strict mode -> Each frequency has to have two working det.
    if len(det_f90) ==2 and len(det_f150) == 2:
        cc = common_cuts(cuts_f90, cuts_f150)

        total_cut_time = 0
        for cut in cc:
            total_cut_time += cut[1]-cut[0]

        # Get the total cut lengths of the pixel
        hotmap[p] = total_cut_time


print hotmap
cPickle.dump(hotmap, open("outputs/hotmap/"+cut_no+".tmp", "wb"),cPickle.HIGHEST_PROTOCOL)
