#単一クラスとしてみた際のグラフ化
#cオプション(1 or 2)でクラス指定，-rオプション（引数なし）で相対誤差の出力

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from matplotlib import ticker
import argparse

import matplotlib.dates as mdates

from common.tools import mkdir

rcParams['font.size'] = 20

def get_args():
    psr = argparse.ArgumentParser()
    psr.add_argument("-od", "--output", type=str, default="output")  # 結果出力先ディレクトリ
    psr.add_argument("-pd", "--picdir", type=str, default="pic")  # 結果出力先ディレクトリ
    psr.add_argument("-Xi", "--prefixXiFileName", type=str, default="xiData_internet_1104_1110")  # 入力のXiファイル名
    psr.add_argument('--resultFileName', default='resultSARIMA_internet_SingleOriginal_1104_1117_cell04259.csv', help='File name of Output data')  
    psr.add_argument("-pI", "--prefixOfInfoFileName", type=str, default="info_internet_Original_1104_1110_cell04259")  # エリア毎の入力ファイル名
    psr.add_argument('--inFileName', default='info_internet_Original_1104_1117_cell04259.csv', help='File name of Input data')  
    psr.add_argument('--pjName', default='test', help='ProjectName')  
    psr.add_argument('-r','--relative',action='store_true',help='output relative error graph')
    #
    psr.add_argument("-s", "--startdate", type=str, default="2013-11-01")  # 開始日の選択
    psr.add_argument("-e", "--enddate", type=str, default="2013-12-31")  # 終了日の選択
    psr.add_argument("--ymaxTraffic", type=float, default=1500.0)  # トラフィックのグラフの最大値
    psr.add_argument("--ymaxPopulation", type=int, default=10000)  # トラフィックのグラフの最大値
    psr.add_argument('-sA', '--switchSARIMA', action='store_true')
    psr.add_argument("-pR1", "--prefixOfResult1FileName", type=str, default="result_internet_SingleOriginal_1104_1110_cell04259")  # エリア毎の結果ファイル名 Proposed
    psr.add_argument("-pR2", "--prefixOfResult2FileName", type=str, default="resultSARIMA_OneDayCycle_internet_SingleOriginal_1104_1117_cell04259")  # エリア毎の結果ファイル名 SARIMA (day)
    psr.add_argument("-pR3", "--prefixOfResult3FileName", type=str, default="resultSARIMA_internet_SingleOriginal_1104_1117_cell04259")  # エリア毎の結果ファイル名 SARIMA (week)

    return psr.parse_args()

def plotSingleResult3Graphs(prefixXiFilename,
                            prefixInputDataFilename,
                            keyInputDataFilename,
                            prefixResult1Filename,
                            prefixResult2Filename,
                            prefixResult3Filename,
                            keyResult1Filename,
                            keyResult2Filename,
                            keyResult3Filename,
                            labelResult1,
                            labelResult2,
                            labelResult3,
                            title,
                            ymax,
                            xlabel,
                            ylabel,
                            t0,
                            t1,
                            pjName="pjName",
                            scaleXi=1.0,
                            key="time",
                            odir="output",
                            picdir="pic"):
    fig, ax = plt.subplots(figsize=(12, 9),sharex=True, sharey=True) 
    key1 = keyInputDataFilename
    keyResult1 = keyResult1Filename
    keyResult2 = keyResult2Filename
    keyResult3 = keyResult3Filename
    # XiData
    prefix = prefixXiFilename
    fileName = odir+ "/" +prefix+ ".csv"
    df0 = pd.read_csv(fileName, header=0)
    df0["Normalized Sum (total)"] *= scaleXi
    # inputTrafficData
    prefix = prefixInputDataFilename
    fileName = odir+ "/" +prefix+ ".csv"
    df1 = pd.read_csv(fileName, header=0)
    df1 = df1.drop(key, axis=1)
    # result1 Data
    prefix1 = prefixResult1Filename
    fileName = odir+ "/" +prefix1+ ".csv"
    df_result1 = pd.read_csv(fileName, header=0)
    #
    # result2 Data
    prefix2 = prefixResult2Filename
    fileName = odir+ "/" +prefix2+ ".csv"
    df_result2 = pd.read_csv(fileName, header=0, skiprows=1, names=[keyResult2])
    #
    # result3 Data
    prefix3 = prefixResult3Filename
    fileName = odir+ "/" +prefix3+ ".csv"
    df_result3 = pd.read_csv(fileName, header=0, skiprows=1, names=[keyResult3])
    #
    #
    data = pd.concat([df0, df1, df_result1, df_result2, df_result3], axis=1) # axis=1は横方向の連結　axis=0は縦方向
    #
    #
    data[key] = pd.to_datetime(data[key], format="%Y-%m-%d %H:%M:%S") # 2005-05-04 15:30:00
    data = data[data[key] > t0]
    data = data[data[key] < t1]
    data.index = data[key]
    print(data)
    #
    ax.plot(data.index,data[key1],label="Original", color="blue", linestyle="-", marker=".", markevery=10) # marker=None, ".", ",", "o", "^", "v", "<", ">"
    ax.plot(data.index,data[keyResult1],label=labelResult1, color="red", linestyle="-", marker=None) # marker=None, ".", ",", "o", "^", "v", "<", ">"
    ax.plot(data.index,data[keyResult2],label=labelResult2, color="green", linestyle=":", marker=None) # marker=None, ".", ",", "o", "^", "v", "<", ">"
    ax.plot(data.index,data[keyResult3],label=labelResult3, color="green", linestyle=":", marker=None) # marker=None, ".", ",", "o", "^", "v", "<", ">"
    #
    ax.set_ylim(0,ymax)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))
    ax.axes.set_xlabel(xlabel)
    ax.axes.set_ylabel(ylabel)
    #
    ax.legend()
    #
    ghFileName = picdir+ "/" +pjName+title.replace(' ','')+ "-OrgPrd.pdf"
    plt.savefig(ghFileName)
    plt.show()
    

