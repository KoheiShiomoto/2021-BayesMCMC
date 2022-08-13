import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15,10
import argparse
import sys
import pathlib

import datetime
import matplotlib.dates as mdates

from common.tools import mkdir

def get_args():
    psr = argparse.ArgumentParser()
    psr.add_argument("-s", "--startdate", type=str, default="2013-11-04")  # 開始日の選択
    psr.add_argument("-e", "--enddate", type=str, default="2013-11-17")  # 終了日の選択
    psr.add_argument("-od", "--output", type=str, default="output")  # 結果出力先ディレクトリ
    psr.add_argument("-pI", "--prefixOfInfoFileName", type=str, default="info_internet_Original_1104_1117_cell")  # エリア毎の入力ファイル名
    psr.add_argument("--ymaxTraffic", type=float, default=4000.0)  # トラフィックのグラフの最大値
    psr.add_argument("--ymaxPopulation", type=int, default=10000)  # トラフィックのグラフの最大値
    psr.add_argument("-pR", "--prefixOfResultFileName", type=str, default="resultSARIMA_internet_SingleOriginal_1104_1117_cell")  # エリア毎の結果ファイル名
    psr.add_argument("-xi", "--prefixXiFileName", type=str, default="xiData_internet_1104_1110.csv")  # エリア毎の結果ファイル名
    
    psr.add_argument("-c","--cellIdList", nargs="*",
                     default=["04259",
                              "04456",
                              # "04703",
                              "05060",
                              "05200",
                              "05085"], help="list of cell IDs")  
    return psr.parse_args()


def plotMultiResultGraphs(prefixXiFilename,
                          prefixInputDataFilename,
                          prefixResultFilename,
                          keyInputDataFilename,
                          keyResultFilename,
                          cellIdList,
                          title,
                          ymax,
                          xlabel,
                          ylabel,
                          t0,
                          t1,
                          odir="output",
                          picdir="pic"
                          ):
    nrows = -(-len(cellIdList) // 2)  # 切り上げ演算 -(-4 // 3)
    i = 0
    fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(12, 9),sharex=True, sharey=True) 
    key1 = keyInputDataFilename
    key2 = keyResultFilename
    for cell in cellIdList :
        # XiData
        prefix = prefixXiFilename
        fileName = odir+ "/" +prefix+ ".csv"
        df0 = pd.read_csv(fileName, header=0)
        # inputTrafficData
        prefix = prefixInputDataFilename
        fileName = odir+ "/" +prefix+str(cell)+ ".csv"
        df1 = pd.read_csv(fileName, header=0)
        df1 = df1.drop("time", axis=1)
        # resultData1
        prefix = prefixResultFilename
        fileName = odir+ "/" +prefix+str(cell)+ ".csv"
        df2 = pd.read_csv(fileName, header=0)
        #
        #
        data = pd.concat([df0, df1, df2], axis=1) # axis=1は横方向の連結　axis=0は縦方向
        #
        #
        data["time"] = pd.to_datetime(data["time"], format="%Y-%m-%d %H:%M:%S") # 2005-05-04 15:30:00
        data = data[data["time"] > t0]
        data = data[data["time"] < t1]
        data.index = data["time"]
        print(data)
        #
        ax[i%nrows, i//nrows].plot(data.index,data[key1],label="Original")
        ax[i%nrows, i//nrows].plot(data.index,data[key2],label="Predicted")
        #
        ax[i%nrows, i//nrows].set_title("cell"+str(cell))
        ax[i%nrows, i//nrows].set_ylim(0,ymax)
        ax[i%nrows, i//nrows].xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))
        ax[i%nrows, i//nrows].axes.set_xlabel(xlabel)
        ax[i%nrows, i//nrows].axes.set_ylabel(ylabel)

        i = i+1
    # plt.tight_layout()
    plt.legend()
    ghFileName = picdir+ "/" +prefixResultFilename+title.replace(' ','')+ ".pdf"
    plt.savefig(ghFileName)
    plt.show()

if __name__ == '__main__':
    args = get_args()
    output = args.output
    mkdir(output)
    prefixOfInfoFileName = args.prefixOfInfoFileName
    print(prefixOfInfoFileName)
    prefixOfResultFileName = args.prefixOfResultFileName
    print(prefixOfResultFileName)
    prefixXiFileName = args.prefixXiFileName
    print(prefixXiFileName)

    cellIdList = list(args.cellIdList)
    print(cellIdList)

    ymaxTraffic = args.ymaxTraffic
    ymaxPopulation = args.ymaxPopulation
    print(ymaxTraffic)
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

    # plot result data
    prefix0=prefixXiFileName
    prefix1=prefixOfInfoFileName
    prefix2=prefixOfResultFileName
    key1="traffic"
    # key2="predicted-traffic"
    key2="predicted_mean"
    plotMultiResultGraphs(odir=output,
                          title="Traffic rate",
                          prefixXiFilename = prefix0,
                          prefixInputDataFilename = prefix1,
                          prefixResultFilename = prefix2,
                          keyInputDataFilename=key1,
                          keyResultFilename=key2,
                          cellIdList=cellIdList,
                          ymax = ymaxTraffic,
                          xlabel="Time",
                          ylabel="Traffic rate [Mbps]",
                          t0=t0,
                          t1=t1)


path = pathlib.Path(output)
print("output directory ---------------------------------------------------------")
print(path.resolve())
print("--------------------------------------------------------------------------")

