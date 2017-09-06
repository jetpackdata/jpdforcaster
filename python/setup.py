from distutils.core import setup

setup(
  name = 'jpddsforcasting',
  packages = ['jpddsforcasting'], 
  version = '0.1.5',
  description = 'Time Series forcasting pipelines library - Use different market models to forcast time series data',
  author = 'Alaoui Mohamed',
  author_email = 'alaoui.simo@gmail.com',
  url = 'https://github.com/jetpackdata/jpdforcaster/tree/master/python/jpddsforcasting',
  download_url = 'https://github.com/jetpackdata/jpdforcaster/archive/0.1.zip',
  keywords = ['time series', 'forecasting', 'prophet', 'homology', 'machine learning'],
  classifiers = [],
  install_requires=['sklearn','scipy','fbprophet'],
  package_data={'dataset':['*']},
)