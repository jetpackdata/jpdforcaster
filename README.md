# jpdforcaster
Time Series forcasting pipelines library - Use different market models to forcast time series data

TODO :
-- Add setup.y for piping
(
pip2 install pandas
pip2 install sklearn
pip2 install scipy
pip2 install numpy
pip2 install cython
pip2 install fbprophet
pip2 install pystan
pip2 install fbprophet
pip2 install statsmodels
)

--- How to test

--- see usage.py file

- We suppose inpout date without outlier as a pandas df with 2 columns ds and y
- We can use 2 models :
  - Simple moving average with lag adjustment  (sma)
  - Prophet (stan model curve fitting)  (prophet)
  
- Basic usage :

