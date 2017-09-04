import logging
import toolbox as tb
from modelfactory import Modelfactory
from statsmodels.iolib import smpickle as pick

logger = logging.getLogger(__name__)

def train_for_forcasting(ts, model, name, model_date):
    #Identify the model from the catalog
    factory = Modelfactory()
    selected_model = factory.create_instance(model)
    
    #Fit the model
    model_fit = selected_model.fit(ts)
    
    #Save the model
    model_ref_as_name = name+'_'+model+'_'+model_date+'.pkl'
    pick.save_pickle(model_fit,model_ref_as_name)
    
    return model_ref_as_name, model_fit
    
    
    

def run_forcast(ts,periods,freq, name, model):
    
    #checker l'existence du model avant
    model_ref_prefix = name+'_'+model
    
    
    model_ref_name = tb.get_model_ref_name(model_ref_prefix,'.')
    
    if model_ref_name is None:
        logger.info("Fitted model doesn't exist. We will create one")
        ref_name,m_ref = train_for_forcasting(ts, model, name, tb.get_now())
    else:
        logger.info("Get the stored model")
        m_ref = pick.load_pickle(model_ref_name)  
    
    future = tb.make_future(ts,periods,freq) 
    forcasted_result = m_ref.predict(future)
    
    return forcasted_result