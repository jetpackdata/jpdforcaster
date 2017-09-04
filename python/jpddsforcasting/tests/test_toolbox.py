from unittest import TestCase
import unittest as ut
import pandas as pd

#use nose intead to avoid adding this relative path
import sys
sys.path.append('../')
import toolbox as tb

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class TestToolbox(TestCase):
    

    def test_validate_time_series_struct(self):
        dataValidated = tb.validate_time_series_struct(DATA)
        self.assertEqual(dataValidated.columns.any(),'ds')
        
        


DATA = pd.read_csv(StringIO("""
ds,y
2012-05-18,38.23
2012-05-21,34.03
"""), parse_dates=['ds'])



#Run test
suite = ut.TestLoader().loadTestsFromTestCase(TestToolbox)
ut.TextTestRunner(verbosity=2).run(suite)