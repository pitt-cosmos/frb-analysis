import json
import os

class CutReader:
    def __init__(self):
        self._cut_data = None
        self._f = None

    def loads_cuts_from_tod(self, todId):
        '''
        Loads all cuts data for a specific TOD into memory
        '''
        try:
            _f = open("outputs/" + str(todId) + ".txt")
            self._f = _f
            _data = _f.read()
            _cut_data = json.loads(_data)
            self._cut_data = _cut_data
        except IOError:
            print "No cuts information available"
        
    def get_cuts(self, det):
        '''
        Get cuts data for a specific detector (det)
        '''
        if self._cut_data == None:
            print "No cut data loaded. "
            return None
        else:
            key = str(det)
            if key in self._cut_data:
                return self._cut_data[key]['cuts']
            else:
                print "No cuts found for detector " + key
                return None

    def get_detectors(self, array = None):
        '''
        Get all detectors that have cuts information
        '''
        if self._cut_data != None:
            if array != None:
                return [int(key) for key in self._cut_data if self._cut_data[key]["array"] == array]
            else:
                return [int(key) for key in self._cut_data]
        else:
            print "No cut data loaded. "
            return None

    def unloads(self):
        '''
        Free the memory of loaded cuts and close opened files
        '''
        if self._f != None:
            self._f.close()
            self._f = None
        self._cut_data = None

    def get_available_tods(self):
        '''
        Get a list of tods that have been processed
        '''
        tod_file_list = os.listdir('outputs');
        
        # Strip off txt and convert to integer
        tod_list = [int(f[:-4]) for f in tod_file_list if f.endswith('.txt')]

        # Sort the list
        tod_list.sort()

        return tod_list