if __name__ == '__main__':
    args = get_args()
    odir = args.output
    mkdir(odir)
    picdir = args.picdir
    mkdir(picdir)
    inFileName = odir+"/"+args.inFileName
    resultFileName = odir+"/"+args.resultFileName
    print(inFileName)
    print(resultFileName)
    pjName = args.pjName
    p = pd.read_csv(resultFileName)
    d = pd.read_csv(inFileName)
    #
    df_1 = pd.concat([d,p], axis=1) 
    df_1.index = df_1['time']
    df_1.index = pd.to_datetime(df_1.index)
    fig,ax = plt.subplots(1,1,figsize=(12,9),sharex=True,sharey=True)
    ax.plot(df_1.index,df_1['traffic'],label='actual')
    ax.plot(df_1.index,df_1['predicted_mean'],label='predicted (SARIMA)')
    plt.xlabel("Time")
    plt.ylabel("Traffic volume (Mbps)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"pic/{pjName}_ActualPredictedTraffic.pdf")
    plt.show()


    #
    #
    # 2013-11-03 23:00:00
    tt0 = datetime.datetime.strptime(args.startdate, "%Y-%m-%d")
    tt1 = datetime.datetime.strptime(args.enddate, "%Y-%m-%d")
    # # 2018-02-01 12:15:30.002000
    t0 = datetime.datetime(tt0.year, tt0.month, tt0.day, 00, 00, 0, 0)
    t1 = datetime.datetime(tt1.year, tt1.month, tt1.day, 23, 59, 59, 59)
    #
    print(f'# start time is {t0}.')
    print(f'# end time is {t1}.')
    t0str = t0.strftime('%Y-%m-%d %H:%M:%S')
    t1str = t1.strftime('%Y-%m-%d %H:%M:%S')
    print(f'# start time is {t0str}.')
    print(f'# end time is {t1str}.')
    ymaxTraffic = args.ymaxTraffic
    ymaxPopulation = args.ymaxPopulation
    print(ymaxTraffic)
    prefixXiFileName = args.prefixXiFileName
    print(prefixXiFileName)
    prefixOfInfoFileName = args.prefixOfInfoFileName
    print(prefixOfInfoFileName)
    prefixOfResult1FileName = args.prefixOfResult1FileName
    print(prefixOfResult1FileName)
    prefixOfResult2FileName = args.prefixOfResult2FileName
    print(prefixOfResult2FileName)
    prefixOfResult3FileName = args.prefixOfResult3FileName
    print(prefixOfResult3FileName)

    ###########################
    ###########################
    ###########################
    if args.switchSARIMA :
        prefix0=prefixXiFileName
        prefix1=prefixOfInfoFileName
        prefixResult1=prefixOfResult1FileName
        prefixResult2=prefixOfResult2FileName
        prefixResult3=prefixOfResult3FileName
        key1="traffic"
        keyResult1="predicted-traffic"
        keyResult2="SARIMA (day)"
        keyResult3="SARIMA (week)"
        plotSingleResult3Graphs(odir=odir,
                                picdir=picdir,
                                title="Traffic Rate",
                                prefixXiFilename = prefix0,
                                prefixInputDataFilename = prefix1,
                                keyInputDataFilename = key1,
                                prefixResult1Filename = prefixResult1,
                                prefixResult2Filename = prefixResult2,
                                prefixResult3Filename = prefixResult3,
                                keyResult1Filename = keyResult1,
                                keyResult2Filename = keyResult2,
                                keyResult3Filename = keyResult3,
                                labelResult1 = "Proposed",
                                labelResult2 = "SARIMA (day)",
                                labelResult3 = "SARIMA (week)",
                                pjName = "ProposedVsSarima",
                                ymax = ymaxTraffic,
                                key = "time",
                                xlabel = "Time",
                                ylabel = "Traffic Rate [Mbps]",
                                t0 = t0,
                                t1 = t1)
    ###########################
    ###########################
    ###########################
    
