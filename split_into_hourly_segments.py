import math
import obspy
import numpy as np
def split_hourly_segments(wins, nhour=1):
    '''
    For example
    input: [[UTCDateTime(2018, 1, 7, 11, 22, 3, 805900), 
             UTCDateTime(2018, 1, 7, 13, 36, 34, 800900)]]
    output: [[UTCDateTime(2018, 1, 7, 12, 0) UTCDateTime(2018, 1, 7, 13, 0)]]
    '''
    time = np.array([])
    for win in wins:
        # The head (less than nhour) and tail (less than nhour) part would be discarded!
        beg = obspy.UTCDateTime(math.ceil(win[0].timestamp / 3600.0) * 3600.0)
        end = obspy.UTCDateTime(math.floor(win[1].timestamp / 3600.0) * 3600.0)
        while beg < end:
            if time.size == 0:
                time = np.array([[beg, beg+3600*nhour]])
            else:
                time = np.vstack((time, [beg, beg+3600*nhour]))
            beg += 3600*nhour
    return time
