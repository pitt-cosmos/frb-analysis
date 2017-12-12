for p in pixels:
    det_f90 = getDetectors(p, 90)
    det_f150 = getDetectors(p, 150)

    # Merge cuts at two polarization detectors of f90
    if len(det_f90) == 2:
        cuts_A = cuts.cuts[det_f90[0]]
        cuts_B = cuts.cuts[det_f90[1]]
        cuts_f90 = merge_cuts(cutsA, cutsB)
            
    elif len(det_f90) == 1:
        cuts_f90 = cuts.cuts[det_f90[0]]
            
    else:
        cuts_f90 = None

    # Merge cuts at two polarization detectors of f150
    if len(det_f150) == 2:
        cuts_A = cuts.cuts[det_f150[0]]
        cuts_B = cuts.cuts[det_f150[1]]
        cuts_f150 = merge_cuts(cutsA, cutsB)
        
    elif len(det_f150) == 1:
        cuts_f150 = cuts.cuts[det_f150[0]]
        
    else:
        cuts_f150 = None

    # Look for coincidental signals in f90 and f150 cuts
    if cuts_f90 and cuts_f150: # if any is none then no need
        coincidence = get_overlap(cuts_f90, cuts_f150)
        
    else:
        coincidence = None # return none if coincidence_cuts are not found
        # if the either of the frequency is None, save the pixel in msising_list
        missing_pixels.append(p)

    coincident_signals[p] = coincidence
    

