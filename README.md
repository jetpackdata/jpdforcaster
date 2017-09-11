# JetPack Data jpdforcaster

jpdforcaster is a time series forcasting pipelines libraries.
Those libraries use different market models to forcast time series data and are based also on some research papers.

Predictive module of jetPack Data platforme use those libraries : https://www.jetpackdata.com

## New Release 0.1.10
```bash
pip install jpddsforcasting --upgrade
```
- Make the lib work with python3

## How to setup

```bash
pip install jpddsforcasting
```

## Get started

Documentation is under generation :


## Quick usage

To see some results :

```bash
python -m jpddsforcasting
```
A window will appear with some forcasting.

Clean your temporary directory :

```bash
python -m jpddsforcasting clean
```


## Some details on current version

- We suppose input data without outliers as a pandas df with 2 columns ds and y
- We can use 2 models :
  - Simple moving average with basic lag adjustment  ('sma')
  - Prophet (stan model curve fitting)  ('prophet')
  
> Basic usage :

As input : a pandas data frame as follow :

dataAsDataFrame :
```
ds,y
2012-05-01,28.23
2012-05-02,18.23
2012-05-03,32.23
2012-05-04,38.23
2012-05-05,45.23
2012-05-06,50.03
2012-05-07,38.23
2012-05-08,39.03
2012-05-09,8.23
2012-05-10,9.03
2012-05-11,15.23
2012-05-12,32.03
2012-05-13,25.03
2012-05-14,34.03
```

dataAsDataFrame should be clean with the right frequency :

```python
import pipelineforcasting as pplprocess
#Launch pipeline
res = pplprocess.run_forcast(dataAsDataFrame, future_period=10, freq='D', name="myYearlySalesRevenues", "sma")
```

> If the model is stored we use it, if not we do a new fit. name should be unique (this behaviour will be improved)

  - future_period : number of value to forcast
  
  - frequency : daily : 'D', monthly : 'M', yearly : 'Y'....according to the time series...This value is not yet infered
  
  - name : model identifier
  
  - model : model to use 'sma' or 'prophet'


### Some precision on model

#### sma :

- sma window is fixed now to 10, we can't infer yet the best window size...It will be done on the fit part later or passed as an input from the client.

- As with a window size of 10 we do a multi step time series forcasting, this model will be very bad if the future period to forcast is bigger than 10 as we will forget the trained model.

- Additionnaly to this, we do not yet add some pertinent transformations to improve the time series signal for forcasting (as log transformation, shifting).....todo

- Seasonability, trend and holiday is not taken into account yet. Input signal is considered stationary...Wich is not the case in the real life

- This model could be use for basic forecasting to detect some singular event or to analyse  a trend or some up/down barrier


#### prophet :

- Prophet is a procedure for forecasting time series data. It is based on an additive model where non-linear trends are fit with yearly and weekly seasonality, plus holidays. It works best with daily periodicity data with at least one year of historical data. Prophet is robust to missing data, shifts in the trend, and large outliers.

- Enought robust to use it for augmented machine learning

## Usefull link for forcasting

- Facebook library : https://facebookincubator.github.io/prophet/
- Forcasting & machine lerning : https://machinelearningmastery.com


