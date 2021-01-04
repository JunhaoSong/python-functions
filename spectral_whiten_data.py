import numpy as np
from obspy.signal.util import smooth
def spectral_whiten(data1, data2, sampling_rate=200, lagtime=2, method='one-bit', freqmin=2, freqmax=10, n_smooth=10):
    '''
    adapted from NoisePy scripts
    '''
    delta = 1/sampling_rate
    if len(data1) != len(data2):
        raise ValueError('The length of two time series should be equal! ')
    winsize = len(data1)
    lagsize = int(sampling_rate * lagtime)
    nfft = winsize + lagsize
    freq = np.fft.fftfreq(nfft, delta)
    mask = np.where((freq >= freqmin) & (freq <= freqmax))[0]
    edge = 100
    left = mask[0]
    right = mask[-1]
    low = mask[0] - edge
    if low <= 0:
        low = 1
    high = mask[-1] + edge
    if high > nfft/2:
        high = int(nfft//2)
    
    output = np.array([])
    for i, data in enumerate([data1, data2]):
        fft = np.fft.fft(data, nfft)
        fft[0:low] *= 0
        fft[low:left] = np.cos(np.linspace(np.pi / 2., np.pi, left - low)) ** 2 * np.exp(1j * np.angle(fft[low:left]))
        fft[right:high] = np.cos(np.linspace(0., np.pi / 2., high - right)) ** 2 * np.exp(1j * np.angle(fft[right:high]))
        fft[high:nfft//2] *= 0
        # Pass band:
        if method == 'one-bit':
            print(method)
            fft[left:right] = np.exp(1j * np.angle(fft[left:right]))
        elif method == 'mov-ave':
            print(method)
            fft[left:right] = fft[left:right] / smooth(np.abs(fft[left:right]), n_smooth)
            
        # Hermitian symmetry (because the input is real)
        fft[-(nfft//2)+1:] = fft[1:(nfft//2)].conjugate()[::-1]
        if i == 0:
            output = fft
        else:
            output = np.vstack((output, fft))
    return output[0], output[1]
