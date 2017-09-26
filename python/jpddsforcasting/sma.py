import logging
import pandas as pd
import numpy as np
import math

import jpddsforcasting.toolbox as tb



logger = logging.getLogger(__name__)


class Sma(object):

    config_schema = ['window_size']

    #default
    sma_config = None
    window_size = 10

    
    def __init__(self, sma_config, full_history = None):

        self.sma_config = sma_config
        self.sma_config.add_specific_schema(self.config_schema)
        self.sma_config.m_config_validator()

        self.full_history = full_history
        self.window_size = self.sma_config.m_config['window_size']

        
    def fit(self, df):
        
        ts = tb.validate_time_series_struct(df)
        self.full_history = ts
    
        logger.info("Je suis un fitter et la fenetre est : %s" % self.window_size) 

        #Look for best windows 
        
        return self
        
              
    def predict(self, df):
        
        logger.info('Do the forecast on the future')                     
        df['yhat'], variance_coeff = self.__compute_the_future(df)
        df['yhat_upper'] = df['yhat'].apply(lambda x : x + variance_coeff*x)
        df['yhat_lower'] = df['yhat'].apply(lambda x : x - variance_coeff*x)

        
        df = df.join(self.full_history[['trend','seasonal']], how='outer')
                
        return df


    def __compute_the_future(self, df_with_future):
    
        
        df_with_future = df_with_future.join(self.full_history[['y']], how='outer')
        max_history_date = self.full_history.ds.max()

        fwd_predictions = pd.Series(self.full_history.y).rolling(window=self.window_size,center=False).mean() # take sma in fwd direction
        bwd_predictions = pd.Series(self.full_history.y[::-1]).rolling(window=self.window_size,center=False).mean() # take sma in bwd direction
        fwd_predictions = fwd_predictions.fillna(method='bfill')
        bwd_predictions = bwd_predictions.fillna(method='bfill')

        filtered = np.vstack(( fwd_predictions, bwd_predictions[::-1])) # lump fwd and bwd together
        predictions = np.mean(filtered, axis=0 ) # average them

        is_to_forcast = (df_with_future.ds > max_history_date)

        iterator = range(len(is_to_forcast))

        temp = self.full_history.y[-self.window_size:]
        
        for i in iterator:
            if is_to_forcast[i]:
                yhat_fwd = pd.Series(temp[-self.window_size:]).rolling(window=self.window_size,center=False).mean()
                yhat_bwd = pd.Series(temp[-self.window_size:][::-1]).rolling(window=self.window_size,center=False).mean()
                
                yhat_fwd = yhat_fwd.fillna(method='bfill')
                yhat_bwd = yhat_bwd.fillna(method='bfill')
                

                yhat = np.mean(np.vstack(( yhat_fwd, yhat_bwd[::-1])),axis=0)[-1:]
                  
                temp = np.append(temp, yhat) # Recursive Multi-step Forecast

                predictions = np.append(predictions, yhat)
        
        var_coef = tb.cv_rmse_evaluation(self.full_history.y,predictions[:len(self.full_history.y)])

        return predictions, var_coef

