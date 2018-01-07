import cPickle
import matplotlib
matplotlib.use("GTKAgg")
from matplotlib import pyplot as plt
import moby2
import numpy as np

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
                iEnd = i
            else:
                iEnd = i
        else:
            if inRange or i == len(mask) -1:
                if iStart != iEnd:
                    _cuts.append([iStart, iEnd])
            inRange = False
    return _cuts

def inRange(vecs, t):
    for vec in vecs:
        if vec[0]<=t and vec[1]>t:
            return True
    return False

def findDet(data,time):
    dets = []
    for det in data:
        if inRange(data[det]['cuts'],time):
            dets.append(int(det))
    return dets

def plotDets(dets):
    ardata = loadArrayData("AR2")
    plt.plot(ardata['array_x'],ardata['array_y'],'r.')
    plt.plot(ardata['array_x'].iloc[dets],ardata['array_y'].iloc[dets],'b.')
    #plt.show()

cut_meta = cPickle.load(open("117.cut.new", "rb"))

cuts = cut_meta['cuts']

lds = cuts.get_uncut()

all_cuts = [list(cut) for ld in lds for cut in cuts.cuts[ld]]

endTime = max([max(item) for item in all_cuts])
print endTime

hist = np.zeros(endTime)
for cut in all_cuts:
    hist[cut[0]:cut[1]]+=1
fig, ax = plt.subplots()
ind = np.arange(endTime)
rects1 = ax.plot(hist, color='r')
ax.set_title('Number of detectors affected by cuts')
ax.set_ylabel('Number of detectors')
ax.set_xlabel('Time (sampling point)')
plt.show()
