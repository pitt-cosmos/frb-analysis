import moby2
import math
import cPickle
import numpy as np
from pixels import PixelReader
import sys

ardata = moby2.scripting.get_array_data({'season':'2016', 'array_name':'AR3'})
cut_no = sys.argv[1]
print 'Loading cut:', cut_no
cuts_data = cPickle.load(open("outputs/cuts/"+cut_no+".cut","rb"))
cuts = cuts_data['cuts']
first = lambda x: x[0]
print cuts_data
npix = 0

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

# Get a unique list of lixels
pr = PixelReader()
pixels = pr.getPixels()

# Get nsamples
nsamps = max([cut[-1][1] for cut in cuts.cuts if len(cut)!=0])
first = True
hist = [0]*nsamps

#Get the good pixel list and use it instead of pixels
good_pixels = cPickle.load(open("good_pixel_list.pickle","rb"))
bad_pixels = [p for p in pixels if p not in good_pixels]
# Get the filtered list
for p in bad_pixels:
    #print '[INFO] Looking at pixel %d ' % p
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
        npix += 1
        hist += cc.get_mask(nsamps=nsamps)

def find_peaks(hist):
    nsamps = len(hist)
    last = 0
    peaks = []
    for i in range(nsamps):
        if hist[i] > 0 and last == 0:
            peak_start = i    
        if hist[i] == 0 and last > 0:
            peak_end = i
            peak_amp = max(hist[peak_start:peak_end])
            peak_duration = peak_end - peak_start
            peaks.append([peak_duration, peak_amp])
        last = hist[i]
    return peaks

cPickle.dump(find_peaks(hist), open("outputs/plot_cs_scatter_filter_reverse/"+cut_no+".tmp", "wb"),cPickle.HIGHEST_PROTOCOL)
#print 'Total number of pixel of interests is:', npix 
#plt.plot(hist) 
#plt.show()
