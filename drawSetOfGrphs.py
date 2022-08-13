import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15,10
import argparse
import sys
import pathlib

from common.tools import mkdir

def get_args():
    psr = argparse.ArgumentParser()
    psr.add_argument("-od", "--output", type=str, default="output")  # 結果出力先ディレクトリ
    psr.add_argument("-i", "--inputFile", type=str, default="xiData_internet_1104_1110.csv")  
    psr.add_argument("-k", "--key", type=str)  
    psr.add_argument("-xl", "--xlabel", type=str)  # x-label
    psr.add_argument("-yl", "--ylabel", type=str)  # y-label
    
    # 'xiData_internet_1104_1110.csv' xiだけはセルによらずシステム共通　
    psr.add_argument('-i','--listOfPrefixOfDataFileName', nargs="*",
                     default=["trafficData_internet_1104_1110_cell",
                              "popData_internet_1104_1110_cell",
                              "infoOriginal_internet_1104_1110_cell",
                              "result_SingleOriginal_internet_1104_1110_cell",
                              "infoSingle_internet_1104_1110_cell",
                              "result_SingleSingle_internet_1104_1110_cell",
                              "infoMulti_internet_1104_1110_cell",
                              "result_MultiSingle1_internet_1104_1110_cell",
                              "result_MultiSingle2_internet_1104_1110_cell",
                              "result_internet_MultiMulti_1104_1110_cell"
                     ], help="data file name")  
    psr.add_argument("-c","--cellIdList", nargs="*",
                     default=["04259",
                              "04456",
                              "05060",
                              "05200",
                              "05085",
                              "04703"], help="list of cell IDs")  
    psr.add_argument("-x","--xlabel", required=True, help="label of x-axis")  
    psr.add_argument("-y","--ylabel", required=True, help="label of y-axis")  
    return psr.parse_args()


