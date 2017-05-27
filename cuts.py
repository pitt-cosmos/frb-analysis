import json

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
                return self._cut_data[key]
            else:
                print "No cuts found for detector " + key
                return None

    def get_detectors(self):
        '''
        Get all detectors that have cuts information
        '''
        if self._cut_data != None:
            return [key for key in self._cut_data]
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
