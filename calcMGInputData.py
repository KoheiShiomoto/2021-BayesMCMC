import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from UserTrafficModelMix import UserTraffic
import argparse

#classオプションでシングルクラス用のデータを作成する
def get_args():
    psr= argparse.ArgumentParser(description='This program predict the traffic assuming two classes traffic.')
    #parser.add_argument('arg1', help='この引数の説明（なくてもよい）')    # 必須の引数を追加
    #parser.add_argument('--arg3')    # オプション引数（指定しなくても良い引数）を追加
    #parser.add_argument('-a', '--arg4')   # よく使う引数なら省略形があると使う時に便利
    psr.add_argument('-c') # class number
    psr.add_argument('--duration', type=float, default=600, help='unit time of time series traffic/population (sec)')   # 600=(10*60) seconds at milano grid
    psr.add_argument('-i','--inputFileNameOriginalTraffic',default='trafficData_internet_1104_1117.csv', help='File name of Input data')  
    psr.add_argument('-f','--fileName',default='popdata_cell04259.csv', help='File name of Input data')  
    psr.add_argument('-iXi','--inXiFileName', default='output/xiData_internet_1104_1117.csv', help='File name of Input Xi data')  
    psr.add_argument('-o','--outfileName',default='cellXXXXXinfoSingleMilanoGrid.csv', help='File name of Output data')  
    psr.add_argument("--mixRate1","-mr1",default=0.8, type=float, help='ratio of class 1 over total')
    psr.add_argument("--mixRate2","-mr2",default=0.2, type=float, help='ratio of class 2 over total')
    psr.add_argument("--uTraffic1","-t1",default=1.0, type=float, help='bps for class 1 (Mbps)')
    psr.add_argument("--uTraffic2","-t2",default=4.0, type=float, help='bps for class 2 (Mbps)')
    psr.add_argument("--uCPU1","-c1",default=25, type=float, help='CPU for class 1')
    psr.add_argument("--uCPU2","-c2",default=25, type=float, help='CPU for class 2')
    psr.add_argument("--uMEM1","-m1",default=80, type=float, help='MEM for class 1')
    psr.add_argument("--uMEM2","-m2",default=80, type=float, help='MEM for class 2')
    psr.add_argument('--arrivalRate1','-ar1',default=1.25, type=float, help='arrival rate 1')
    psr.add_argument('--arrivalRate2','-ar2',default=6.25, type=float, help='arrival rate 2')
    psr.add_argument('-iO','--isOriginalTraffic',action='store_true', help='make data for Milano Grid')
    psr.add_argument('-ci','--city',default='cell04259') # Bocconi, one of the most famous Universities in Milan(Square id: 4259);
    return psr.parse_args()

if __name__ == '__main__':

    args = get_args()
    duration = args.duration
    inputFileNameOriginalTraffic = args.inputFileNameOriginalTraffic
    input_file_name = args.fileName
    input_xi_file_name = args.inXiFileName
    output_file_name = args.outfileName
    mr1 = args.mixRate1
    mr2 = args.mixRate2
    utraffic1ave = 1000.0*args.uTraffic1  # convert Mbps -> kbps 
    utraffic2ave = 1000.0*args.uTraffic2  # convert Mbps -> kbps 
    uCPU1ave = args.uCPU1
    uCPU2ave = args.uCPU2
    uMEM1ave = args.uMEM1
    uMEM2ave = args.uMEM2
    arrivalRate1 = args.arrivalRate1
    arrivalRate2 = args.arrivalRate2

    pop = pd.read_csv(input_file_name,index_col=0) #population_data
    xi = pd.read_csv(input_xi_file_name,index_col=0) #xi_data
    originalTrafficData = pd.read_csv(inputFileNameOriginalTraffic,index_col=0) 

    data = pd.DataFrame(index=None)

    # aveDataSize * 8 * arrivalRate = utrafficAve (kbps) * 1000
    aveDataSize1 = 100.0 # 100 KBytes
    arrivalRate1 = utraffic1ave / (aveDataSize1*8) # arrivalRate=1.25,AveDataSize=100 -> 1Mbps?
    aveDataSize2 = 100.0 # 100 KBytes
    arrivalRate2 = utraffic2ave / (aveDataSize2*8) # arrivalRate=6.25,AveDataSize=100 -> 5Mbps?
    resource_1 = UserTraffic(arrivalRate1,aveDataSize1,uCPU1ave,0.1,uMEM1ave,0.3) # arrivalRate=1.25,AveDataSize=100 -> 1Mbps?
    resource_2 = UserTraffic(arrivalRate2,aveDataSize2,uCPU2ave,0.1,uMEM2ave,0.3) # arrivalRate=6.25,AveDataSize=100 -> 5Mbps?
    #
    # resource_1 = UserTraffic(1.25,100.0,0.25,0.1,0.8,0.3) # arrivalRate=1.25,AveDataSize=100 -> 1Mbps?
    # resource_2 = UserTraffic(6.25,100.0,1.25,0.1,4.0,0.3) # arrivalRate=6.25,AveDataSize=100 -> 5Mbps?
    print(f'mixRate1={mr1}, mixRate2={1-mr1}.')
    print(f'arrivalRate1=1.25, aveDataSize1=100.0, uCPU1ave=25, uMEM1ave=80.')
    print(f'arrivalRate1={arrivalRate1}, aveDataSize1={aveDataSize1}, uCPU1ave={uCPU1ave}, uMEM1ave={uMEM1ave}.')
    print(f'arrivalRate2=6.25, aveDataSize2=100.0, uCPU2ave=125, uMEM2ave=400.')
    print(f'arrivalRate2={arrivalRate2}, aveDataSize2={aveDataSize2}, uCPU2ave={uCPU2ave}, uMEM2ave={uMEM2ave}.')
    
    traffic = []
    CPU = []
    MEM = []
    for i in range(len(pop)):
        xiPop_1 = round(pop[args.city][i]*xi.iloc[i][0]*mr1) #class-1のアクティブ人口
        xiPop_2 = round(pop[args.city][i]*xi.iloc[i][0]*(1.0-mr1)) #class-2のアクティブ人口
        traffic_1 = float(resource_1.getGeneratedData(xiPop_1,duration)*1.0e-6/duration) # convert bps -> Mbps
        traffic_2 = float(resource_2.getGeneratedData(xiPop_2,duration)*1.0e-6/duration) # convert bps -> Mbps
        if(args.isOriginalTraffic): # Milano Gridのオリジナルのトラフィックデータを出力する
            # traffic.append('{:.1f}'.format(1000.0*originalTrafficData[args.city][i])) # Milano Gridのオリジナルデータの単位が Mbps
            traffic.append('{:.1f}'.format(1.0*originalTrafficData[args.city][i])) # Milano Gridのオリジナルデータの単位が Mbps
        else :
            traffic.append('{:.1f}'.format(float(traffic_1)+float(traffic_2))) # convert bps -> Mbps
        CPU_1 = resource_1.getGeneratedCPU(xiPop_1)
        CPU_2 = resource_2.getGeneratedCPU(xiPop_2)
        CPU.append('{:.1f}'.format(float(CPU_1)+float(CPU_2)))
        MEM_1 = resource_1.getGeneratedMEM(xiPop_1)
        MEM_2 = resource_2.getGeneratedMEM(xiPop_2)
        MEM.append('{:.1f}'.format(float(MEM_1)+float(MEM_2)))
    data['pop'] = pop[args.city]
    data['traffic'] = traffic
    data['CPU'] = CPU
    data['MEM'] = MEM

    data.index = pop.index
    data.to_csv(output_file_name)