def plotMultiGraphs(prefix,
                    listOfFileName,
                    key,
                    explanation_xlabel,
                    explanation_ylabel):
    nrows = -(-len(listOfFileName) // 2)  # 切り上げ演算 -(-4 // 3)
    i = 0
    for fileName in listOfFileName :
        fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(9, 9),sharex=True, sharey=True) 
        data = pd.read_csv(fileName, header=0)
        ax[i%nrows, i//nrows].plot(data.index,data[key])
        ax[i%nrows, i//nrows].set_title(epoch)
        ax[i%nrows, i//nrows].axes.xaxis.set_ticklabels([])
        ax[i%nrows, i//nrows].axes.yaxis.set_ticklabels([])
        i = i+1
    # plt.tight_layout()
    plt.legend()
    ghFileName = prefix+'.pdf'
    plt.savefig(ghFileName)
    plt.show()

def plotMultiGraphsFromTwoDF(prefix,
                               list1OfFileName,
                               list2OfFileName,
                               key1,
                               key2,
                               explanation_xlabel,
                               explanation_ylabel):
    nrows = -(-len(listOfFileName) // 2)  # 切り上げ演算 -(-4 // 3)
    i = 0
    for file1Name, file2Name in zip(list1OfFileName, list2OfFileName) :
        fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(9, 9),sharex=True, sharey=True) 
        data1 = pd.read_csv(file1Name, header=0)
        data2 = pd.read_csv(file2Name, header=0)
        ax[i%nrows, i//nrows].plot(data1.index,data[key1])
        ax[i%nrows, i//nrows].plot(data2.index,data[key2])
        ax[i%nrows, i//nrows].set_title(epoch)
        ax[i%nrows, i//nrows].axes.xaxis.set_ticklabels([])
        ax[i%nrows, i//nrows].axes.yaxis.set_ticklabels([])
        i = i+1
    # plt.tight_layout()
    plt.legend()
    ghFileName = prefix+'.pdf'
    plt.savefig(ghFileName)
    plt.show()

def setConfig(self):
    setOfPlots=[
        {data_tyep : [prefixOfFilename,key,xlabel,ylabel]},
        #
        {activityFactor : ['xiData_internet_1104_1110.csv',"Normalized Sum (total)","Time","Activity factor"]},  # xiはセルによらずシステム共通
        #
        {traffic : ["trafficData_internet_1104_1110_cell","cell04259","Time","Traffic rate [Mbps]"]},
        {population : ["popData_internet_1104_1110_cell","cell04259","Time", "Population"]},
        #
        {SO_inputTrafficData : ["infoOriginal_internet_1104_1110_cell","traffic","Time","Traffic [Mbps]"]},
        {SO_resultData1 : ["result_SingleOriginal_internet_1104_1110_cell","predicted-traffic","Time","Predicted traffic rate [Mbps]"]},
        {SO_resultData2 : ["result_SingleOriginal_internet_1104_1110_cell","xi","Time","Predicted activity factor"]},
        {SO_resultData3 : ["result_SingleOriginal_internet_1104_1110_cell","population","Time","Population"]},
        {SO_resultData4 : ["result_SingleOriginal_internet_1104_1110_cell","Nv1","Time","Number of predicted active users"]},
        #
        {SS_inputTrafficData : ["infoSingle_internet_1104_1110_cell","traffic","Time","Traffic [Mbps]"]},
        {SS_resultData1 : ["result_SingleSingle_internet_1104_1110_cell","predicted-traffic","Time","Predicted traffic rate [Mbps]"]},
        {SS_resultData2 : ["result_SingleSingle_internet_1104_1110_cell","xi","Time","Predicted activity factor"]},
        {SS_resultData3 : ["result_SingleSingle_internet_1104_1110_cell","population","Time","Population"]},
        {SS_resultData4 : ["result_SingleSingle_internet_1104_1110_cell","Nv1","Time","Number of predicted active users"]},
        #
        #
        {MS1_inputTrafficdata : ["infoMulti_internet_1104_1110_cell","traffic","Time","Traffic [Mbps]"]},
        {MS1_resultData1 : ["result_MultiSingle1_internet_1104_1110_cell","predicted-traffic","Time","Predicted traffic rate [Mbps]"]},
        {MS1_resultData2 : ["result_MultiSingle1_internet_1104_1110_cell","xi","Time","Predicted activity factor"]},
        {MS1_resultData3 : ["result_MultiSingle1_internet_1104_1110_cell","population","Time","Population"]},
        {MS1_resultData4 : ["result_MultiSingle1_internet_1104_1110_cell","Nv1","Time","Number of predicted active users"]},
        #
        {MS2_inputTrafficdata : ["infoMulti_internet_1104_1110_cell","traffic","Time","Traffic [Mbps]"]}, # same as MS1
        {MS2_resultData1 : ["result_MultiSingle2_internet_1104_1110_cell","predicted-traffic","Time","Predicted traffic rate [Mbps]"]},
        {MS2_resultData2 : ["result_MultiSingle2_internet_1104_1110_cell","xi","Time","Predicted activity factor"]},
        {MS2_resultData3 : ["result_MultiSingle2_internet_1104_1110_cell","population","Time","Population"]},
        {MS2_resultData4 : ["result_MultiSingle2_internet_1104_1110_cell","Nv1","Time","Number of predicted active users"]},
        #
        {MM_inputTrafficdata : ["infoMulti_internet_1104_1110_cell","traffic","Time","Traffic [Mbps]"]}, # same as MS1
        {MM_resultData1 : ["result_MultiMulti_internet_1104_1110_cell","predicted-traffic","Time","Predicted traffic rate [Mbps]"]},
        {MM_resultData2 : ["result_MultiMulti_internet_1104_1110_cell","xi","Time","Predicted activity factor"]},
        {MM_resultData3 : ["result_MultiMulti_internet_1104_1110_cell","population","Time","Population"]},
        {MM_resultData4 : ["result_MultiMulti_internet_1104_1110_cell","Nv1","Time","Number of predicted active users"]},
    ]
    
              


if __name__ == '__main__':
    args = get_args()
    output = args.output
    mkdir(output)
    listOfPrefixOfDataFileName = args.listOfPrefixOfDataFileName
    print(listOfPrefixOfDataFileName)
    cellIdList = list(args.cellIdList)
    print(cellIdList)
    xlabel = args.xlabel
    print(xlabel)

    listOfPrefixOfDataFileName =["trafficData_internet_1104_1110_cell",
                                 "popData_internet_1104_1110_cell"]
    for prefix in listOfPrefixOfDataFileName :
        listOfFileName=[]
        for cell in cellIdList :
            fname = prefix + str(cell) + ".csv"
            listOfFileName.append(fname)
            print(fname)
        plotMultiGraphs(prefix=prefix,
                        listOfFileName=listOfFileName,
                        key="traffic",
                        explanation_xlabel="Time",
                        explanation_ylabel="Traffic rate [Mbps]")
    sys.exit()

    list1 =["infoOriginal_internet_1104_1110_cell"]
    list2 =["result_SingleOriginal_internet_1104_1110_cell"]
    for prefix in listOfPrefixOfDataFileName :
        listOfFileName=[]
        for cell in cellIdList :
            fname = prefix + str(cell) + ".csv"
            listOfFileName.append(fname)
            print(fname)
            plotMultiGraphsFromTwoDF(prefix=prefix,
                                       list1OfFileName=list1,
                                       list2OfFileName=list2,
                                       key1="traffic",
                                       key2="traffic",
                                       explanation_xlabel="Time",
                                       explanation_ylabel="Traffic rate [Mbps]")
    sys.exit()



path = pathlib.Path(output)
print("output directory ---------------------------------------------------------")
print(path.resolve())
print("--------------------------------------------------------------------------")



# import json

# d = {"name":"ndj", "place":["Qiita", "Twitter", "YouTube"], "age": 25}

# with open("ndj.json", mode="w") as f:
#     d = json.dumps(d)
#     f.write(d)
# # ndj.json
# # {
# #     "name": "ndj", 
# #     "place": ["Qiita", "Twitter", "YouTube"], 
# #     "age": 25
# # }


# {
#     "datafile": "xiData_internet_1104_1110.csv",
#     "scope": "all",
#     "y_axis": "xi",
#     "xlabel": "Time",
#     "ylabel": "Activity factor"
# }
# {
#     "datafile": "trafficData_internet_1104_1110_cell",
#     "scope": "part",
#     "y_axis": "traffic",
#     "xlabel": "Time",
#     "ylabel": "Traffic rate (Mbps)"
#     "cells": ["04259",
#               "04456",
#               "05060",
#               "05200",
#               "05085",
#               "04703"]
# }
# {
#     "datafile": "popData_internet_1104_1110_cell",
#     "scope": "part",
#     "y_axis": "population",
#     "xlabel": "Time",
#     "ylabel": "Population"
#     "cells": ["04259",
#               "04456",
#               "05060",
#               "05200",
#               "05085",
#               "04703"]
# }
# {
#     "datafile": "infoOriginal_internet_1104_1110_cell",
#     "scope": "part",
#     "y_axis": "population",
#     "xlabel": "Time",
#     "ylabel": ""
#     "cells": ["04259",
#               "04456",
#               "05060",
#               "05200",
#               "05085",
#               "04703"]
# }

                              
#                               "result_SingleOriginal_internet_1104_1110_cell",
#                               "infoSingle_internet_1104_1110_cell",
#                               "result_SingleSingle_internet_1104_1110_cell",
#                               "infoMulti_internet_1104_1110_cell",
#                               "result_MultiSingle1_internet_1104_1110_cell",
#                               "result_MultiSingle2_internet_1104_1110_cell",
#                               "result_internet_MultiMulti_1104_1110_cell"
#                      ], help="data file name")  
#     psr.add_argument("-c","--cellIdList", nargs="*",
#                      default=["04259",
#                               "04456",
#                               "05060",
#                               "05200",
#                               "05085",
#                               "04703"], help='list of cell IDs')  

    
