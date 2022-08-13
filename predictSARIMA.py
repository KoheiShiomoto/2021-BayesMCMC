import sys
import argparse

import datetime

import numpy as np
import pandas as pd
from scipy import stats
from matplotlib import pylab as plt
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

from common.tools import mkdir

def get_args():
    psr = argparse.ArgumentParser()

    psr.add_argument("-s_train", "--startdate_train", type=str, default="2013-11-04")  # 開始日(train)の選択
    psr.add_argument("-e_train", "--enddate_train", type=str, default="2013-11-10")  # 終了日(train)の選択
    psr.add_argument("-s_test", "--startdate_test", type=str, default="2013-11-11")  # 開始日(test)の選択
    psr.add_argument("-e_test", "--enddate_test", type=str, default="2013-11-17")  # 終了日(test)の選択
    #
    psr.add_argument("-od", "--output", type=str, default="output")  # 結果出力先ディレクトリ
    psr.add_argument('-f','--inFileName',default='info_internet_Original_1104_1117_cell04259.csv', help='File name of Input data')  
    psr.add_argument('-o','--outFileName',default='resultSARIMA_internet_SingleOriginal_1104_1117_cell04259.csv', help='File name of Output data')  
    #
    psr.add_argument('-c','--lengthCycle', type=int, default=1, help='length of cycle in terms of days')  
    psr.add_argument('-sp','--sampleRate', type=int, default=6, choices=[1, 2, 3, 6, 12, 18, 24], help='sample rate to reduce the number of epochs in the cycle')  
    return psr.parse_args()

# # trafficData_internet_1104_1110_cell04259.csv
# time,cell04259
# 2013-11-04 00:00:00,120.55095348513927
# 2013-11-04 00:10:00,152.20242458870763
# 2013-11-04 00:20:00,126.8777550632817



# "infoOriginal_internet_1104_1110_cell": time,pop,traffic,CPU,MEM
# "resultSARIMA_internet_1104_1110_cell": time,predicted-traffic

