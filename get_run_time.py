import numpy as np
def get_run_time(st):
    '''
    Get the operating time windows of one station
    The input is suggested to be the 'headonly' stream for single component
    written by Junhao, SONG
    e.g.
        stream = obspy.read('*BHZ.SAC')
        get_run_time(stream)
        output:
        array([[UTCDateTime(2018, 1, 7, 11, 22, 3, 805900),
                UTCDateTime(2018, 1, 9, 10, 36, 34, 800900)]], dtype=object)
    '''
    time = np.array([])
    for tr in st:
        beg, end = tr.stats.starttime, tr.stats.endtime
        if time.size == 0:
            time = np.array([[beg, end]])
        else:
            # when there exists overlaping or perfect connection
            if (beg <= time[-1][1] + tr.stats.delta) & (end > time[-1][1]):
                time[-1][1] = end
            # when gaps exist, a new time-pair would be created
            elif (beg > time[-1][1] + tr.stats.delta):
                time = np.vstack((time, [beg, end]))
    return time
