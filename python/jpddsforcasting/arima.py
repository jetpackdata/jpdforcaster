import logging
import pandas as pd
import numpy as np
import math

import jpddsforcasting.toolbox as tb
import jpddsforcasting.modelbox as mb
from statsmodels.tsa.arima_model import ARIMA



logger = logging.getLogger(__name__)


class Arima(object):

    config_schema = None

    #default
    arima_config = None
    stationarityModel = None
    model = None
    
    def __init__(self, arima_config, full_history = None):

        self.arima_config = arima_config
        self.arima_config.add_specific_schema(self.config_schema)
        self.arima_config.m_config_validator()

        self.full_history = full_history

        self.stationarityModel = mb.stationarityModelHandling()

        
    def fit(self, df):
        
        ts = tb.validate_time_series_struct(df)
        self.full_history = ts
    
        logger.info("Je suis un fitter arima") 

        self.stationarityModel.fit(df) 
        ts = ts.set_index('ds')

        self.model = ARIMA(ts, order=(1, 1, 1)) 
        self.model.fit(disp=0)


        #Look for best windows 
        
        return self
        
              
    def predict(self, df):
        
        logger.info('Do the forecast on the future')  
        

        df['yhat'], variance_coeff = self.__compute_the_future(df)
        df['yhat_upper'] = df['yhat'].apply(lambda x : x + variance_coeff*x)
        df['yhat_lower'] = df['yhat'].apply(lambda x : x - variance_coeff*x)

        return df


    def __compute_the_future(self, df_with_future):
    
        stModel = self.stationarityModel.predict(df_with_future)
        
        df_with_future = df_with_future.join(self.full_history[['y']], how='outer')

        start_date = self.full_history.ds.max()
        end_date = df_with_future.ds.max()
        histoSize = len(self.full_history.y)
        residual = self.full_history.y - stModel.trend[:histoSize]

        
        predictions = self.model.predict(residual, start=1, end=histoSize+1)
        print(len(predictions),len(stModel.trend))
        predictions = predictions #+ stModel.trend + stModel.seasonal

        #var_coef = tb.cv_rmse_evaluation(self.full_history.y,predictions[:histoSize])
        #var_coef = var_coef + (stModel.trend_upper-stModel.trend_lower).mean() + (stModel.seasonal_upper-stModel.seasonal_lower).mean()
        var_coef = 0.15
        
        return predictions, var_coef

