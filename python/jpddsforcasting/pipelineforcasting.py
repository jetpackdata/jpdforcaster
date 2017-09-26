import logging
import os.path
import tempfile

from statsmodels.iolib import smpickle as pick

import jpddsforcasting.datatransformer as dtt
import jpddsforcasting.toolbox as tb
from jpddsforcasting.modelfactory import Modelfactory

logger = logging.getLogger(__name__)

"""
m_config = {
        'model' : None,
        'date' : None,
        'id_model' : None,
    }
"""
def train_for_forcasting(ts, config):  
    #Identify the model from the catalog
    selected_model = Modelfactory().create_instance(config)

    #Data set transformation
    prepared_ts = dtt.prepare(ts, config)
    
    #Fit the model
    model_fit = selected_model.fit(prepared_ts)

    #Save the model
    stored_model_ref = __store_model(model_fit, config)
    
    return stored_model_ref, model_fit
    
    
    
"""
"""
def run_forcast(ts,periods,freq, config):
    
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
    
    future = tb.make_future(ts,periods,freq) 
    forcasted_result = dtt.back_to_origin(m_ref.predict(future))
    
    return forcasted_result

def __store_model(model, config):
    stored_model_ref = tb.compute_model_id_hash(config)+'_'+config['date']+'.pkl'
    abs_path_model_ref = os.path.join(tempfile.gettempdir(),stored_model_ref)

    #Save the model
    pick.save_pickle(model,abs_path_model_ref)
    
    return stored_model_ref
