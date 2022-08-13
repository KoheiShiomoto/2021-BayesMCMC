import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import datetime
import argparse

from common.tools import mkdir

from UserTrafficModelMix import UserTraffic

#classオプションでシングルクラス用のデータを作成する
def get_args():
    psr= argparse.ArgumentParser(description='This program extract a city traffic from the entire traffic database.')
    #parser.add_argument('arg1', help='この引数の説明（なくてもよい）')    # 必須の引数を追加
    #parser.add_argument('--arg3')    # オプション引数（指定しなくても良い引数）を追加
    #parser.add_argument('-a', '--arg4')   # よく使う引数なら省略形があると使う時に便利
    psr.add_argument("-od", "--output", type=str, default="output")  # 結果出力先ディレクトリ
    psr.add_argument('-i','--inputFileName',default='output/trafficData_internet_1104_1117.csv', help='File name of Input data')  
    psr.add_argument('-o','--outFileName',default='output/trafficData_internet_1104_1117_cellXXXX.csv', help='File name of Output data')  
    psr.add_argument("-s", "--startdate", type=str, default="2013-11-01")  # 開始日の選択
    psr.add_argument("-e", "--enddate", type=str, default="2013-12-31")  # 終了日の選択
    # psr.add_argument("-e", "--enddate", type=str, default="2013-11-10")  # 終了日の選択
    # psr.add_argument("-e", "--enddate", type=str, default="2013-11-05")  # 終了日の選択
    psr.add_argument('-ci','--city',default='cell04259') # Bocconi, one of the most famous Universities in Milan(Square id: 4259);
    #
    return psr.parse_args()

if __name__ == '__main__':

    args = get_args()
    output = args.output
    mkdir(output)
    inputFileName = args.output+"/"+args.inputFileName
    outputFileName = args.output+"/"+args.outFileName
    start_date = args.startdate
    end_date = args.enddate
    city = args.city

    # 2013-11-03 23:00:00
    tt0 = datetime.datetime.strptime(args.startdate, "%Y-%m-%d")
    tt1 = datetime.datetime.strptime(args.enddate, "%Y-%m-%d")
    # # 2018-02-01 12:15:30.002000
    t0 = datetime.datetime(tt0.year, tt0.month, tt0.day, 00, 00, 0, 0)
    t1 = datetime.datetime(tt1.year, tt1.month, tt1.day, 23, 59, 59, 59)
    #
    t0str = t0.strftime('%Y-%m-%d %H:%M:%S')
    t1str = t1.strftime('%Y-%m-%d %H:%M:%S')
    print(f'# start time is {t0str}.')
    print(f'# end time is {t1str}.')

    data = pd.read_csv(inputFileName,index_col=0)
    data[t0str:t1str][city].to_csv(outputFileName)
