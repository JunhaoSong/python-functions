import numpy as np
import math
from obspy.signal.util import smooth
def cal_fft_matrix(stream, nsmooth=0):
    st = stream.copy()
    WAVE, RESP = {}, {}
    
    ## time domain
    for tr in st:
        component = tr.stats.channel
        if 'TIME' not in WAVE.keys():
            WAVE['TIME'] = np.copy(tr.times())
        WAVE[component] = np.copy(tr.data)
        
    ## frequency domain
    # first remove mean, trend and taper two ends
    st.detrend('constant').detrend('linear').taper(max_percentage=0.05)
    # then pad the data with zeros to the next power of 2
    fs = st[0].stats.sampling_rate
    npts = st[0].stats.npts
    nfft = 2**math.ceil(math.log(npts)/math.log(2))
    freq = np.fft.fftfreq(nfft, 1/fs)
    # only reserve the positive part
    mask = (freq > 0)
    RESP['FREQ'] = freq[mask]
    for tr in st:
        component = tr.stats.channel
        RESP[component] = np.abs(np.fft.fft(tr.data, nfft)[mask]) / nfft * 2
        RESP[component] = smooth(RESP[component], nsmooth)
    return WAVE, RESP
