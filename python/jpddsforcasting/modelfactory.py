from sma import Sma
from fbprophet import Prophet
import logging

logger = logging.getLogger(__name__)

class Modelfactory(object):
    
    registred_model = ["sma","prophet"]
    
    def __init__(self):
        pass
        
    def create_instance(self, model_name):
        model_fit = None
        if model_name in self.registred_model:
            if model_name == 'sma':
                model_fit = Sma()
            if model_name == 'prophet':
                model_fit = Prophet()
        else:
            error_message = model_name + " is not yet registred"
            logger.error(error_message)
            raise ValueError(error_message) 
                
        return model_fit