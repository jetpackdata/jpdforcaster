import pandas as pd
import numpy as np
from os import walk
import re
from datetime import datetime
from sklearn.metrics import mean_squared_error
from math import sqrt
import os.path

default_conf = {"runtime_file_relative_path" : "/prickl_files/"}

def validate_time_series_struct(ts):
    """
        Parameters
        ----------
    
        Returns
        -------
        
        """
    if ts.columns.size != 2:
        raise ValueError("Data Frame size must be equal to 2 and have ds (datetime) and y (numeric) column")
        
    if 'ds' in ts:
        ts['ds'] = pd.to_datetime(ts['ds'])
    if 'y' in ts:
        ts['y'] = pd.to_numeric(ts['y'])       
        
    if ts['ds'].isnull().any():
        raise ValueError('Found NaN in column ds.')

    ts = ts.sort_values('ds')
    ts.reset_index(inplace=True, drop=True)
    
    return ts

def validate_dates_struct(ts):
    """
        Parameters
        ----------
    
        Returns
        -------
        
        """
        
    if 'ds' in ts:
        ts['ds'] = pd.to_datetime(ts['ds'])      
        
    if ts['ds'].isnull().any():
        raise ValueError('Found NaN in column ds.')

    ts['ds'] = ts['ds'].sort_values()
    ts.reset_index(inplace=True, drop=True)
    
    return ts

def make_future(ts, periods, freq='D', include_history=True):
        """
        Parameters
        ----------
    
        Returns
        -------
        
        """

        ts = validate_dates_struct(ts)
        date_history = ts['ds']
        last_date = date_history.max()
        dates = pd.date_range(
            start=last_date,
            periods=periods + 1,  # An extra in case we include start
            freq=freq)
           
        dates = dates[dates > last_date]  # Drop start if equals last_date
        
        dates = dates[:periods]  # Return correct number of periods
        
        if include_history:
            dates = np.concatenate((np.array(date_history), dates))

        return pd.DataFrame({'ds': dates})



def get_model_ref_name(ref_prefix, dir_path):
    file_modelname = None
    listeFichiers = []
    for (repertoire, sousRepertoires, fichiers) in walk(dir_path):
        listeFichiers.extend(fichiers)
    r = re.compile(ref_prefix+".*")
    model_list = filter(r.match, listeFichiers)
    if model_list is not None:
        if not not(model_list):
            model_list = sorted(model_list,reverse=True)
            file_modelname = model_list[0]
                           
    return file_modelname


def get_now():    
    (dt, micro) = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f').split('.')
    dt = "%s%03d" % (dt, int(micro) / 1000)
    return dt



def nrmse_evaluation(test, predictions):
    return sqrt(mean_squared_error(test, predictions))/(test.max()-test.min())

def rmse_evaluation(test, predictions):
    return sqrt(mean_squared_error(test, predictions))

def split_for_model_selection(ts,rate = 0.50):
    train_size = int(len(ts)*rate)
    train,test = ts[0:train_size],ts[train_size:]
    return train, test


"""
Split validation for time serie
"""
def split_time_series_for_validation(ts, split_point, name = 'ts'):
    """
        Parameters
        ----------
        ts : Initial time Series
        ....
    
        Returns
        -------
        
        """
    dataset, validation = ts[0:split_point], ts[split_point:]
    print('Dataset %d, Validation %d' % (len(dataset), len(validation)))
    dataset.to_csv(name + '_dataset.csv')
    validation.to_csv(name + '_validation.csv')
    return dataset, validation

"""
Get file name in consitent way
"""
def get_path_file(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

"""
Get a default configuration
"""
def get_conf(key):
    return default_conf[key]