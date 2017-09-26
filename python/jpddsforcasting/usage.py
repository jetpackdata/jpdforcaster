import logging
import sys

import matplotlib.pyplot as plt
import pandas as pd

import jpddsforcasting.pipelineforcasting as pplprocess
import jpddsforcasting.toolbox as tb

logger = logging.getLogger(__name__)


def do_and_plot_forcasting(df, future_period, freq, config):

    # Launch pipeline
    forecast_data = pplprocess.run_forcast(df, future_period, freq, config)

    # Prepare viz data
    viz_df = forecast_data[['yhat', 'yhat_lower',
                            'yhat_upper']].join(df, how='outer')

    viz_df['ds'] = forecast_data['ds']
    viz_df.set_index('ds', inplace=True)

    last_date = df['ds'].max()

    # Mask to connect origin and forcasted data
    msk = (viz_df.index >= last_date)
    orig_msk = (viz_df.index < last_date)

    # filtre on msk
    predict_df = viz_df.loc[msk]
    orig_df = viz_df.loc[orig_msk]

    # error
    cvrmse = tb.cv_rmse_evaluation(orig_df.y, orig_df.yhat)

    # Now...plot everything
    plt.rcParams['figure.figsize'] = (10, 5)
    plt.style.use('ggplot')

    fig, ax1 = plt.subplots()
    ax1.plot(viz_df.y, color='black')
    ax1.plot(viz_df.yhat, color='red')
    #ax1.plot(predict_df.yhat, color='red')
    ax1.fill_between(
        predict_df.index, predict_df['yhat_upper'], predict_df['yhat_lower'], alpha=0.2, color='darkred')
    ax1.set_title(
        'Origine vs Forecast (in Blue with cvrmse ' + str(cvrmse) + ')')
    ax1.set_ylabel('Origine unit')
    ax1.set_xlabel('Date')

    # change the legend text
    L = ax1.legend()
    L.get_texts()[0].set_text('Actual')
    L.get_texts()[1].set_text('Forecasted')

    plt.show()

    # Return the viz dataframe
    return viz_df


def main():
    # if with clean
    if len(sys.argv) > 1:
        if sys.argv[1] == 'clean':
            print("Clean all existing model")
            tb.clean_stored_model()
        else:
            logger.info("Usage without args or clean")
    elif len(sys.argv) == 1:

        data1 = pd.read_csv(tb.get_path_file(
            "dataset/jpdDataSetForForcasting-1.csv"))
        df1 = pd.DataFrame()
        df1['ds'] = data1['ds']
        df1['y'] = data1['y']

        data2 = pd.read_csv(tb.get_path_file(
            "dataset/jpdDataSetForForcasting-2.csv"))
        df2 = pd.DataFrame()
        df2['ds'] = data2['ds']
        df2['y'] = data2['y']

        data3 = pd.read_csv(tb.get_path_file(
            "dataset/HistoricalQuotesNASDACQ.csv"))
        df3 = pd.DataFrame()
        df3['ds'] = data3['date']
        df3['y'] = data3['volume']

        
        conf1sma = {
            'id_model' : 'smatestmodel-1',
            'model' : 'sma',
            'date' : tb.get_now(),
            'window_size' : 3,
            'tech_conf': {'clean': True} 
            }
        
        conf1prophet = {
            'id_model' : 'prophettestmodel-1',
            'model' : 'prophet',
            'date' : tb.get_now(),
            'tech_conf': {'clean': True}
            } 
            
        conf1ewma = {
            'id_model' : 'ewmatestmodel-1',
            'model' : 'sma',
            'date' : tb.get_now(),
            'window_size' : 3,
            'tech_conf': {'clean': True} 
            }

        conf2sma = {
            'id_model': 'smatestmodel-2',
            'model': 'sma',
            'date': tb.get_now(),
            'window_size': 3,
            'tech_conf': {'clean': True}
        }
    
        conf2prophet = {
            'id_model': 'prophettestmodel-2',
            'model': 'prophet',
            'date': tb.get_now(),
            'tech_conf': {'clean': True}
        }
            
        conf2ewma = {
            'id_model': 'ewmatestmodel-2',
            'model': 'ewma',
            'date': tb.get_now(),
            'window_size': 6,
            'tech_conf': {'clean': True}
        }

        res2prophet = do_and_plot_forcasting(df2, 24, 'M', conf2sma)
        res2sma = do_and_plot_forcasting(df2, 24, 'M', conf1prophet)
        res1prophet = do_and_plot_forcasting(df2, 24, 'M', conf1ewma)
