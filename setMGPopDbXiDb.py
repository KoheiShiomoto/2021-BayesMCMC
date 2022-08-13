#人口の平滑化を行うプログラム
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15,10
import datetime
import argparse

import sys

from common.tools import mkdir

def get_args():
    psr = argparse.ArgumentParser()
    # psr.add_argument('-a','--apd',action='store_true')#平滑化を行うかどうか
    psr.add_argument("-od", "--output", type=str, default="output")  # 結果出力先ディレクトリ
    psr.add_argument('-i','--inTrfMtxFileName', default='output/trafficData_internet_1104_1117.csv', help='File name of Input Traffic Matrix data')  
    psr.add_argument('--alpha', type=float, default=0.01, help='coefficient of exponential smoothing')  
    psr.add_argument('--xiBase', type=float, default=1.0, help='activity factor at peak hour')  
    psr.add_argument('-o','--outFileName', default='output/popData_internet_1104_1117.csv', help='File name of Output data')  
    psr.add_argument('-oXi','--outXiFileName', default='output/xiData_internet_1104_1117.csv', help='File name of Output Xi data')  
    #
    # default start time is '2013-11-03 23:00'
    # default end   time is '2013-11-17 22:50'
    psr.add_argument("-s", "--startdate", type=str, default="2013-11-01")  # 開始日の選択
    psr.add_argument("-e", "--enddate", type=str, default="2013-12-31")  # 終了日の選択
    return psr.parse_args()


if __name__ == '__main__':
    args = get_args()
    alpha = args.alpha
    xiBase = args.xiBase
    output = args.output
    mkdir(output)
    outFileName = args.output+"/"+args.outFileName
    outXiFileName = args.output+"/"+args.outXiFileName
    inTrfMtxFileName = args.output+"/"+args.inTrfMtxFileName
    data = pd.read_csv(inTrfMtxFileName, header=0)
    tt0 = datetime.datetime.strptime(args.startdate, "%Y-%m-%d")
    tt1 = datetime.datetime.strptime(args.enddate, "%Y-%m-%d")
    t0 = datetime.datetime(tt0.year, tt0.month, tt0.day, 00, 00, 0, 0)
    t1 = datetime.datetime(tt1.year, tt1.month, tt1.day, 23, 59, 59, 59)
    print(f'# start time is {t0}.')
    print(f'# end time is {t1}.')
    t0str = t0.strftime('%Y-%m-%d %H:%M:%S')
    t1str = t1.strftime('%Y-%m-%d %H:%M:%S')
    print(f'# start time is {t0str}.')
    print(f'# end time is {t1str}.')

    xi = data['Normalized Sum (total)']  # activity factor is computed from the normalized total traffic volume
    xi.index=data['time']
    listOfAllCells = [f'cell{i:05}' for i in range(1,10001)]
    for cell in listOfAllCells:
        # data[cell] = data[cell] / (data['Normalized Sum (total)'])  # population obtained by dividing by adjusted activity factor
        data[cell] = data[cell] / (xiBase*data['Normalized Sum (total)']) # population obtained by dividing by adjusted activity factor
    data.index=data['time']
    # data = data[t0str:t1str].ewm(span=10).mean()
    data = data[t0str:t1str].ewm(alpha=alpha).mean()
    xi *= xiBase
    # xi = xi[t0str:t1str].ewm(span=10).mean()
    xi = xi[t0str:t1str].ewm(alpha=alpha).mean()

    #
    # milano grid traffic data
    # trafficData_internet_1104_1117.csv
    # time,Normalized Sum (total),Sum (total),cell04259,cell04456,cell05060,cell05200,cell05085,cell04703
    # 2013-11-03 23:00:00,0.5560133731168918,589247.9261802054,164.54480015570186,724.1616341721386,143.1902454320498,51.51321121658152,14.019635271759675,1.6079584682686865

    # if(args.apd): # 平滑化する場合は元トラフィックデータはMb/s単位で表記されており、ユーザあたり1Mb/sで送信していると仮定して指数平滑を行う。
    if(True): # 平滑化する場合は元トラフィックデータはMb/s単位で表記されており、ユーザあたり1Mb/sで送信していると仮定して指数平滑を行う。
        data_ev = data
        #
        indexDatetime = data.index
        isMidnight = False
        for i in range(1,len(data)):
            # tmp = alpha*data.iloc[i]+(1-alpha)*data_ev.iloc[i-1]
            tmp = data.iloc[i]
            #
            xi_tmp = xi.iloc[i]  # population obtained by dividing by activity factor
            #
            # start of midnight adjustment
            hour = datetime.datetime.strptime(indexDatetime[i], '%Y-%m-%d %H:%M:%S').hour # 2013-11-03 23:10:00
            if isMidnight == False :  # Daytime
                if hour >= 23 : # Start of Midnight
                    isMidnight = True
                    popMidnight = tmp
                    xiMidnight = xi_tmp
            else : # Midnight
                if hour >= 6 : # Daytime
                    isMidnight = False
                else: # Midnight
                    xi_tmp = 1.0*xiMidnight*(tmp/popMidnight)
                    tmp = popMidnight
            # end of midnight adjustment
            #
            data_ev[i] = tmp
            xi[i] = xi_tmp
        #
        # 2022-02-08
        data_ev = round(data_ev)
        #
        data_ev.fillna(0).astype('int', errors='ignore')
        # data_ev.astype('int')
        data_ev.to_csv(
            outFileName,
            header=True)  
    else: # 平滑化しない場合はユーザあたり1Mb/sで送信していると仮定して丸めたものを人口とする。
        data.fillna(0).astype('int', errors='ignore')
        data.astype('int')
        data.to_csv(outFileName)  
    #
    # print(xi)
    xi.to_csv(
        outXiFileName,
        header=True)  
    #
