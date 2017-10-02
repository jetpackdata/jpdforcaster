# JetPack Data jpdforcaster

jpdforcaster is a time series forcasting pipelines libraries.
Those libraries use different market models to forcast time series data and are based also on some research papers.

Predictive module of jetPack Data platforme use those libraries : https://www.jetpackdata.com

## New Release 0.1.12
```bash
pip install jpddsforcasting --upgrade
```

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

Clean your temporary directory if it needed:

```bash
python -m jpddsforcasting clean
```


## Some details on current version

- We suppose input data without outliers as a pandas df with 2 columns ds and y
- We can use 2 models :
  - Simple moving average with basic lag adjustment  ('sma')
  - Exponential moving average (ewma)
  - Prophet (stan model curve fitting)  ('prophet')
  
> Basic usage :

As input : a pandas data frame as follow :

dataAsDataFrame :
ts
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

config = {
            'id_model': 'my_ewma_for_sales_revenue',
            'model': 'ewma', #or 'sma' or 'prophet'
            'date': tb.get_now(),
            'window_size': 3, #for 'ewma' and 'sma'
            'prediction_conf': {'future_period':24,'freq':'M'},
            'tech_conf': {'clean': True}
        }

#Launch pipeline
res = pplprocess.run_forcast(ts, config)
```

```code
"""This function does the forcasting and return a pandas df with all the historical value
    and predicted one. We have 2 differents mode according to our usage.
    If you need to refit the model, add clean entry to True to the config dict

    Args:
        ts (pandas data frame): ts means time series. There is no a strong 
                                hypthesis on the data frame except an exictence 
                                of a minumum of 2 columns ds (datetime) and y (numeric)

        config (dictionary):    config is a dictionnary with a minimum of 3 entries. 
                                Could have some model dependant entries or optionnal technical entries
            model (string): the model name
            date (datetime): the date of the training as a time staamp with millis
            id_model (string): model indentifier to make the model unique
            prediction_conf (dictionary):
                future_period (int): number of prediction to perform
                freq (string): 'D' for daily, 'M' for monthly, 'Y' for yearly
            tech_conf (dictionary) [optionnal]:
                clean (bool): clean all existing model and refit. This option remove all exixting model.
                              need improvement to perform an ad hoc clean


    Returns:
       forcasted result (pandas data frame):    This function return some new columns in the data frame.
                                                yhat predicted values, yhat_lower and yhat_upper for uncertainty,
                                                trend, seasonnability...to complete
```

### Some precision on model


#### sma & ewma :

- log transformation is used for variance stabilization
- we automaticaly compute residual with an additional model

#### prophet :

- Prophet is a procedure for forecasting time series data. It is based on an additive model where non-linear trends are fit with yearly and weekly seasonality, plus holidays. It works best with daily periodicity data with at least one year of historical data. Prophet is robust to missing data, shifts in the trend, and large outliers.

- Enought robust to use it for augmented machine learning

## Usefull link for forcasting

- Facebook library : https://facebookincubator.github.io/prophet/
- Forcasting & machine lerning : https://machinelearningmastery.com


