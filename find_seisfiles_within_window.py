import obspy
import glob
def find_seisfiles_within_window(seisfiles, window):
    '''
    input the seismic files list, starttime and endtime
    output the seismic files whose timeperiods span the time window
    this function performs very well when there are lots of seismic data files
    it's inappropriate to use obspy.read(***, starttime, endtime) when '***' contains many files
    '''
    output = np.array([])
    for seisfile in seisfiles:
        st = obspy.read(seisfile, headonly=True)
        t1,t2 = st[0].stats.starttime, st[0].stats.endtime
        # flags for no overlap at all
        flag1 = (t2 <= window[0])
        flag2 = (t1 >= window[1])
        if flag1 or flag2:
            continue
        else:
            output = np.append(output, seisfile)
    return output
