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

find_adjacent_detectors = adjacent_detectors_generator('AR2')
print find_adjacent_detectors(10)
