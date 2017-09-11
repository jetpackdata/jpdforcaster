import logging
import pandas as pd
import numpy as np
import math

import jpddsforcasting.toolbox as tb


logger = logging.getLogger(__name__)


class Sma(object):
    
    def __init__(self, windows_size = 1, 
                 full_history=None):
        self.windows_size = windows_size
        self.full_history = full_history
        
    def fit(self, df):
        logger.info("Je suis un fitter et la fenetre est : %s" % self.windows_size) 
        ts = tb.validate_time_series_struct(df)
        self.full_history = ts
        logger.info("Time Series have the right structure")
        
        #Look for best windows -- to do later -- let assume it's 10
        #We suppose at the first time as full_history is the estimationSet
        self.windows_size = 10
        
        return self
        
              
    def predict(self, df):
        
        logger.info('Do the forecast on the future')                     
        df['yhat'] = self.__compute_the_future(df)
        
        return df
    
    
    def __compute_the_future(self, df_with_future):
        
        first_window = self.full_history['y']
        df_with_future = pd.concat((df_with_future,first_window),axis=1)
            
        iterator = range(len(df_with_future)-self.windows_size)
        
        temp_prediction = np.array(first_window[:self.windows_size])
        predictions = np.array(first_window[:self.windows_size])
        history_with_future = np.array(first_window[:self.windows_size])
            
        for i in iterator:
            yhat_with_lag = np.mean(history_with_future[-self.windows_size:])  
            temp_prediction = np.append(temp_prediction,yhat_with_lag)
            
            obs = df_with_future['y'][i]
            if math.isnan(obs) :
                obs = yhat_with_lag  
            history_with_future = np.append(history_with_future,obs)
            
            yhat_unlag = np.mean(temp_prediction[-self.windows_size:]) 
            
            diff = yhat_with_lag - yhat_unlag
            
            yhat = yhat_with_lag + diff
            
            predictions = np.append(predictions,yhat)        
            
            
        return predictions
    