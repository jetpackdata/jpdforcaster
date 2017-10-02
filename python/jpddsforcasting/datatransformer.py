"""
Transforme, Clean data for better modelization

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose

import jpddsforcasting.toolbox as tb



def prepare(time_series, configuration):
    
    ts = tb.validate_time_series_struct(time_series)
    ts = __variance_stabilizator(ts)
    #ts = __decomposition(ts)
    return ts

def back_to_origin(time_series): 
    #ts = __inverse_decomposition(time_series)   
    ts = __inverse_variance_stabilizator(time_series) 
    ts = tb.validate_time_series_date(time_series)
    return ts


def __variance_stabilizator(time_series):
    """
    Use log transform to stabilize the variance and take into account small variation
    Assume a well formed data frame
    """

    time_series['y'] = np.log(1 + time_series.y)
    return time_series

def __inverse_variance_stabilizator(time_series):
    """
    Assume a data frame with a yhat prediction with lower/ipper value
    """
    time_series['yhat'] = np.exp(time_series.yhat) - 1

    time_series['yhat_lower'] = np.exp(time_series.yhat_lower) - 1
    time_series['yhat_upper'] = np.exp(time_series.yhat_upper) - 1
    return time_series


def __decomposition(time_series):
    """
    Smooth trend and seasonability 
    """

    ts_decomp = time_series[['ds','y']]
    ts_decomp.set_index('ds', inplace=True)
    decomposition = seasonal_decompose(ts_decomp)

    trend = decomposition.trend.fillna(method='bfill').fillna(method='ffill')
    seasonal = decomposition.seasonal.fillna(method='bfill').fillna(method='ffill')
    residual = decomposition.resid.fillna(method='bfill').fillna(method='ffill')

    
    time_series['y'] = residual.reset_index('ds').y
    time_series['trend'] = trend.reset_index('ds').y
    time_series['seasonal'] = seasonal.reset_index('ds').y
    
    return time_series

def __inverse_decomposition(time_series):
    """
    Back to origine 
    """
    time_series['yhat'] = time_series['yhat']#*time_series['seasonal'] + time_series['trend']
    
    return time_series

def is_stationar(ts):

    ts = tb.validate_time_series_struct(ts)
    result = adfuller(ts.y)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')

    for key, value in result[4].items():
	    print('\t%s: %.3f' % (key, value))

    return result[0] < result[4]['1%']

def autocorrelation(ts) :
    """
    Compute the autocorrelation of the signal, based on the properties of the
    power spectral density of the signal.
    """
    centralized_ts = ts.y-np.mean(ts.y)
    tf = np.fft.fft(centralized_ts)
    spectral_density = np.array([np.real(v)**2+np.imag(v)**2 for v in tf])
    itf_spectral_density = np.fft.ifft(spectral_density)
    return np.real(itf_spectral_density)[:ts.y.size/2]/np.sum(centralized_ts**2)

