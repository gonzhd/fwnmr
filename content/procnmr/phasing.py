import numpy as np
import scipy.optimize as opt


def phase_corr(data, p0, p1) :
    p0 = p0 * np.pi / 180. 
    p1 = p1 * np.pi / 180.
    size = data.shape[-1]
    corr = np.exp(-1.0j * (p0 + (p1 * np.linspace(0, 1, size)))).astype(data.dtype)
    return corr * data

def dx(data):
    z = np.empty_like(data)
    z[..., 0] = data[..., 1] - data[..., 0]    # first point
    z[..., -1] = data[..., -1] - data[..., -2]  # last point
    z[..., 1:-1] = data[..., 2:] - data[..., 1:-1]  # interior
    return z

def entropy(data) :
    d1 = dx(data.real)
    norm = sum(np.abs(d1))
    h = np.abs(d1) / norm
    #plotspec(h)
    return -sum(h * np.log(h))
    
def penalty(data) :
    return sum([i**2 for i in data.real if i < 0])
    
def E(data, alpha, beta, gamma, ph0, ph1) :
    f = phase_corr(data, p0=ph0, p1=ph1)
    e = alpha * entropy(f)
    i = beta * tot_abs_int(f)
    p = gamma * penalty(f)
    #print(ph0, ph1, e, p, e+p)
    return e + i + p
    
def minE(x, *args) :
    return E(args[0], args[1], args[2], args[3], x[0], x[1])
    
def minPh0(ph0, *args) :
    ''' minimize ph0 independently from ph1 '''
    return E(args[0], args[1], args[2], args[3], ph0, args[4])
    
def poly(x, a, b, c, d) :
    return a * x**3 + b * x**2 + c * x + d

def tot_abs_int(data) :
    ''' calculates the total absolute intensity of the spectrum '''
    return np.abs(data.real).sum()

def tot_pos_int(data) :
    ''' returns total positive integral '''
    return sum([x for x in data.real if x > 0])

def tot_neg_int(data) :
    ''' calculate total negative integral '''
    return sum([x for x in data.real if x < 0])

def tot_pow_neg_int(data) :
    ''' returns total power of negative integral '''
    return sum([x * np.conjugate(x) for x in data if x < 0])
    
def total_power(data):
    ''' returns total spectral power '''
    return sum(power_spectrum(data))

def power_spectrum(data) :
    ''' returns power spectrum'''
    return data * data.conj()