# jpdforcaster
Time Series forcasting pipelines library - Use different market models to forcast time series data

TODO :
-- Add setup.y for piping

pip2 install pandas
pip2 install sklearn
pip2 install scipy
pip2 install numpy
pip2 install cython
pip2 install fbprophet
pip2 install pystan
pip2 install fbprophet
pip2 install statsmodels


--- How to test

--- see usage.py file

- We suppose inpout data without outlier as a pandas df with 2 columns ds and y
- We can use 2 models :
  - Simple moving average with lag adjustment  (sma)
  - Prophet (stan model curve fitting)  (prophet)
  
- Basic usage :

import pipelineforcasting as pplprocess
#Launch pipeline
res = pplprocess.run_forcast(df,future_period, freq, name, model)

If the model is stored we use it, if not we do a new fit. name should be unique (this behaviour will be improved)

  - future_period : number of value to forcaste
  
  - frequency : daily : 'D', monthly : 'M', yearly : 'Y'....according to the time series...This value is not yet infered
  
  - name : model identifier
  
  - model : model to use 'sma' or 'prophet'


- Some precision on model

-sma :

sma window is fixed now to 10, we can't infer yet the best window size...It will be done on the fit part later or passed as an input from the client.

As with a window size of 10 we do a multi step time series forcasting, this model will be very bad id the future period to forcast is biffer than 10 as we will forget the trained model.

Additionnaly to this, we do not yet add some pertinent transformation to improve the time series signal for forcasting (as log transformation, shifting).

Seasonability, trend and holiday is not taken into account yet.


-prophet :
todo
