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
    psr.add_argument("-s", "--startdate", type=str, default="2013-11-01")  # 開始日の選択
    psr.add_argument("-e", "--enddate", type=str, default="2013-12-31")  # 終了日の選択
    psr.add_argument("-od", "--output", type=str, default="outputToy")  # 結果出力先ディレクトリ
    psr.add_argument("-pd", "--picdir", type=str, default="picToy")  # 結果出力先ディレクトリ
    psr.add_argument("-Xi", "--prefixOfXiFileName", type=str, default="xiData_cell")  # 入力のXiファイル名のPrefix [Flat, Step, ,,,]
    psr.add_argument("-pT", "--prefixOfTrafficFileName", type=str, default="trafficData_internet_1104_1110_cell")  # 入力のエリア毎のトラフィックファイル名 dummy
    psr.add_argument("-pP", "--prefixOfPopFileName", type=str, default="popData_cell")  # 入力の人口ファイル名のPrefix [Flat, Step, ,,,]
    psr.add_argument("-pI", "--prefixOfInfoFileName", type=str, default="info_cell")  # エリア毎の入力ファイル名のPrefix [PopFlatXiFlat, PopFlatXiStep, PopStepXiFlat, PopStepXiStep, ,,,]
    psr.add_argument("-eN", "--experimentName", type=str, default="_sn06")  # 実験名 [_sn12, _sn10, _sn08, _sn06, _sn04, _sn03, _sn02, _sn01, ,,,]
    psr.add_argument("--ymaxTraffic", type=float, default=2000.0)  # トラフィックのグラフの最大値
    psr.add_argument("--ymaxPopulation", type=int, default=15000)  # 人口のグラフの最大値
    psr.add_argument("--ymaxXi", type=int, default=1.0)  # Activity Factorのグラフの最大値
    psr.add_argument("-pR", "--prefixOfResultFileName", type=str, default="result_cell")  # エリア毎の結果ファイル名のPrefix [PopFlatXiFlat, PopFlatXiStep, PopStepXiFlat, PopStepXiStep, ,,,]
    
    psr.add_argument("-c","--cellIdList", nargs="*",
                     default=["PopFlatXiFlat",
                              "PopFlatXiStep",
                              "PopStepXiFlat",
                              "PopStepXiStep"], help="list of cell IDs")  
    psr.add_argument("-pt","--patternIdList", nargs="*",
                     default=["Flat",
                              "Step"], help="list of pattern IDs")  
    return psr.parse_args()


