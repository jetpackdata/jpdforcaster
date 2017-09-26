from distutils.core import setup

setup(
  name = 'jpddsforcasting',
  packages = ['jpddsforcasting'], 
  package_data={'jpddsforcasting': ['dataset/*.csv']},
  version = '0.1.11',
  description = 'Time Series forcasting pipelines library - Use different market models to forcast time series data',
  author = 'Alaoui Mohamed',
  author_email = 'alaoui.simo@gmail.com',
  url = 'https://github.com/jetpackdata/jpdforcaster/tree/master/python/jpddsforcasting',
  download_url = 'https://github.com/jetpackdata/jpdforcaster/archive/0.1.zip',
  keywords = ['time series', 'forecasting', 'prophet', 'homology', 'machine learning'],
  install_requires=['sklearn','scipy','fbprophet'],
  #Show usage properly
  entry_points={
    'console_scripts': ['jpddsforcasting = jpddsforcasting.usage:main'],
  },
  classifiers=[
          'Development Status :: 1 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python 2.7',
          'Programming Language :: Python 3',
          'Topic :: Communications :: Email',
          ],
)
