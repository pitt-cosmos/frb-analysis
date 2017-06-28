import numpy as np
from cuts import CutReader
import pickle
#import matplotlib.pyplot as plt
import sys

def findCuts(hist, low, high=None):
    # Generate masks
    if high:
        mask = [item >= low and item < high for item in hist] 
    else:
        mask = [item >= low for item in hist] 
    
    # Find cuts
    inRange = False
    iStart = 0
    iEnd = 0
    _cuts = []
    for i, t in enumerate(mask):
        if t:
            if not inRange:
                inRange = True
                iStart = i
            else:
                iEnd = i
        else:
            if inRange:
                _cuts.append([iStart, iEnd])
            inRange = False
    return _cuts

def plotCuts(data):
    AR1_cuts = [data[det]['cuts'] for det in data if data[det]['array']=='AR1' and len(data[det]['cuts'])!=0]
    AR2_cuts = [data[det]['cuts'] for det in data if data[det]['array']=='AR2' and len(data[det]['cuts'])!=0]
    endTime = max([max(item) for item in AR2_cuts])[1]
    hist = np.zeros(endTime)
    for cuts in AR1_cuts:
        for cut in cuts:
            hist[cut[0]:cut[1]]+=1
    nCutsPerOccurance = [len(findCuts(hist,i,i+1)) for i in range(1, int(max(hist)))] 
    
    '''
    fig, ax = plt.subplots()
    ax.bar(np.arange(1, len(nCutsPerOccurance)+1), nCutsPerOccurance, color='red')
    ax.set_title('Number of cuts that affect a fixed number of detectors (AR1)')
    ax.set_ylabel('Number of cuts')
    ax.set_xlabel('Number of detectors affected')
    plt.show()
    '''
    
    return nCutsPerOccurance

#===================
# Main body
#===================

cr = CutReader()
tods = cr.get_available_tods()

istart = int(sys.argv[1])
iend = int(sys.argv[2])

for tod in tods[istart:iend]:
    print "INFO: Extracting information from tod " + str(tod)
    cr.loads_cuts_from_tod(tod)
    data = cr._cut_data
    hist = plotCuts(data)
    with open("cuts_fixed_detector/" + str(tod) + ".dat", "wb") as f:
        pickle.dump(hist, f)
    print "INFO: File saved!"
