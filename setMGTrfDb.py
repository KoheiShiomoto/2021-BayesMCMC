import pandas as pd
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib
from datetime import datetime
from datetime import timedelta

import sys

from common.tools import mkdir

# # エリア例は以下の通り
# Bocconi, one of the most famous Universities in Milan(Square id: 4259);
# Navigli district, one of the most famous nightlifeplaces in Milan (Square id: 4456);
# Duomo, the city centre of Milan (Square id: 5060);
# Duomo, the city centre of Trento (Square id: 5200);
# Mesiano, the department of Engineering of the Uni-versity of Trento (Square id: 5085);
# Bosco della città, a forest near Trento (Square id:4703)
listOfAllCellIds = [i for i in range(1,10001)]
# listOfAllCellIds = [4259,4456,5060,5200,5085,4703]
listOfGroupCellIds = [i for i in range(1,10001)]
# listOfGroupCellIds = [4259,4456,5060,5200,5085,4703]
listOfGroupCellIdsByName = ['Bocconi(4259)','Navigli(4456)','Duomo Milan (5060)','Duomo Trento (5200)',' Mesiano (5085)','Bosco (4703)']
#
listOfTimeAndGroupCellNames=['time','Normalized Sum (total)','Sum (total)']
for cell in listOfGroupCellIds:
    listOfTimeAndGroupCellNames.append(f'cell{cell:05}')

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", type=str, default="dataset")  # datasetのディレクトリ
#
# dataset directory looks like ...
#
# dataset
# └── milano
#     ├── full-December
#     │   ├── sms-call-internet-mi-2013-12-01.txt
#     │   ├── sms-call-internet-mi-2013-12-03.txt
#     │   ├── sms-call-internet-mi-2013-12-04.txt
#     │   ├── sms-call-internet-mi-2013-12-05.txt
#     │   ├── sms-call-internet-mi-2013-12-06.txt
#     ...
#     │   ├── sms-call-internet-mi-2013-12-31.txt
#     │  └── sms-call-internet-mi-2014-01-01.txt
#     └─ full-November
#         ├── sms-call-internet-mi-2013-11-01.txt
#         ├── sms-call-internet-mi-2013-11-02.txt
#         ├── sms-call-internet-mi-2013-11-03.txt
#         ├── sms-call-internet-mi-2013-11-04.txt
#         ├── sms-call-internet-mi-2013-11-05.txt
#         ├── sms-call-internet-mi-2013-11-06.txt
#         ...
#         ├── sms-call-internet-mi-2013-11-29.txt
#         └── sms-call-internet-mi-2013-11-30.txt
#
#
# file sms-call-internet-mi-2013-11-01.txt looks like ...
#
# 1	1383264000000	0	0.029712044475285478	                  	                   	0.003574620210998875	    
# 1	1383264000000	39	0.13533928377303134	0.0849372437222577	0.05343788914147278	0.0017873101054994376	8.026269748512151
# 1	1383264600000	0	0.02730046487718618				
# 1	1383264600000	39	0.1887771729145041	0.026137424264286602	0.0017873101054994376	0.05460092975437236	8.514178577183893
# 1	1383265200000	39	0.24221506205597687	0.16031366742441833	0.10803881889584513	0.026137424264286602	6.8334248963840505
# 1	1383265800000	0	0.02730046487718618	                    	                     	0.02730046487718618	
# 1	1383265800000	39	0.2944899105845501	0.2457041838946756	0.02730046487718618	0.08073835401865896	6.55460504454769
# 1	1383266400000	0	0.026137424264286602				
# 1	1383266400000	39	0.10803881889584513	0.10803881889584513	                     	                  	7.338716012816092

parser.add_argument("-od", "--output", type=str, default="output")  # 結果出力先ディレクトリ
parser.add_argument('-o','--outFileName', default='popData_internet_1104_1117.csv', help='File name of Output data')  

parser.add_argument("-t", "--trafficType", type=str, default="internet")  # 開始日の選択

parser.add_argument("-s", "--startdate", type=str, default="2013-11-01")  # 開始日の選択
parser.add_argument("-e", "--enddate", type=str, default="2013-12-31")  # 終了日の選択
# parser.add_argument("-e", "--enddate", type=str, default="2013-11-10")  # 終了日の選択
# parser.add_argument("-e", "--enddate", type=str, default="2013-11-05")  # 終了日の選択
parser.add_argument("-p", "--person", type=int, default=1.0)  # 1人の1時間当たりの通信量 1 Mb/s 元のトラフィック量の単位がMb/sと想定
args = parser.parse_args()
output = args.output
mkdir(output)
outFileName = args.output+"/"+args.outFileName
dataset_dir = args.dataset
args.trafficType
start_date = args.startdate
end_date = args.enddate
internet_per_person = args.person

active_user = 0.8


def dateRange(start, end):
    for n in range((end - start).days + 1):
        yield start + timedelta(n)



