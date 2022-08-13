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
    psr.add_argument("-od", "--output", type=str, default="output")  # 結果出力先ディレクトリ
    psr.add_argument("-pd", "--picdir", type=str, default="pic")  # 結果出力先ディレクトリ
    psr.add_argument("-Xi", "--prefixXiFileName", type=str, default="xiData_internet_1104_1110")  # 入力のXiファイル名
    psr.add_argument("-rXi1", "--ratioOfXi1", type=float, default=0.8)
    psr.add_argument("-rXi2", "--ratioOfXi2", type=float, default=0.2)
    psr.add_argument("-pT", "--prefixOfTrafficFileName", type=str, default="trafficData_internet_1104_1110_cell")  # 入力のエリア毎のトラフィックファイル名
    psr.add_argument("-pP", "--prefixOfPopFileName", type=str, default="popData_internet_1104_1110_cell")  # 入力のエリア毎の人口ファイル名
    psr.add_argument("-pI", "--prefixOfInfoFileName", type=str, default="info_internet_Original_1104_1110_cell")  # エリア毎の入力ファイル名
    psr.add_argument("-m", "--didMultiPrediction", action='store_true')  # 複数クラスでの推定を行ったか？
    psr.add_argument("--ymaxTraffic", type=float, default=4000.0)  # トラフィックのグラフの最大値
    psr.add_argument("--ymaxPopulation", type=int, default=10000)  # トラフィックのグラフの最大値
    psr.add_argument("-pR", "--prefixOfResultFileName", type=str, default="result_internet_SingleOriginal_1104_1110_cell")  # エリア毎の結果ファイル名
    #
    psr.add_argument('-sA', '--switchSARIMA', action='store_true')
    psr.add_argument('-sMltSngl', '--switchMultiSingle', action='store_true')
    psr.add_argument("-pR1", "--prefixOfResult1FileName", type=str, default="result_internet_SingleOriginal_1104_1110_cell")  # エリア毎の結果ファイル名 Proposed
    psr.add_argument("-pR2", "--prefixOfResult2FileName", type=str, default="resultSARIMA_OneDayCycle_internet_SingleOriginal_1104_1117_cell04259")  # エリア毎の結果ファイル名 SARIMA (day)
    psr.add_argument("-pR3", "--prefixOfResult3FileName", type=str, default="resultSARIMA_internet_SingleOriginal_1104_1117_cell")  # エリア毎の結果ファイル名 SARIMA (week)
    
    psr.add_argument('--pjName', default='test', help='ProjectName')  

    psr.add_argument("-c","--cellIdList", nargs="*",
                     default=["04259",
                              "04456",
                              # "04703",
                              "05060",
                              "05200",
                              "05085"], help="list of cell IDs")  
    return psr.parse_args()


def plotInputXiDataGraphs(odir,
                          prefix,
                          t0,
                          t1,
                          key="time"):
    fileName = odir+ "/" +prefix+ ".csv"
    data = pd.read_csv(fileName, header=0)
    data[key] = pd.to_datetime(data[key], format="%Y-%m-%d %H:%M:%S") # 2005-05-04 15:30:00
    data = data[data[key] > t0]
    data = data[data[key] < t1]
    data.index = data[key]
    key_local = "Normalized Sum (total)"
    fig, ax = plt.subplots(1,1, figsize=(9, 4),sharex=True, sharey=True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))
    ax.plot(data.index,data[key_local])
    ax.set_title("Activity factor")
    # ax.legend()
    # ax.axes.xaxis.set_ticklabels([])
    # ax.axes.yaxis.set_ticklabels([])
    ax.axes.set_xlabel(key)
    ax.axes.set_ylabel("Activity factor")
    # plt.tight_layout()
    # plt.legend()
    # ghFileName = "pic/"+prefix+".pdf"
    ghFileName = picdir+prefix+".pdf"
    plt.savefig(ghFileName)
    plt.show()

