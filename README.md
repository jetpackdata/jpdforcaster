# JetPack Data jpdforcaster

jpdforcaster is a time series forcasting pipelines libraries.
Those libraries use different market models to forcast time series data and are based also on some research papers.
Predictive module of jetPack Data platforme use those libraries

## How to setup

In near future use pip :
```bash
pip install jpdforcaster
```

Currently :

clone the repository and install some dependency :

```bash
pip install pandas
pip install sklearn
pip install scipy
pip install numpy
pip install cython
pip install fbprophet
pip install pystan
pip install fbprophet
pip install statsmodels
```




## How to test
Some tests are implemented in jpdforcaster/tests

```bash
python test_toolbox.py
```

## Get started

Documentation is under generation
jpdforcaster/usage.py

To see some results you can execute :

```bash
python usage.py
```


## Some précision for current version

- We suppose inpout data without outlier as a pandas df with 2 columns ds and y
- We can use 2 models :
  - Simple moving average with lag adjustment  (sma)
  - Prophet (stan model curve fitting)  (prophet)
  
> Basic usage :

```python
import pipelineforcasting as pplprocess
#Launch pipeline
res = pplprocess.run_forcast(df,future_period, freq, name, model)
'''

> If the model is stored we use it, if not we do a new fit. name should be unique (this behaviour will be improved)

  - future_period : number of value to forcaste
  
  - frequency : daily : 'D', monthly : 'M', yearly : 'Y'....according to the time series...This value is not yet infered
  
  - name : model identifier
  
  - model : model to use 'sma' or 'prophet'


### Some precision on model

#### sma :

- sma window is fixed now to 10, we can't infer yet the best window size...It will be done on the fit part later or passed as an input from the client.

- As with a window size of 10 we do a multi step time series forcasting, this model will be very bad if the future period to forcast is biger than 10 as we will forget the trained model.

- Additionnaly to this, we do not yet add some pertinent transformations to improve the time series signal for forcasting (as log transformation, shifting).....todo

- Seasonability, trend and holiday is not taken into account yet. Input signal is considered stationary.


#### prophet :

- Prophet is a procedure for forecasting time series data. It is based on an additive model where non-linear trends are fit with yearly and weekly seasonality, plus holidays. It works best with daily periodicity data with at least one year of historical data. Prophet is robust to missing data, shifts in the trend, and large outliers.

## Usefull link for forcasting

- Facebook library : https://facebookincubator.github.io/prophet/
- Forcasting & machine lerning : https://machinelearningmastery.com


