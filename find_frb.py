import numpy as np
import moby2

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
        _mask =  (dis == 0) & (det_type == 'tes') # May need to give a range, and it will contain the item itself
        mask = _mask.flatten()
        indexes = np.where(mask == True) 
        overlap_location_list = list(list(indexes)[0]) # Normalize the np array output to list
        if i in overlap_location_list:
            overlap_location_list.remove(i) # Need to remove i from the list 

        overlap_dets[i]= overlap_location_list
    # Generate a function to access the data to make sure above procedures run once only
    def get_overlap_detectors(detector):
        if overlap_dets[detector]==[]:
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
    indexes = np.where(mask == True)
    input_list = list(list(indexes)[0]) 
    output_list = list(input_list) # Make a copy to input list 
    get_overlap_detectors = overlap_detectors_generator(array)
 
    for i in input_list:
        i_overlap = get_overlap_detectors(i)
        # i_overlap > i is to make sure no double removal occur
        if i_overlap != None and (i_overlap in output_list) and i_overlap > i:
            output_list.remove(i_overlap)
    
    return output_list

find_adjacent_detectors = adjacent_detectors_generator('AR2')
find_overlap_detectors = overlap_detectors_generator('AR2')
print find_adjacent_detectors(10)
print find_overlap_detectors(10)
print get_unique_detectors('AR2')

