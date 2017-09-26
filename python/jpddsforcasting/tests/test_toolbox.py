from unittest import TestCase
import unittest as ut
import pandas as pd
import logging

import jpddsforcasting.toolbox as tb
import jpddsforcasting.modelconfig as mc
import jpddsforcasting.datatransformer as dtt

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


logger = logging.getLogger(__name__)

class TestToolbox(TestCase):
    

    def test_validate_time_series_struct(self):
        dataValidated = tb.validate_time_series_struct(DATA)
        self.assertEqual(dataValidated.columns.any(),'ds')
        
        
    def test_model_configuration(self):
        conf = mc.ModelConfig(ext_config)
        self.assertTrue(conf.m_config['date'] == ext_config['date'])

    #You can use assert raise also
    def test_model_configuration_schema(self):
        conf = mc.ModelConfig(ext_config)
        try:
            conf.m_config_validator()
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)
        
    def test_model_configuration_schema_bis(self):
        conf = mc.ModelConfig(ext_config)
        conf.add_specific_schema(['window_size'])
        try:
            conf.m_config_validator()  
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)


    def test_compute_model_id_hash(self):
        hashconf = tb.compute_model_id_hash(config_for_hash)
        self.assertEqual(hashconf,hashref)

    def test_prepare_back(self):
        #Assume the identity as trained model
        ts = dtt.prepare(DATA_TRANS, None)
        ts['yhat'] = ts.y
        ts['yhat_upper'] = 0
        ts['yhat_lower'] = 0
        ts = dtt.back_to_origin(ts)
        print(ts)
        self.assertEqual(ts.y_orig.any(),ts.yhat.any())

    def test_autocorrelation(self):
        ts = real_data
        autoC = dtt.autocorrelation(ts)
        self.assertIsNotNone(autoC)

    def test_stationarity(self):
        ts = real_data
        self.assertFalse(dtt.is_stationar(ts))


#data for tests
ext_config = {'window_size' : 50, 'date' : tb.get_now()}
config_for_hash = {'window_size' : 50, 'date' : 11111111, 'id_model' : 'gross revenue aiaxa', 'model' : 'sma'}
hashref = '53bc7ef6bef350f4feb2f3305c30b873d133515f'

DATA = pd.read_csv(StringIO("""
ds,y
2012-05-18,38.23
2012-05-21,34.03
"""), parse_dates=['ds'])

DATA_TRANS = pd.read_csv(StringIO("""
ds,y
2012-05-18,38.23
2012-05-19,0.8
2012-05-20,0.2
2012-05-21,0.0
2012-05-22,36.0
2012-05-23,34.03
"""), parse_dates=['ds'])

real_data = pd.read_csv(tb.get_path_file("dataset/jpdDataSetForForcasting-2.csv"))



#Run test
suite = ut.TestLoader().loadTestsFromTestCase(TestToolbox)
ut.TextTestRunner(verbosity=2).run(suite)