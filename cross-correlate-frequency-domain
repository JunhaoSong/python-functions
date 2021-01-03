import numpy as np
def correlate(data1, data2, sampling_rate, lagtime):
    '''
    Given two time series data (e.g. seismic waveforms) with equal length and equal sampling rate
    this function could calculate the cross-correlation function between them in the frequency domain
    which is much more efficient than in the time domain when the lagtime is relatively large
    Such as: 
    data1 = np.array([1, 2, 3])
    data2 = np.array([4, 5, 6])
    correlate(data1, data2, 1, 2)
    output: 
    [-2., -1.,  0.,  1.,  2.]
    [  6.,  17.,  32.,  23.,  12.]
    The result is the same as that calculated from: np.correlate(data1, data2, 'full')
    '''
    if len(data1) != len(data2):
        raise ValueError('The length of two time series should be equal! ')
    winsize = len(data1)
    lagsize = int(sampling_rate * lagtime)
    time = np.linspace(-lagsize, lagsize, 2*lagsize+1)/sampling_rate
    fft1 = np.fft.fft(data1, winsize+lagsize)
    fft2 = np.fft.fft(data2, winsize+lagsize)
    f_corr = np.fft.ifft(np.conjugate(fft2)*fft1)
    r_corr = np.real(f_corr[:lagsize+1])
    l_corr = np.real(f_corr[-lagsize:])
    f_corr = np.append(l_corr, r_corr)
    return time, f_corr
