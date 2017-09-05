import pipelineforcasting as pplprocess
import toolbox as tb
import pandas as pd

import matplotlib.pyplot as plt


def do_and_plot_forcasting(df,future_period, freq, name, model):
    
    #Launch pipeline
    res = pplprocess.run_forcast(df,future_period, freq, name, model)
    
    #Plot to explore
    plt.figure(1, figsize=(20, 5))
    plt.suptitle(name+'_'+model, fontsize=10)
    plt.xlabel("NRMSE %f" % tb.nrmse_evaluation(df['y'],res.set_index("ds")[:df['ds'].max()]['yhat']))
    
    plt.plot(res['ds'].values, res['yhat'], color="red")
    plt.plot(df['ds'].values, df['y'], color="blue")
    plt.show()

    #Return the original time series and forecasting
    return res

"""
Usage daily forcasting
"""

data1 = pd.read_csv(tb.get_path_file("dataset/jpdDataSetForForcasting-1.csv"))
df1 = pd.DataFrame()
df1['ds'] = data1['ds']
df1['y'] = data1['y']

fdata1sma = do_and_plot_forcasting(df1,40, 'D', 'smatestmodel-1', 'sma')

fdata1prophet = do_and_plot_forcasting(df1,40, 'D', 'prophettestmodel-1', 'prophet')



"""
Usage monthly forcasting
"""
data2 = pd.read_csv(tb.get_path_file("dataset/jpdDataSetForForcasting-2.csv"))
df2 = pd.DataFrame()
df2['ds'] = data2['ds']
df2['y'] = data2['y']

fdata2sma = do_and_plot_forcasting(df2, 12, 'M', 'smatestmodel-2', 'sma')

fdata2prophet = do_and_plot_forcasting(df2,12, 'M', 'prophettestmodel-2', 'prophet')

