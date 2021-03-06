"""
.. module:: model dictionary
   :synopsis: A useful module indeed.

.. moduleauthor:: Alaoui Mohamed <alaoui.simo@gmail.com>


"""

class ModelConfig(object):
    m_config = {
        'model' : None,
        'date' : None,
        'id_model' : None,
    }

    schema = ['model','date','id_model','prediction_conf']
    sub_schema = ['future_period','freq']

    def __init__(self, mconfig):
        self.m_config.update(mconfig)

    def add_specific_schema(self, additional_schema_list):
        if (additional_schema_list):
            self.schema = self.schema + additional_schema_list 


    def add_specific_config(self, specific_dict):
        self.m_config.update(specific_dict)


    def m_config_validator(self):
        for key in self.schema:
            if key not in self.m_config:
                raise Exception("Model configuration is not valid, %s is not in the schema. Here is the configuration schema %s" % (key,self.schema))
            else:
                if(isinstance(self.m_config[key],dict)):
                   for keySub in self.sub_schema:
                        if keySub not in self.m_config[key]:
                            raise Exception("Model configuration is not valid, %s is not in the sub_config for %s attribute. Here is the configuration subschema %s attempted" % (keySub,key,self.sub_schema))
                    