start = datetime.strptime(start_date, "%Y-%m-%d")
end = datetime.strptime(end_date, "%Y-%m-%d")

dates_dic = []
for date in dateRange(start, end):
    month = date.month
    day = date.day
    if month == 11:
        dates_dic.append(
            f"{dataset_dir}/milano/full-November/sms-call-internet-mi-2013-{month}-{day:02}.txt"
        )
    else:
        dates_dic.append(
            f"{dataset_dir}/milano/full-December/sms-call-internet-mi-2013-{month}-{day:02}.txt"
        )

print("CellID  ------------------------------------------------------------------")
print(cell)
print("--------------------------------------------------------------------------\n")

print("range --------------------------------------------------------------------")
print(f"{start.month}/{start.day} ~ {end.month}/{end.day}")
print("--------------------------------------------------------------------------\n")

df_cdrs = pd.DataFrame({})

print("start loading dataset ----------------------------------------------------")
for file in dates_dic:
    print(f"loading {file} ...")
    df = pd.read_csv(
        file,
        names=(
            "CellID",
            "datetime",
            "countrycode",
            "smsin",
            "smsout",
            "callin",
            "callout",
            "internet",
        ),
        delimiter="\t",
        dtype={
            "CellID": int,
            "datetime": float,
            "countrycode": int,
            "smsin": float,
            "smsout": float,
            "callin": float,
            "callout": float,
        },
    )
    df_cdrs = df_cdrs.append(df)
print("finish loading dataset ----------------------------------------------------\n")

df_cdrs = df_cdrs.fillna(0)
df_cdrs["datetime"] = pd.to_datetime(df_cdrs["datetime"], unit="ms")
df_cdrs["days"] = df_cdrs["datetime"].dt.weekday
df_cdrs["sms"] = df_cdrs["smsin"] + df_cdrs["smsout"]
df_cdrs["calls"] = df_cdrs["callin"] + df_cdrs["callout"]

df_data = (
    df_cdrs[["CellID", "datetime", "internet", "calls", "sms", "days"]]
    .groupby(["CellID", "datetime"], as_index=False)
    .sum()
)

#######################
# 2022-01-19 K.S. Start
#######################
listOfTrafficType = []
listOfTrafficType.append(args.trafficType)
print(listOfTrafficType)
# for trafficType in ['internet','sms','calls']:
for trafficType in listOfTrafficType:
    # print(df_data)
    isFirst = True
    for cell in listOfAllCellIds:
        df_traffic_cell = df_data[df_data.CellID == cell][['datetime',trafficType]].reset_index(drop=True)
        df_traffic_cell.set_index('datetime',drop=False)
        df_traffic_cell.columns = ['time',f'cell{cell:05}']
        # print(df_traffic_cell)
        if isFirst == True:
            df_traffic_allCells = df_traffic_cell
            isFirst = False
        else:
            # methodだとmergeされなかった
            # df_traffic_allCells.merge(df_traffic_cell, on='time', how='outer')
            df_traffic_allCells = pd.merge(df_traffic_allCells,df_traffic_cell, on='time', how='outer')
        # print(df_traffic_allCells)
    df_traffic_allCells['Sum (total)'] = df_traffic_allCells.sum(axis = 1)
    df_traffic_allCells['Normalized Sum (total)'] = df_traffic_allCells['Sum (total)']/df_traffic_allCells['Sum (total)'].max()
    print(df_traffic_allCells)
    
    # 2022-03-04
    df_traffic_allCells.fillna(0)
    # df_traffic_allCells[start:end].to_csv(
    df_traffic_allCells.to_csv(
        outFileName,
        columns = listOfTimeAndGroupCellNames,
        index = False
    )

sys.exit()
#######################
# 2022-01-19 K.S. End
#######################


df_data["days"] = df_data["datetime"].dt.weekday
df_data = df_data[df_data.CellID == cell]
df_data["revision"] = df_data["datetime"].dt.hour
df_data = df_data.set_index(["datetime"]).sort_index()
df_data["hour"] = df_data.reset_index().index

df_data["population"] = df_data["internet"] / (active_user * internet_per_person)
df_data["population"] = df_data["population"].ewm(span=10).mean()
df_data["traffic"] = df_data["population"] * internet_per_person
f = plt.figure()

ax = df_data[df_data.CellID == cell]["population"].plot(
    label="population"
)
sns.despine()

box = ax.get_position()

ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
ax.legend(
    loc="upper center", bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5
)

plt.legend()

plt.xlabel("weekly hours")
plt.ylabel("population")
plt.savefig(
    f"{output}/{cell}_population_{start.month}_{start.day}_{end.month}_{end.day}.png"
)

df_data.to_csv(
    f"{output}/{cell}_population_{start.month}_{start.day}_{end.month}_{end.day}.csv"
)

path = pathlib.Path(output)
print("output directory ---------------------------------------------------------")
print(path.resolve())
print("--------------------------------------------------------------------------")
