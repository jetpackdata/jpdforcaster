from fbprophet import Prophet
import logging

from jpddsforcasting.sma import Sma
from jpddsforcasting.ewma import Ewma
from jpddsforcasting.modelconfig import ModelConfig

logger = logging.getLogger(__name__)

class Modelfactory(object):
    
    registred_model = ["sma","prophet","ewma"]
    
    def __init__(self):
        pass
        
    def create_instance(self, configuration):
        model_fit = None
        conf = ModelConfig(configuration)

        #Basic validation for generic configuration
        conf.m_config_validator()
        
        model_name = conf.m_config['model']
        if model_name in self.registred_model:
            if model_name == 'sma':
                model_fit = Sma(conf)
            if model_name == 'prophet':
                model_fit = Prophet()
            if model_name == 'ewma':
                model_fit = Ewma(conf)
        else:
            error_message = model_name + " is not yet registred"
            logger.error(error_message)
            raise ValueError(error_message)       
        
        return model_fit