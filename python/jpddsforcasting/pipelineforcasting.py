"""This module is the public API of jdpdsforcasting.
We have a train API and forcast API
"""



import logging
import os.path
import tempfile

from statsmodels.iolib import smpickle as pick

import jpddsforcasting.datatransformer as dtt
import jpddsforcasting.toolbox as tb
from jpddsforcasting.modelfactory import Modelfactory

logger = logging.getLogger(__name__)

def train_for_forcasting(ts, config):
    """This function does the training on ts according to the config argument

    Args:
        ts (pandas data frame): ts means time series. There is no a strong 
                                hypthesis on the data frame except an exictence 
                                of a minumum of 2 columns ds (datetime) and y (numeric)

        config (dictionary):    config is a dictionnary with a minimum of 3 entries. 
                                Could have some model dependant entries or optionnal technical entries
            model: the model name
            date: the date of the training
            id_model: model indentifier

    Returns:
       model name (string):     As the model is persited, the first returnd value is the pinckle name
       model fitted (object):   Model instance    

    Raises:
       XXXXXX

    A really great idea.  A way you might use me is

    See usage.py for a demo."""  
    #Identify the model from the catalog
    selected_model = Modelfactory().create_instance(config)

    #Data set transformation
    prepared_ts = dtt.prepare(ts, config)
    
    #Fit the model
    model_fit = selected_model.fit(prepared_ts)

    #Save the model
    stored_model_ref = __store_model(model_fit, config)
    
    return stored_model_ref, model_fit
    
    
def run_forcast(ts, config):
    """This function does the forcasting and return a pandas df with all the historical value
    and predicted one. We have 2 differents mode according to our usage.
    If you need to refit the model, add clean entry to True to the config dict

    Args:
        ts (pandas data frame): ts means time series. There is no a strong 
                                hypthesis on the data frame except an exictence 
                                of a minumum of 2 columns ds (datetime) and y (numeric)
        periods (int):          used to define the future period for forecasting. According 
                                to the freq args, it's interpreted as a daily,monthly or yearly periods
        freq (string):          frequency in the time series. Could take 3 values : 'D' for daily,
                                'M' for monthly, 'Y' for yearly

        config (dictionary):    config is a dictionnary with a minimum of 3 entries. 
                                Could have some model dependant entries or optionnal technical entries
            model (string): the model name
            date (datetime): the date of the training as a time staamp with millis
            id_model (string): model indentifier to make the model unique
            prediction_conf (dictionary):
                future_period (int): number of prediction to perform
                freq (string): 'D' for daily, 'M' for monthly, 'Y' for yearly
            tech_conf (dictionary) [optionnal]:
                clean (bool): clean all existing model and refit. This option remove all exixting model.
                              need improvement to perform an ad hoc clean


    Returns:
       forcasted result (pandas data frame):    This function return some new columns in the data frame.
                                                yhat predicted values, yhat_lower and yhat_upper for uncertainty,
                                                trend, seasonnability...to complete

    Raises:
       XXXXXX

    See usage.py for a demo."""
    
    #Try to get the model
    model_ref_prefix = tb.compute_model_id_hash(config)
    
    
    model_ref_name = tb.get_model_ref_name(model_ref_prefix,tempfile.gettempdir())
    clean = 'tech_conf' in config and 'clean' in config['tech_conf'] and config['tech_conf']['clean']
    
    if model_ref_name is None or clean:
        logger.info("Fitted model doesn't exist or not up to date. We will create one")
        ref_name,m_ref = train_for_forcasting(ts, config)
    else:
        logger.info("Get the stored model")
        m_ref = pick.load_pickle(os.path.join(tempfile.gettempdir(),model_ref_name))  
    
    period = config['prediction_conf']['future_period']
    freq = config['prediction_conf']['freq']
    future = tb.make_future(ts, period, freq)
    forcasted_result = dtt.back_to_origin(m_ref.predict(future))
    
    return forcasted_result

def __store_model(model, config):
    stored_model_ref = tb.compute_model_id_hash(config)+'_'+config['date']+'.pkl'
    abs_path_model_ref = os.path.join(tempfile.gettempdir(),stored_model_ref)

    #Save the model
    pick.save_pickle(model,abs_path_model_ref)
    
    return stored_model_ref