def plotMultiToyInputDataGraphs(y1max,
                                y2max=1.0,
                                odir="output",
                                picdir="pic",
                                pjName="PopXi",
                                y1prefix="popData_cell",
                                y2prefix="xiData_cell",
                                patternIdList=["Flat", "Step"],
                                key="time",
                                xlabel="Time",
                                y1label="Population",
                                y2label="Activity factor"):
    # nrows = -(-len(patternIdList) // 2)  # 切り上げ演算 -(-4 // 3)
    nrows = 2
    i = 0
    fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(12, 9),sharex=True, sharey=True) 
    for y1pattern in patternIdList :
        for y2pattern in patternIdList :
            subTitle = y1pattern+y2pattern
            y1fileName = odir+ "/" +y1prefix+str(y1pattern)+ ".csv"
            y1data = pd.read_csv(y1fileName, header=0)
            y1data[key] = pd.to_datetime(y1data[key], format="%Y-%m-%d %H:%M:%S") # 2005-05-04 15:30:00
            y1data.index = y1data[key]
            y1key_local = "cell04456"
            ax[i%nrows, i//nrows].xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))
            ax[i%nrows, i//nrows].plot(y1data.index,y1data[y1key_local], label="Population", color="blue", linestyle="-", marker=None) # marker=None, ".", ",", "o", "^", "v", "<", ">"
            ax[i%nrows, i//nrows].set_title(subTitle)
            ax[i%nrows, i//nrows].set_ylim(0,y1max)
            ax[i%nrows, i//nrows].axes.set_xlabel(xlabel)
            ax[i%nrows, i//nrows].axes.set_ylabel(y1label)
            #
            y2fileName = odir+ "/" +y2prefix+str(y2pattern)+ ".csv"
            y2data = pd.read_csv(y2fileName, header=0)
            y2data[key] = pd.to_datetime(y2data[key], format="%Y-%m-%d %H:%M:%S") # 2005-05-04 15:30:00
            y2data.index = y2data[key]
            y2key_local = "Normalized Sum (total)"
            ax2 = ax[i%nrows, i//nrows].twinx()
            ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))
            ax2.plot(y2data.index,y2data[y2key_local], label="Activity factor", color="red", linestyle=":", marker=None)  # marker=None, ".", ",", "o", "^", "v", "<", ">"
            ax2.set_ylim(0,y2max)
            ax2.axes.set_xlabel(xlabel)
            ax2.axes.set_ylabel(y2label)
            #
            h1, l1 = ax[i%nrows, i//nrows].get_legend_handles_labels()
            h2, l2 = ax2.get_legend_handles_labels()
            ax[i%nrows, i//nrows].legend(h1+h2, l1+l2, loc='upper right')
            i = i+1
    # plt.tight_layout()
    # plt.legend()
    ghFileName = picdir+ "/" +pjName +".pdf"
    plt.savefig(ghFileName)
    plt.show()

# {SO_inputData : ["infoOriginal_internet_1104_1110_cell","traffic","Time","Traffic [Mbps]"]},
# {SO_resultData1 : ["result_SingleOriginal_internet_1104_1110_cell","predicted-traffic","Time","Predicted traffic rate [Mbps]"]},
# {SO_resultData2 : ["result_SingleOriginal_internet_1104_1110_cell","xi","Time","Predicted activity factor"]},
# {SO_resultData3 : ["result_SingleOriginal_internet_1104_1110_cell","population","Time","Population"]},
# {SO_resultData4 : ["result_SingleOriginal_internet_1104_1110_cell","Nv1","Time","Number of predicted active users"]},
def plotMultiToyResultGraphs(prefixOfXiFilename,
                             prefixInputDataFilename,
                             prefixResultFilename,
                             keyInputDataFilename,
                             keyResultFilename,
                             title,
                             ymax,
                             xlabel,
                             ylabel,
                             experimentName="_sn06",
                             patternIdList=["Flat", "Step"],
                             cellIdList=["PopFlatXiFlat",
                                         "PopFlatXiStep",
                                         "PopStepXiFlat",
                                         "PopStepXiStep"],
                             key="time",
                             odir="outputToy",
                             picdir="picToy"):
    # for y1pattern in patternIdList :
    #     for y2pattern in patternIdList :
    #
    # nrows = -(-len(cellIdList) // 2)  # 切り上げ演算 -(-4 // 3)
    nrows = 2
    i = 0
    fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(12, 9),sharex=True, sharey=True) 
    key1 = keyInputDataFilename
    key2 = keyResultFilename
    for cell in cellIdList :
        # # XiData
        # prefix = prefixOfXiFilename
        # fileName = odir+ "/" +prefix+ ".csv"
        # df0 = pd.read_csv(fileName, header=0)
        # inputTrafficData
        prefix = prefixInputDataFilename
        fileName = odir+ "/" +prefix+str(cell)+".csv"
        df1 = pd.read_csv(fileName, header=0)
        # df1 = df1.drop(key, axis=1)
        # resultData1
        prefix = prefixResultFilename
        fileName = odir+ "/" +prefix+str(cell)+experimentName+".csv"
        df2 = pd.read_csv(fileName, header=0)
        #
        #
        # data = pd.concat([df0, df1, df2], axis=1) # axis=1は横方向の連結　axis=0は縦方向
        data = pd.concat([df1, df2], axis=1) # axis=1は横方向の連結　axis=0は縦方向
        #
        #
        data[key] = pd.to_datetime(data[key], format="%Y-%m-%d %H:%M:%S") # 2005-05-04 15:30:00
        data.index = data[key]
        print(data)
        #
        ax[i%nrows, i//nrows].plot(data.index,data[key1],label="Original", linestyle="-", color="blue", marker=None) # marker=".", ",", "o", "^", "v", "<", ">"
        ax[i%nrows, i//nrows].plot(data.index,data[key2],label="Predicted", linestyle=":", color="red", marker=None) # marker=".", ",", "o", "^", "v", "<", ">"
        #
        ax[i%nrows, i//nrows].set_title(str(cell))
        ax[i%nrows, i//nrows].set_ylim(0,ymax)
        ax[i%nrows, i//nrows].xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))
        ax[i%nrows, i//nrows].axes.set_xlabel(xlabel)
        ax[i%nrows, i//nrows].axes.set_ylabel(ylabel)
        #
        ax[i%nrows, i//nrows].legend()
        i = i+1
    # plt.tight_layout()
    # plt.legend()
    ghFileName = picdir+ "/" +prefixResultFilename+experimentName+title.replace(' ','')+ "-OrgPrd.pdf"
    plt.savefig(ghFileName)
    plt.show()

if __name__ == '__main__':
    args = get_args()
    output = args.output
    mkdir(output)
    picdir = args.picdir
    mkdir(picdir)
    prefixOfXiFileName = args.prefixOfXiFileName
    print(prefixOfXiFileName)
    prefixOfTrafficFileName = args.prefixOfTrafficFileName
    print(prefixOfTrafficFileName)
    prefixOfPopFileName = args.prefixOfPopFileName
    print(prefixOfPopFileName)
    prefixOfInfoFileName = args.prefixOfInfoFileName
    print(prefixOfInfoFileName)
    prefixOfResultFileName = args.prefixOfResultFileName
    print(prefixOfResultFileName)

    cellIdList = list(args.cellIdList)
    print(cellIdList)
    patternIdList = list(args.patternIdList)
    print(patternIdList)

    experimentName = args.experimentName
    print(experimentName)

    ymaxTraffic = args.ymaxTraffic
    ymaxPopulation = args.ymaxPopulation
    ymaxXi = args.ymaxXi
    
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


    # plot population data
    y1prefix = prefixOfPopFileName
    y2prefix = prefixOfXiFileName
    plotMultiToyInputDataGraphs(y1max = ymaxPopulation,
                                y2max = ymaxXi,
                                odir=output,
                                picdir=picdir,
                                y1prefix=y1prefix,
                                y2prefix=y2prefix,
                                patternIdList=patternIdList,
                                key="time",
                                xlabel="Time",
                                y1label="Population",
                                y2label="Activity Factor")

    prefix0=prefixOfXiFileName
    prefix1=prefixOfInfoFileName
    prefix2=prefixOfResultFileName
    key1="traffic"
    key2="predicted-traffic"
    plotMultiToyResultGraphs(odir=output,
                             picdir=picdir,
                             title="Traffic Rate",
                             prefixOfXiFilename = prefix0,
                             prefixInputDataFilename = prefix1,
                             prefixResultFilename = prefix2,
                             keyInputDataFilename=key1,
                             keyResultFilename=key2,
                             cellIdList=cellIdList,
                             experimentName = experimentName,
                             ymax = ymaxTraffic,
                             key="time",
                             xlabel="Time",
                             ylabel="Traffic Rate [Mbps]")

    # # Activity factor
    # prefix0=prefixOfXiFileName
    # prefix1=prefixOfInfoFileName
    # prefix2=prefixOfResultFileName
    # key1="Normalized Sum (total)"
    # if args.didMultiPrediction == False:
    #     # Single Class
    #     key2="predicted-xi"
    #     plotMultiResultGraphs(odir=output,
    #                           picdir=picdir,
    #                           title="Activity factor",
    #                           prefixOfXiFilename = prefix0,
    #                           prefixInputDataFilename = prefix1,
    #                           prefixResultFilename = prefix2,
    #                           keyInputDataFilename=key1,
    #                           keyResultFilename=key2,
    #                           cellIdList=cellIdList,
    #                           ymax = 1.0,
    #                           xlabel="Time",
    #                           key="time",
    #                           ylabel="Activity factor",
    #                           t0=t0,
    #                           t1=t1)
        
    # else:
    #     # Multi Class
    #     key2="predicted-xi1"
    #     plotMultiResultGraphs(odir=output,
    #                           picdir=picdir,
    #                           title="Activity factor of class 1",
    #                           prefixOfXiFilename = prefix0,
    #                           prefixInputDataFilename = prefix1,
    #                           prefixResultFilename = prefix2,
    #                           keyInputDataFilename=key1,
    #                           keyResultFilename=key2,
    #                           cellIdList=cellIdList,
    #                           ymax = 1.0,
    #                           key="time",
    #                           xlabel="Time",
    #                           ylabel="Activity factor",
    #                           t0=t0,
    #                           t1=t1)
    #     key2="predicted-xi2"
    #     plotMultiResultGraphs(odir=output,
    #                           picdir=picdir,
    #                           title="Activity factor of class 2",
    #                           prefixOfXiFilename = prefix0,
    #                           prefixInputDataFilename = prefix1,
    #                           prefixResultFilename = prefix2,
    #                           keyInputDataFilename=key1,
    #                           keyResultFilename=key2,
    #                           cellIdList=cellIdList,
    #                           ymax = 1.0,
    #                           key="time",
    #                           xlabel="Time",
    #                           ylabel="Activity factor",
    #                           t0=t0,
    #                           t1=t1)
        


path = pathlib.Path(output)
print("output directory ---------------------------------------------------------")
print(path.resolve())
print("--------------------------------------------------------------------------")

