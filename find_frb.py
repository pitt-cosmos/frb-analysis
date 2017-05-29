import numpy as np
import moby2
import itertools

######################
# Auxilary Functions 
######################

# Generator function to generate find_adjacent_detector function
def adjacent_detectors_generator(array):
    """
    Generate a get_adjacent_detectors function
    Return a function to get adjacent detectors
    
    array: 'AR1' or 'AR2'
    return: [int] function(int det)
    """
    
    # Make sure array name is valid
    assert array == 'AR1' or array == 'AR2' 
    
    # Get detector info file
    amdata = moby2.scripting.get_array_data({'season':'2014', 'array_name': array})
    arx = amdata['array_x']
    ary = amdata['array_y']
    det_type = amdata['det_type']
    # Find the adjacent detectors
    adj_dets = [None] * len(arx) # Generate an empty list to store adjacent detector lists
  
    for i in range(len(arx)):
        dis = (arx - arx[i])**2 + (ary - ary[i])**2 
        _mask = ((dis < 0.6**2) & (dis <> 0)).T & ((arx <> 0) | (ary <> 0)) & (det_type == 'tes')
        mask = _mask.flatten()
        indexes = np.where(mask == True)
        adj_dets[i]= list(list(indexes)[0]) # Normalize the np array output to list
    
    # Generate a function to access the data to make sure above procedures run once only
    def get_adjacent_detectors(detector):
        return adj_dets[detector]
    
    return get_adjacent_detectors

# Generator function to generate find_adjacent_detector function
def overlap_detectors_generator(array):
    """
    Generate a get_adjacent_detectors function
    Return a function to get adjacent detectors
    
    array: 'AR1' or 'AR2'
    return: [int] function(int det)
    """
    
    # Make sure array name is valid
    assert array == 'AR1' or array == 'AR2' 
    
    # Get detector info file
    amdata = moby2.scripting.get_array_data({'season':'2014', 'array_name': array})
    arx = amdata['array_x']
    ary = amdata['array_y']
    det_type = amdata['det_type']
    
    # Find the same location detectors algorithm starts below
    overlap_dets = [None] * len(arx) # Generate an empty list to store adjacent detector lists
    for i in range(len(arx)):
        dis = (arx - arx[i])**2 + (ary - ary[i])**2
        _mask =  (dis == 0) & (det_type == 'tes') # It will contain the item itself
                                                  # Only the working detectors are used
                                                  # STRICT
        mask = _mask.flatten()
        indexes = np.where(mask == True) 
        overlap_location_list = list(list(indexes)[0]) # Normalize the np array output to list
        if i in overlap_location_list:
            overlap_location_list.remove(i) # Need to remove i from the list 

        overlap_dets[i]= overlap_location_list
    # Generate a function to access the data to make sure above procedures run once only
    def get_overlap_detectors(detector):
        if not overlap_dets[detector]:
            return None
        else:
            return overlap_dets[detector][0]
    
    return get_overlap_detectors

def get_unique_detectors(array):
    '''
    Function to find a unique list of detectors that occupy each 
    detector location
    '''
    assert array == 'AR1' or array == 'AR2' 
    amdata = moby2.scripting.get_array_data({'season':'2014', 'array_name': array})
    _mask = (amdata['det_type'] == 'tes')
    mask = _mask.flatten()
    print "len(mask)"
    print len(mask)
    indexes = np.where(mask == True)
    input_list = list(list(indexes)[0]) 
    output_list = list(input_list) # Make a copy to input list 
    get_overlap_detectors = overlap_detectors_generator(array)
 
    for i in input_list:
        i_overlap = get_overlap_detectors(i)
        # i_overlap > i is to make sure no double removal occur
        if i_overlap != None and (i_overlap in output_list) and i_overlap > i:
            output_list.remove(i_overlap)
        elif i_overlap == None: # remove the detector from the list if it's 
                                # overlapping partner is offline
                                # STRICT
            output_list.remove(i)
    
    return output_list

# DEBUG
#find_adjacent_detectors = adjacent_detectors_generator('AR2')
#find_overlap_detectors = overlap_detectors_generator('AR2')
#print find_adjacent_detectors(16)
#print find_overlap_detectors(16)
#print get_unique_detectors('AR2')

####################
# Main program
###################

from cuts import CutReader
cr = CutReader()

# Work with one TOD for example
# Load cuts data into memory
cr.loads_cuts_from_tod(49) 

# Work with one array for example
# Get list of detectors with cuts of interests
list_detectors = cr.get_detectors('AR2')
print "Numbers of detectors from file is "
print len(list_detectors)

# Generate auxilary functions and list
find_adjacent_detectors = adjacent_detectors_generator('AR2')
find_overlap_detectors = overlap_detectors_generator('AR2')
unique_detectors = get_unique_detectors('AR2')
print "Number of unique detectors is "
print len(unique_detectors)

# Find unique detectors with cuts of interests
unique_detectors_with_cuts = [det for det in unique_detectors if det in list_detectors] 

def find_overlap(cutVec1, cutVec2):
    '''
    This function finds the overlap interval between two cut vectors
    It returns None if there is no overlap
    '''
    mi = max(cutVec1[0], cutVec2[0])
    ma = min(cutVec1[1], cutVec2[1])
    if mi < ma:
        return [mi, ma]
    else:
        return None

def find_common_cuts(cutList1, cutList2):
    ''' 
    Function to return common cuts among two cut lists
    returns a new cut list
    '''
    common_cuts = []
    for cut1 in cutList1:
        for cut2 in cutList2:
            overlap = find_overlap(cut1, cut2)
            if overlap != None:
                common_cuts.append(overlap)
    if not common_cuts: # when the list is empty return None
        return None
    return common_cuts

# 1. Filter cuts based on overlaping detectors

cuts = {} # A dictionary to store results
print "Number of unique detectors with cuts is "
print len(unique_detectors_with_cuts)

for det in unique_detectors_with_cuts:
    det_overlap = find_overlap_detectors(det)
    if det_overlap != None and det_overlap in list_detectors:
        common_cuts = find_common_cuts(cr.get_cuts(det), cr.get_cuts(det_overlap))
        if common_cuts != None:
            cuts[det] = common_cuts


# 2. Filter cuts based on adjacent detectors
signals = {}

# Generate a list of detectors that pass the overlap filter
filtered_detectors = [int(key) for key in cuts]
print "Number of detectors passing overlap filter"
print len(filtered_detectors)

for det in filtered_detectors:
    all_cuts = []
    adjacent_detectors = find_adjacent_detectors(det)
    unique_adjacent_detectors = [ d for d in adjacent_detectors if d in cuts] # remove detectors that are overlapped
    for adj_det in unique_adjacent_detectors:
        common_cuts = find_common_cuts(cuts[det], cuts[adj_det])
        if common_cuts != None:
            all_cuts.append(common_cuts[0])

    # A unique cut vector in the list will be a signal that we are interested
    all_cuts.sort()
    uniq = list(k for k, g in itertools.groupby(all_cuts) if len(list(g)) == 1)
    if len(uniq) != 0: 
        signals[det] = uniq

print signals