if __name__ == '__main__':

    args = get_args()
    #
    odir = args.output
    mkdir(odir)
    inFileName = odir+"/"+args.inFileName
    outFileName = odir+"/"+args.outFileName
    print(inFileName)
    print(outFileName)
    lengthCycle = args.lengthCycle
    sampleRate = args.sampleRate
    #
    # train period
    # 2013-11-04 00:00:00
    # 2013-11-10 23:50:00
    tt0_train = datetime.datetime.strptime(args.startdate_train, "%Y-%m-%d")
    tt1_train = datetime.datetime.strptime(args.enddate_train, "%Y-%m-%d")
    t0_train = datetime.datetime(tt0_train.year, tt0_train.month, tt0_train.day, 00, 00, 0, 0)
    t1_train = datetime.datetime(tt1_train.year, tt1_train.month, tt1_train.day, 23, 50, 0, 0)
    #
    print(f'# train start time is {t0_train}.')
    print(f'# train end time is {t1_train}.')
    t0_train_str = t0_train.strftime('%Y-%m-%d %H:%M:%S')
    t1_train_str = t1_train.strftime('%Y-%m-%d %H:%M:%S')
    print(f'# train start time is {t0_train_str}.')
    print(f'# train end time is {t1_train_str}.')
    #
    # test period
    # 2013-11-11 00:00:00
    # 2013-11-17 23:50:00
    tt0_test = datetime.datetime.strptime(args.startdate_test, "%Y-%m-%d")
    tt1_test = datetime.datetime.strptime(args.enddate_test, "%Y-%m-%d")
    t0_test = datetime.datetime(tt0_test.year, tt0_test.month, tt0_test.day, 00, 00, 0, 0)
    t1_test = datetime.datetime(tt1_test.year, tt1_test.month, tt1_test.day, 23, 50, 0, 0)
    #
    print(f'# test start time is {t0_test}.')
    print(f'# test end time is {t1_test}.')
    t0_test_str = t0_test.strftime('%Y-%m-%d %H:%M:%S')
    t1_test_str = t1_test.strftime('%Y-%m-%d %H:%M:%S')
    print(f'# test start time is {t0_test_str}.')
    print(f'# test end time is {t1_test_str}.')
    

    data = pd.read_csv(inFileName)
    data.index = data['time']
    # data = data[train_column]
    data = data['traffic']
    ts_train = data[t0_train_str:t1_train_str]
    ts_test = data[t0_test_str:t1_test_str]
    ts_train = ts_train[1::sampleRate]
    ts_test = ts_test[1::sampleRate]
    print("ts_train")
    print(ts_train)
    print("ts_test")
    print(ts_test)
    #

    train_acf = sm.tsa.stattools.acf(ts_train, nlags=40)
    train_pacf = sm.tsa.stattools.pacf(ts_train, nlags=40)

    # 2022-06-02
    # comment out
    #
    # figure = plt.figure(figsize=(14,7))
    # ax1 = figure.add_subplot(211)
    # figure = sm.graphics.tsa.plot_acf(train_acf, lags=19, ax=ax1)
    # ax1.set_title('ACF(traffic)')
    # ax2 = figure.add_subplot(212)
    # figure = sm.graphics.tsa.plot_pacf(train_pacf, lags=19, ax=ax2)
    # ax2.set_title('PACF(traffic)')
    # plt.show()

    diff = ts_train - ts_train.shift()
    diff = diff.dropna()

    order = sm.tsa.arma_order_select_ic(diff, ic='aic', trend='nc')
    print(f"order is {order}.")

    p = order['aic_min_order'][0]
    q = order['aic_min_order'][1]
    print(f"p is {p}, q is {q}.")
    #
    # order=(p,1,q), 
    # # seasonal_order=(0,1,1,96), 
    # seasonal_order=(0,1,1,144), 
    #
    """
    import statsmodels.api as sm
    SARIMA_p_1_q_111 = sm.tsa.SARIMAX(ts_train,
                                    order=(p,1,q), 
                                    seasonal_order=(0,1,1,144), 
                                    enforce_stationarity = False,
                                    enforce_invertibility = False
                                    ).fit()
    """
    max_sp = 3
    max_sd = 1
    max_sq = 3

    pattern = (max_sp +1)*(max_sd+1)*(max_sq+1)
    modelSelection = pd.DataFrame(index=range(pattern), columns=["model", "aic","p","q","sp","sd","sq"])
    num=0

    
    numPoints = 6*24*lengthCycle/sampleRate
    print(f"lengthCycle is {lengthCycle}.")
    print(f"sampleRate is {sampleRate}.")
    print(f"numPoints is {numPoints}.")
    # 168 points are included in a cycle. 1*24*7 = 24*7 =168, sample 1 out of 6
    # 1008 points are included in a cycle. 6*24*7 = 144*7 =1008, full sample
    # if lengthCycle == 7 : # if 1 cycle is 7 days, sample 1 out of 6
    #     numPoints = 168
    #     # 168 points are included in a cycle. 1*24*7 = 24*7 =168, sample 1 out of 6
    #     # # 1008 points are included in a cycle. 6*24*7 = 144*7 =1008, full sample
    # else : # otherwise, full sample
    #     numPoints = 144
    #     # 144 points are included in a cycle. 6*24 = 144, full sample
    #     # # 24 points are included in a cycle. 1* 24 = 24, sample 1 out of 6
    for sp in range(0,max_sp+1):
        for sd in range(0, max_sd + 1):
            for sq in range(0, max_sq + 1):
                model = sm.tsa.SARIMAX(ts_train, order=(p,1,q), 
                                       seasonal_order=(sp,sd,sq,numPoints),
                                       enforce_stationarity = False, 
                                       enforce_invertibility = False)
                result = model.fit(method='bfgs', maxiter=300, disp=False)
                modelSelection.iloc[num]["model"] = "order=(" + str(p) + ",1,"+ str(q) + "), season=("+ str(sp) + ","+ str(sd) + "," + str(sq) + ")"
                modelSelection.iloc[num]["aic"] = result.aic
                modelSelection.iloc[num]["p"] = p
                modelSelection.iloc[num]["q"] = q
                modelSelection.iloc[num]["sp"] = sp
                modelSelection.iloc[num]["sd"] = sd
                modelSelection.iloc[num]["sq"] = sq
                num = num + 1

    print(modelSelection)
    print(modelSelection[modelSelection.aic == min(modelSelection.aic)])

    idx = modelSelection.index[modelSelection.aic == min(modelSelection.aic).tolist()]
    i = idx[0]
    p = modelSelection.iloc[i]["p"]
    q = modelSelection.iloc[i]["q"]
    sp = modelSelection.iloc[i]["sp"]
    sd = modelSelection.iloc[i]["sd"]
    sq = modelSelection.iloc[i]["sq"]
    print(f"i={i}")
    print(f"p={p}, q={q}, sp={sp}, sd={sd}, sq={sq}")
    model = sm.tsa.SARIMAX(ts_train, order=(p,1,q), 
                           seasonal_order=(sp,sd,sq,numPoints),
                           enforce_stationarity = False, 
                           enforce_invertibility = False
    )
    result = model.fit(method='bfgs', maxiter=300, disp=False)

    #
    # 2022-06-04
    # df_tmp = result.predict(start=t0_train_str, end=t1_test_str)
    #
    train_pred = result.predict()
    print(train_pred)
    test_pred = result.forecast(len(ts_test))
    print(test_pred)
    test_pred_ci = result.get_forecast(len(ts_test)).conf_int()
    df_tmp = pd.concat([train_pred, test_pred], axis=0)
    #
    # 2022-06-02
    # Recover the original time series data given at 10 min intervals, filling in the intervals generated by sampling
    df = df_tmp.asfreq("10min")
    # 2022-06-04
    # replace NaN with blank
    df = df.fillna("")
    # df = df_tmp.asfreq("10min").fillna("")  # if we want to remove nan, please un-comment out
    #
    # # # Freq: 10T, Name: predicted_mean, Length: 1002, dtype: float64
    # # df.rename(columns={'A': 'Col_1'}, index={'ONE': 'Row_1'}, inplace=True)
    # # !!! this does not work because the df has only one column
    # df.rename(columns={'predicted_mean': 'predicted-traffic(SARIMA)'}, inplace=True)
    print(df)
    df.to_csv(outFileName,index=False)
