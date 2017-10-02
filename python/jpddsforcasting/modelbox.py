"""This modul expose some common services for models
As prophet library handle perfectly the trend ans seasonability
we choose to use it as a background fitter for all models to handle the seasonnability
and the trend
"""

from fbprophet import Prophet

def stationarityModelHandling():
    return Prophet()
