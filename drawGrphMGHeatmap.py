#人口の平滑化を行うプログラム
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15,10
import datetime
import argparse

import sys

from common.tools import mkdir

import milanoTrafficDB

def get_args():
    psr = argparse.ArgumentParser()
    psr.add_argument("-od", "--output", type=str, default="output")  # 結果出力先ディレクトリ
    psr.add_argument('-i','--inTrfMtxFileName', default='trafficData_internet_1104_1117.csv', help='File name of Input Time Series Traffic Matrix data')  
    psr.add_argument('-iPop','--inPopFileName', default='popData_internet_1104_1117.csv', help='File name of Input Time Series Population data')  
    psr.add_argument('-pj','--pjName', default='pjName', help='project name')  

    #
    # default start time is '2013-11-03 23:00'
    # default end   time is '2013-11-17 22:50'
    psr.add_argument("-s", "--startdate", type=str, default="2013-11-01")  # 開始日の選択
    psr.add_argument("-e", "--enddate", type=str, default="2013-12-31")  # 終了日の選択
    # #
    # psr.add_argument('-y0','--year0',default=2013, type=int, help='start year of period.')  
    # psr.add_argument('-m0','--month0',default=11, type=int, help='start month of period.')  
    # psr.add_argument('-d0','--day0',default=3, type=int, help='start day of period.')  
    # psr.add_argument('-h0','--hour0',default=23, type=int, help='start hour of period.')  
    # psr.add_argument('-mi0','--minute0',default=00, type=int, help='start minute of period.')  
    # psr.add_argument('-y1','--year1',default=2013, type=int, help='end year of period.') 
    # psr.add_argument('-m1','--month1',default=11, type=int, help='end month of period.') 
    # psr.add_argument('-d1','--day1',default=17, type=int, help='end day of period.') 
    # psr.add_argument('-h1','--hour1',default=22, type=int, help='end hour of period.') 
    # psr.add_argument('-mi1','--minute1',default=50, type=int, help='end minute of period.') 
    return psr.parse_args()

if __name__ == '__main__':
    args = get_args()
    output = args.output
    mkdir(output)
    inTrfMtxFileName = output+"/"+args.inTrfMtxFileName
    data = pd.read_csv(inTrfMtxFileName, header=0)
    #
    inPopFileName = output+"/"+args.inPopFileName
    #
    pjName = args.pjName
    # data.index=data['times']
    data.index=data['time']

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
    #
    # year0 = int(args.year0)
    # month0 = int(args.month0)
    # day0 = int(args.day0)
    # hour0 = int(args.hour0)
    # minute0 = int(args.minute0)
    # year1 = int(args.year1)
    # month1 = int(args.month1)
    # day1 = int(args.day1)
    # hour1 = int(args.hour1)
    # minute1 = int(args.minute1)
    # # dt = datetime.datetime(2018, 2, 1, 12, 15, 30, 2000)
    # # print(dt)
    # # # 2018-02-01 12:15:30.002000
    # t0 = datetime.datetime(year0, month0, day0, hour0, minute0, 0, 0)
    # t1 = datetime.datetime(year1, month1, day1, hour1, minute1, 0, 0)
    # # print(f'# start time is {t0}.')
    # # print(f'# end time is {t1}.')
    # t0str = t0.strftime('%Y-%m-%d %H:%M:%S')
    # t1str = t1.strftime('%Y-%m-%d %H:%M:%S')
    # print(f'# start time is {t0str}.')
    # print(f'# end time is {t1str}.')

    engine = milanoTrafficDB.milanoHeatMap(csvInputFileName=inPopFileName,
                                           hm_type = "Population",
                                           pjName = pjName,
                                           t0 = t0,
                                           t1 = t1
    )
    engine.show()
    engine.plotHeatMap(explanation_xlabel = "Time",
                       explanation_ylabel = "Population")
    # engine.gen_tex(explanation1 = 'time series of population',
    #                explanation2 = '(period: from '+t0str+' to '+t1str+')')

