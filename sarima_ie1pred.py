import numpy as np
import pandas as pd
from scipy import stats
from matplotlib import pylab as plt
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

import argparse

def get_args():
    psr = argparse.ArgumentParser()
    psr.add_argument('-sd','--startday',default='2005-05-04')#train開始日の指定
    psr.add_argument('-st','--starttime',default='15:30')#train開始時間の指定
    psr.add_argument('-ed','--endday',default='2005-05-09')#train終了日の指定
    psr.add_argument('-et','--endtime',default='15:30')#train終了時間の指定
    psr.add_argument('-i','--input',default='trafficMatrixData.csv')#入力ファイル名
    psr.add_argument('-o','--output',default='sarima_result.csv')#出力ファイル名
    psr.add_argument('-tc','--traincolumn',default='ie1')#SARIMAで予測したいcolumnの指定
    psr.add_argument('-ic','--indexcolumn',default='times')#データのインデックスcolumnの指定
    return psr.parse_args()

# # trafficMatrixData.csv
# times,at1,be1,ch1,cz1,de1,es1,fr1,gr1,hr1,hu1,ie1,il1,it1,lu1,nl1,ny1,pl1,pt1,se1,si1,sk1,uk1,at1Population,be1Population,ch1Population,cz1Population,de1Population,es1Population,fr1Population,gr1Population,hr1Population,hu1Population,ie1Population,il1Population,it1Population,lu1Population,nl1Population,ny1Population,pl1Population,pt1Population,se1Population,si1Population,sk1Population,uk1Population
# 2005-05-04 15:30:00,624.248331,701.385087,7723.848639,588.791084,11277.728707,801.742042,1104.674558,4977.823063,4786.642488,6619.489082,96.598625,371.019586,4782.321282,125.721646,4544.297701,2795.401013,531.295005,1772.898724,3966.450343,5391.613105,98.222923,4281.6726,624,701,7724,589,11278,802,1105,4978,4787,6619,97,371,4782,126,4544,2795,531,1773,3966,5392,98,4282
    


if __name__ == '__main__':

    args = get_args()
    start_day = args.startday
    start_time = args.starttime
    end_day = args.endday
    end_time = args.endtime
    in_file = args.input
    out_file = args.output
    train_column = args.traincolumn
    index_column = args.indexcolumn

    data = pd.read_csv(in_file)
    data.index = data[index_column]

    data = data[train_column]

    train = data[start_day+' '+start_time:end_day+' '+end_time]

    train_acf = sm.tsa.stattools.acf(train, nlags=40)
    train_pacf = sm.tsa.stattools.pacf(train, nlags=40)

    figure = plt.figure(figsize=(14,7))
    ax1 = figure.add_subplot(211)
    figure = sm.graphics.tsa.plot_acf(train_acf, lags=19, ax=ax1)
    ax1.set_title('ACF(traffic)')
    ax2 = figure.add_subplot(212)
    figure = sm.graphics.tsa.plot_pacf(train_pacf, lags=19, ax=ax2)
    ax2.set_title('PACF(traffic)')
    plt.show()

    diff = train - train.shift()
    diff = diff.dropna()

    order = sm.tsa.arma_order_select_ic(diff, ic='aic', trend='nc')
    print(order)

    p = order['aic_min_order'][0]
    q = order['aic_min_order'][1]


    """
    import statsmodels.api as sm
    SARIMA_p_1_q_111 = sm.tsa.SARIMAX(train,
                                    order=(p,1,q), 
                                    seasonal_order=(0,1,1,96), 
                                    enforce_stationarity = False,
                                    enforce_invertibility = False
                                    ).fit()
    """
    max_sp = 3
    max_sd = 1
    max_sq = 3

    pattern = (max_sp +1)*(max_sd+1)*(max_sq+1)
    modelSelection = pd.DataFrame(index=range(pattern), columns=["model", "aic"])
    num=0

    for sp in range(0,max_sp+1):
        for sd in range(0, max_sd + 1):
            for sq in range(0, max_sq + 1):
                sarima = sm.tsa.SARIMAX(
                        train, order=(p,1,q), 
                                    seasonal_order=(sp,sd,sq,96), 
                                    enforce_stationarity = False, 
                                    enforce_invertibility = False
                                ).fit(method='bfgs', maxiter=300, disp=False)
                modelSelection.iloc[num]["model"] = "order=(" + str(p) + ",1,"+ str(q) + "), season=("+ str(sp) + ","+ str(sd) + "," + str(sq) + ")"
                modelSelection.iloc[num]["aic"] = sarima.aic
                num = num + 1
                print(num)

    print(modelSelection)
    print(modelSelection[modelSelection.aic == min(modelSelection.aic)])
    
    # 2022-04-12
    modelSelection.to_csvo(out_file)