def plotMultiInputDataGraphs(prefix,
                             cellIdList,
                             ymax,
                             xlabel,
                             ylabel,
                             t0,
                             t1,
                             key="time",
                             odir="output",
                             picdir="pic"):
    nrows = -(-len(cellIdList) // 2)  # 切り上げ演算 -(-4 // 3)
    i = 0
    fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(12, 9),sharex=True, sharey=True) 
    for cell in cellIdList :
        fileName = odir+ "/" +prefix+str(cell)+ ".csv"
        data = pd.read_csv(fileName, header=0)
        data[key] = pd.to_datetime(data[key], format="%Y-%m-%d %H:%M:%S") # 2005-05-04 15:30:00
        data = data[data[key] > t0]
        data = data[data[key] < t1]
        data.index = data[key]
        key_local = "cell"+str(cell)
        ax[i%nrows, i//nrows].xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))
        ax[i%nrows, i//nrows].plot(data.index,data[key_local])
        ax[i%nrows, i//nrows].set_title(key_local)
        ax[i%nrows, i//nrows].set_ylim(0,ymax)
        # ax[i%nrows, i//nrows].axes.xaxis.set_ticklabels([])
        # ax[i%nrows, i//nrows].axes.yaxis.set_ticklabels([])
        ax[i%nrows, i//nrows].axes.set_xlabel(xlabel)
        ax[i%nrows, i//nrows].axes.set_ylabel(ylabel)
        #
        # ax[i%nrows, i//nrows].legend()
        #
        i = i+1
    # plt.tight_layout()
    # plt.legend()
    ghFileName = picdir+ "/" +prefix +".pdf"
    plt.savefig(ghFileName)
    plt.show()

# {SO_inputData : ["infoOriginal_internet_1104_1110_cell","traffic","Time","Traffic [Mbps]"]},
# {SO_resultData1 : ["result_SingleOriginal_internet_1104_1110_cell","predicted-traffic","Time","Predicted traffic rate [Mbps]"]},
# {SO_resultData2 : ["result_SingleOriginal_internet_1104_1110_cell","xi","Time","Predicted activity factor"]},
# {SO_resultData3 : ["result_SingleOriginal_internet_1104_1110_cell","population","Time","Population"]},
# {SO_resultData4 : ["result_SingleOriginal_internet_1104_1110_cell","Nv1","Time","Number of predicted active users"]},
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
                          scaleXi=1.0,
                          key="time",
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
        df0["Normalized Sum (total)"] *= scaleXi
        # inputTrafficData
        prefix = prefixInputDataFilename
        fileName = odir+ "/" +prefix+str(cell)+ ".csv"
        df1 = pd.read_csv(fileName, header=0)
        df1 = df1.drop(key, axis=1)
        # resultData1
        prefix = prefixResultFilename
        fileName = odir+ "/" +prefix+str(cell)+ ".csv"
        df2 = pd.read_csv(fileName, header=0)
        #
        #
        data = pd.concat([df0, df1, df2], axis=1) # axis=1は横方向の連結　axis=0は縦方向
        #
        #
        data[key] = pd.to_datetime(data[key], format="%Y-%m-%d %H:%M:%S") # 2005-05-04 15:30:00
        data = data[data[key] > t0]
        data = data[data[key] < t1]
        data.index = data[key]
        print(data)
        #
        ax[i%nrows, i//nrows].plot(data.index,data[key1],label="Original", color="blue", linestyle=":", marker=".", markevery=10) # marker=None, ".", ",", "o", "^", "v", "<", ">"
        ax[i%nrows, i//nrows].plot(data.index,data[key2],label="Predicted", color="red", linestyle="-", marker=None) # marker=None, ".", ",", "o", "^", "v", "<", ">"
        #
        ax[i%nrows, i//nrows].set_title("cell"+str(cell))
        ax[i%nrows, i//nrows].set_ylim(0,ymax)
        ax[i%nrows, i//nrows].xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))
        ax[i%nrows, i//nrows].axes.set_xlabel(xlabel)
        ax[i%nrows, i//nrows].axes.set_ylabel(ylabel)
        #
        ax[i%nrows, i//nrows].legend()
        #
        i = i+1
    # plt.tight_layout()
    # plt.legend()
    ghFileName = picdir+ "/" +prefixResultFilename+title.replace(' ','')+ "-OrgPrd.pdf"
    plt.savefig(ghFileName)
    plt.show()
    data.to_csv(picdir+ "/" +prefixResultFilename+title.replace(' ','')+ "-OrgPrd.csv")


def plotMultiResult2Graphs(prefix1,
                           prefix2,
                           prefix3,
                           header1,
                           header2,
                           header3,
                           key1,
                           key2,
                           key3,
                           label1,
                           label2,
                           label3,
                           cellIdList,
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
    nrows = -(-len(cellIdList) // 2)  # 切り上げ演算 -(-4 // 3)
    i = 0
    fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(12, 9),sharex=True, sharey=True) 
    for cell in cellIdList :
        # prefix1 data
        prefix1 = prefix1
        fileName = odir+ "/" +prefix1+str(cell)+ ".csv"
        if (header1 >=0) :
            df_tmp = pd.read_csv(fileName, header=header1)
        else:
            df_tmp = pd.read_csv(fileName)
        df1 = df_tmp.rename(columns={key1: label1})
        print(df1)
        # prefix2 Data
        prefix2 = prefix2
        fileName = odir+ "/" +prefix2+str(cell)+ ".csv"
        if (header2 >=0) :
            df_tmp = pd.read_csv(fileName, header=header2)
        else:
            df_tmp = pd.read_csv(fileName)
        df2 = df_tmp.rename(columns={key2: label2})
        print(df2)
        # prefix3 Data
        prefix3 = prefix3
        fileName = odir+ "/" +prefix3+str(cell)+ ".csv"
        if (header3 >=0) :
            df_tmp = pd.read_csv(fileName, header=header3)
        else:
            df_tmp = pd.read_csv(fileName)
        df3 = df_tmp.rename(columns={key3: label3})
        print(df3)
        #
        data = pd.concat([df1, df2, df3], axis=1) # axis=1は横方向の連結　axis=0は縦方向
        #

        #
        data[key] = pd.to_datetime(data[key], format="%Y-%m-%d %H:%M:%S") # 2005-05-04 15:30:00
        data = data[data[key] > t0]
        data = data[data[key] < t1]
        data.index = data[key]
        print(data)
        #
        ax[i%nrows, i//nrows].plot(data.index,data[label1],label=label1, color="blue", linestyle="-", marker=None) # marker=None, ".", ",", "o", "^", "v", "<", ">"
        ax[i%nrows, i//nrows].plot(data.index,data[label2],label=label2, color="red", linestyle=":", marker=None) # marker=None, ".", ",", "o", "^", "v", "<", ">"
        ax[i%nrows, i//nrows].plot(data.index,data[label3],label=label3, color="red", linestyle=":", marker=".", markevery=10) # marker=None, ".", ",", "o", "^", "v", "<", ">"
        #
        ax[i%nrows, i//nrows].set_title("cell"+str(cell))
        ax[i%nrows, i//nrows].set_ylim(0,ymax)
        ax[i%nrows, i//nrows].xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))
        ax[i%nrows, i//nrows].axes.set_xlabel(xlabel)
        ax[i%nrows, i//nrows].axes.set_ylabel(ylabel)
        #
        ax[i%nrows, i//nrows].legend()
        #
        i = i+1
    # plt.tight_layout()
    # plt.legend()
    ghFileName = picdir+ "/" +pjName+title.replace(' ','')+ "-OrgPrd.pdf"
    plt.savefig(ghFileName)
    plt.show()
    data.to_csv(picdir+ "/" +pjName+title.replace(' ','')+ "-OrgPrd.csv")
    


def plotMultiResult3Graphs(prefix1,
                           prefix2,
                           prefix3,
                           prefix4,
                           header1,
                           header2,
                           header3,
                           header4,
                           key1,
                           key2,
                           key3,
                           key4,
                           label1,
                           label2,
                           label3,
                           label4,
                           cellIdList,
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
    nrows = -(-len(cellIdList) // 2)  # 切り上げ演算 -(-4 // 3)
    i = 0
    fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(12, 9),sharex=True, sharey=True) 
    for cell in cellIdList :
        # prefix1 data
        fileName = odir+ "/" +prefix1+str(cell)+ ".csv"
        if (header1 >= 0) :
            df_tmp = pd.read_csv(fileName, header=header1)
        else:
            df_tmp = pd.read_csv(fileName)
        df1 = df_tmp.rename(columns={key1: label1})
        print(fileName)
        print(df1)
        # prefix2 data
        fileName = odir+ "/" +prefix2+str(cell)+ ".csv"
        if (header2 >= 0) :
            df_tmp = pd.read_csv(fileName, header=header2)
        else:
            df_tmp = pd.read_csv(fileName)
        df2 = df_tmp.rename(columns={key2: label2})
        print(fileName)
        print(df2)
        # prefix3 data
        fileName = odir+ "/" +prefix3+str(cell)+ ".csv"
        if (header3 >= 0) :
            df_tmp = pd.read_csv(fileName, header=header3)
        else:
            df_tmp = pd.read_csv(fileName)
        df3 = df_tmp.rename(columns={key3: label3})
        print(fileName)
        print(df3)
        # prefix4 data
        fileName = odir+ "/" +prefix4+str(cell)+ ".csv"
        if (header4 >= 0) :
            df_tmp = pd.read_csv(fileName, header=header4)
        else:
            df_tmp = pd.read_csv(fileName)
        df4 = df_tmp.rename(columns={key4: label4})
        print(fileName)
        print(df4)
        #
        #
        data = pd.concat([df1, df2, df3, df4], axis=1) # axis=1は横方向の連結　axis=0は縦方向
        # data = df0.join([df1, df_result1, df_result2, df_result3]) # axis=1は横方向の連結　axis=0は縦方向
        # print(data)
        #

        # data.columns = ["Normalized Sum (total)", "Original", labelResult1, labelResult2, labelResult3]

        #
        #
        data[key] = pd.to_datetime(data[key], format="%Y-%m-%d %H:%M:%S") # 2005-05-04 15:30:00
        data = data[data[key] > t0]
        data = data[data[key] < t1]
        data.index = data[key]
        # print(data)
        #
        data_tmp = data[label1].dropna()
        ax[i%nrows, i//nrows].plot(data_tmp.index,data_tmp,label=label1, color="black", linestyle=":", marker=".", markevery=24) # marker=None, ".", ",", "o", "^", "v", "<", ">"
        data_tmp = data[label2].dropna()
        ax[i%nrows, i//nrows].plot(data_tmp.index,data_tmp,label=label2, color="red", linestyle="-", marker=None) # marker=None, ".", ",", "o", "^", "v", "<", ">"
        data_tmp = data[label3].dropna()
        ax[i%nrows, i//nrows].plot(data_tmp.index,data_tmp,label=label3, color="green", linestyle=":", marker="^", markevery=12) # marker=None, ".", ",", "o", "^", "v", "<", ">"
        data_tmp = data[label4].dropna()
        ax[i%nrows, i//nrows].plot(data_tmp.index,data_tmp,label=label4, color="green", linestyle="-", marker=None) # marker=None, ".", ",", "o", "^", "v", "<", ">"
        # #
        # ax[i%nrows, i//nrows].plot(data.index,data[label2],label=label1, color="black", linestyle=":", marker=".", markevery=24) # marker=None, ".", ",", "o", "^", "v", "<", ">"
        # ax[i%nrows, i//nrows].plot(data.index,data[label2],label=label2, color="red", linestyle="-", marker=None) # marker=None, ".", ",", "o", "^", "v", "<", ">"
        # ax[i%nrows, i//nrows].plot(data.index,data[label3],label=label3, color="green", linestyle=":", marker="^", markevery=24) # marker=None, ".", ",", "o", "^", "v", "<", ">"
        # ax[i%nrows, i//nrows].plot(data.index,data[label4],label=label4, color="green", linestyle="-", marker=None) # marker=None, ".", ",", "o", "^", "v", "<", ">"
        #
        ax[i%nrows, i//nrows].set_title("cell"+str(cell))
        ax[i%nrows, i//nrows].set_ylim(0,ymax)
        ax[i%nrows, i//nrows].xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))
        ax[i%nrows, i//nrows].axes.set_xlabel(xlabel)
        ax[i%nrows, i//nrows].axes.set_ylabel(ylabel)
        #
        ax[i%nrows, i//nrows].legend()
        #
        i = i+1
    # plt.tight_layout()
    # plt.legend()
    ghFileName = picdir+ "/" +pjName+title.replace(' ','')+ "-OrgPrd.pdf"
    plt.savefig(ghFileName)
    plt.show()
    print(data)
    data.to_csv(picdir+ "/" +pjName+title.replace(' ','')+ "-OrgPrd.csv")
    
    
if __name__ == '__main__':
    args = get_args()
    output = args.output
    mkdir(output)
    picdir = args.picdir
    mkdir(picdir)
    prefixXiFileName = args.prefixXiFileName
    print(prefixXiFileName)
    rXi1 = args.ratioOfXi1
    rXi2 = args.ratioOfXi2
    prefixOfTrafficFileName = args.prefixOfTrafficFileName
    print(prefixOfTrafficFileName)
    prefixOfPopFileName = args.prefixOfPopFileName
    print(prefixOfPopFileName)
    prefixOfInfoFileName = args.prefixOfInfoFileName
    print(prefixOfInfoFileName)
    prefixOfResultFileName = args.prefixOfResultFileName
    print(prefixOfResultFileName)
    #
    prefixOfResult1FileName = args.prefixOfResult1FileName
    print(prefixOfResult1FileName)
    prefixOfResult2FileName = args.prefixOfResult2FileName
    print(prefixOfResult2FileName)
    prefixOfResult3FileName = args.prefixOfResult3FileName
    print(prefixOfResult3FileName)

    cellIdList = list(args.cellIdList)
    print(cellIdList)

    pjName = args.pjName

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



    # plot activity factor
    plotInputXiDataGraphs(odir=output,
                          prefix=prefixXiFileName,
                          t0=t0,
                          t1=t1)
    

    # plot traffic data 
    prefix = prefixOfTrafficFileName
    plotMultiInputDataGraphs(odir=output,
                             picdir=picdir,
                             prefix=prefix,
                             cellIdList=cellIdList,
                             ymax = ymaxTraffic,
                             key="time",
                             xlabel="Time",
                             ylabel="Traffic Rate [Mbps]",
                             t0=t0,
                             t1=t1)

    # # # plot result of predicted traffic data
    # # prefix=prefixOfResultFileName
    # plotMultiInputDataGraphs(odir=output,
    #                          picdir=picdir,
    #                          prefix=prefix,
    #                          cellIdList=cellIdList,
    #                          ymax = ymaxTraffic,
    #                          key="time",
    #                          xlabel="Time",
    #                          ylabel="Predicted Traffic Rate [Mbps]",
    #                          t0=t0,
    #                          t1=t1)


    # plot population data
    prefix = prefixOfPopFileName
    plotMultiInputDataGraphs(odir=output,
                             picdir=picdir,
                             prefix=prefix,
                             cellIdList=cellIdList,
                             ymax = ymaxPopulation,
                             key="time",
                             xlabel="Time",
                             ylabel="Population",
                             t0=t0,
                             t1=t1)



    # plot result data
    # {SO_inputData : ["infoOriginal_internet_1104_1110_cell","traffic","Time","Traffic [Mbps]"]},
    # {SO_resultData1 : ["result_SingleOriginal_internet_1104_1110_cell","predicted-traffic","Time","Predicted traffic rate [Mbps]"]},
    # {SO_resultData2 : ["result_SingleOriginal_internet_1104_1110_cell","xi","Time","Predicted activity factor"]},
    # {SO_resultData3 : ["result_SingleOriginal_internet_1104_1110_cell","population","Time","Population"]},
    # {SO_resultData4 : ["result_SingleOriginal_internet_1104_1110_cell","Nv1","Time","Number of predicted active users"]},
    prefix0=prefixXiFileName
    prefix1=prefixOfInfoFileName
    prefix2=prefixOfResultFileName
    key1="traffic"
    key2="predicted-traffic"
    plotMultiResultGraphs(odir=output,
                          picdir=picdir,
                          title="Traffic Rate",
                          prefixXiFilename = prefix0,
                          prefixInputDataFilename = prefix1,
                          prefixResultFilename = prefix2,
                          keyInputDataFilename=key1,
                          keyResultFilename=key2,
                          cellIdList=cellIdList,
                          ymax = ymaxTraffic,
                          key="time",
                          xlabel="Time",
                          ylabel="Traffic Rate [Mbps]",
                          t0=t0,
                          t1=t1)

    ###########################
    ###########################
    ###########################
    if args.switchSARIMA :
        plotMultiResult3Graphs(odir=output,
                               picdir=picdir,
                               title="Traffic Rate",
                               prefix1=prefixOfInfoFileName,
                               prefix2=prefixOfResult1FileName,
                               prefix3=prefixOfResult2FileName,
                               prefix4=prefixOfResult3FileName,
                               header1=0,
                               header2=0,
                               header3=0,
                               header4=0,
                               key1 ="traffic", # time,pop,traffic,CPU,MEM
                               key2 = "predicted-traffic", # predicted-traffic,predicted-xi,predicted-population,predicted-Nv1
                               key3 = "predicted_mean", # predicted_mean
                               key4 = "predicted_mean", # predicted_mean
                               label1 = "Original",
                               label2 = "Proposed",
                               label3 = "SARIMA (day)",
                               label4 = "SARIMA (week)",
                               pjName = "ProposedVsSarima"+pjName,
                               cellIdList = cellIdList,
                               ymax = ymaxTraffic,
                               key = "time",
                               xlabel = "Time",
                               ylabel = "Traffic Rate [Mbps]",
                               t0 = t0,
                               t1 = t1)
    ###########################
    ###########################
    ###########################




    ###########################
    ###########################
    ###########################
    if args.switchMultiSingle :
        ########## Traffic
        prefix1=prefixOfInfoFileName
        prefix2=prefixOfResult1FileName
        prefix3=prefixOfResult2FileName
        plotMultiResult2Graphs(odir=output,
                               picdir=picdir,
                               title="Traffic Rate",
                               prefix1= prefix1,
                               prefix2 = prefix2,
                               prefix3 = prefix3,
                               header1 = 0,
                               header2 = -1,
                               header3 = -1,
                               key1 = "traffic",
                               key2 = "predicted-traffic",
                               key3 = "predicted-traffic",
                               label1 = "Original",
                               label2 = "Predicted (class 1)",
                               label3 = "Predicted (class 2)",
                               pjName = "MultiSingle12",
                               cellIdList = cellIdList,
                               ymax = ymaxTraffic,
                               key = "time",
                               xlabel = "Time",
                               ylabel = "Traffic Rate [Mbps]",
                               t0 = t0,
                               t1 = t1)
        ########## Activity Factor
        prefix1=prefixXiFileName+"_cell"
        prefix2=prefixOfResult1FileName
        prefix3=prefixOfResult2FileName
        plotMultiResult2Graphs(odir=output,
                               picdir=picdir,
                               title="Activity Factor",
                               prefix1= prefix1,
                               prefix2 = prefix2,
                               prefix3 = prefix3,
                               header1 = 0,
                               header2 = -1,
                               header3 = -1,
                               key1 = "Normalized Sum (total)",
                               key2 = "predicted-xi",
                               key3 = "predicted-xi",
                               label1 = "Original",
                               label2 = "Predicted (class 1)",
                               label3 = "Predicted (class 2)",
                               pjName = "MultiSingle12",
                               cellIdList = cellIdList,
                               ymax = 1.0,
                               key = "time",
                               xlabel = "Time",
                               ylabel = "Activity Factor",
                               t0 = t0,
                               t1 = t1)
    ###########################
    ###########################
    ###########################
    


    # Activity factor
    prefix0=prefixXiFileName
    prefix1=prefixOfInfoFileName
    prefix2=prefixOfResultFileName
    key1="Normalized Sum (total)"
    if args.didMultiPrediction == False:
        # Single Class
        key2="predicted-xi"
        plotMultiResultGraphs(odir=output,
                              picdir=picdir,
                              title="Activity factor",
                              prefixXiFilename = prefix0,
                              prefixInputDataFilename = prefix1,
                              prefixResultFilename = prefix2,
                              keyInputDataFilename=key1,
                              keyResultFilename=key2,
                              cellIdList=cellIdList,
                              ymax = 1.0,
                              xlabel="Time",
                              key="time",
                              ylabel="Activity factor",
                              t0=t0,
                              t1=t1)
        
    else:
        # Multi Class
        key2="predicted-xi1"
        plotMultiResultGraphs(odir=output,
                              scaleXi = rXi1,
                              picdir=picdir,
                              title="Activity factor of class 1",
                              prefixXiFilename = prefix0,
                              prefixInputDataFilename = prefix1,
                              prefixResultFilename = prefix2,
                              keyInputDataFilename=key1,
                              keyResultFilename=key2,
                              cellIdList=cellIdList,
                              ymax = 1.0,
                              key="time",
                              xlabel="Time",
                              ylabel="Activity factor",
                              t0=t0,
                              t1=t1)
        key2="predicted-xi2"
        plotMultiResultGraphs(odir=output,
                              scaleXi = rXi2,
                              picdir=picdir,
                              title="Activity factor of class 2",
                              prefixXiFilename = prefix0,
                              prefixInputDataFilename = prefix1,
                              prefixResultFilename = prefix2,
                              keyInputDataFilename=key1,
                              keyResultFilename=key2,
                              cellIdList=cellIdList,
                              ymax = 1.0,
                              key="time",
                              xlabel="Time",
                              ylabel="Activity factor",
                              t0=t0,
                              t1=t1)
        


path = pathlib.Path(output)
print("output directory ---------------------------------------------------------")
print(path.resolve())
print("--------------------------------------------------------------------------")

