# モデル式において各uCPU,uMEMは100倍されているのでその逆処理をする必要があることに注意
# トラフィックデータの単位時間が900秒の場合は係数を9とする。geant
# トラフィックデータの単位時間が600秒の場合は係数を6とする。milano grid

# pystan 2.19.0.0
# scipy 1.5.2

import argparse

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pystan
from scipy.stats import norm
import math
from itertools import zip_longest
import datetime
import time

from matplotlib.pylab import rcParams

from common.tools import mkdir

print("pystan 2.19.0.0 was used to test the program.")
print("pystan version is used as follows...")
print(pystan.__version__)

rcParams['figure.figsize'] = 15,10

parser=argparse.ArgumentParser(description='This program predict the traffic assuming two classes traffic.')
#parser.add_argument('arg1', help='この引数の説明（なくてもよい）')    # 必須の引数を追加
#parser.add_argument('--arg3')    # オプション引数（指定しなくても良い引数）を追加
#parser.add_argument('-a', '--arg4')   # よく使う引数なら省略形があると使う時に便利
parser.add_argument("-od", "--output", type=str, default="output")  # 結果出力先ディレクトリ
parser.add_argument('-f','--fileName',default='info_internet_Original_1104_1110_cell04259.csv', help='File name of Input data')  
parser.add_argument('-o','--outfileName',default='result_internet_SingleOriginal_1104_1110_cell04259.csv', help='File name of Output data')  
parser.add_argument("--uTraffic","-t",default=1.0, type=float, help='bps (Mbps)')
parser.add_argument("--uCPUave","-cave",default=25.0, type=float, help='CPU')
parser.add_argument("--uMEMave","-mave",default=80.0, type=float, help='MEM')
parser.add_argument("--uCPUstd","-cstd",default=0.1, type=float, help='CPU for class 1')
parser.add_argument("--uMEMstd","-mstd",default=0.3, type=float, help='MEM for class 1')
#
parser.add_argument("--sampleNum","-sN", default=6, type=int, help="sliding window size for MCMC")

args=parser.parse_args()
output = args.output
mkdir(output)
input_file_name = args.output+"/"+args.fileName
output_file_name = args.output+"/"+args.outfileName
utrafficave = args.uTraffic
uCPUave = args.uCPUave
uMEMave = args.uMEMave
uCPUstd = args.uCPUstd
uMEMstd = args.uMEMstd
#sampleNum = 5
sampleNum = args.sampleNum



trafficPred = []
utraffic1Pred = []
utraffic2Pred = []
uCPU_1 = []
uCPU_2 = []
uMEM_1 = []
uMEM_2 = []
xi1Pred = []
xi2Pred = []
NPred = []
Nv1Pred = []
Nv2Pred = []

mcmccode = """
data {
    int N;
    int traffic[N];
    int population[N];
    int CPU[N];
    int MEM[N];
    real utraffic_ave;
    real uCPUave;
    real uMEMave;
    real uCPUstd;
    real uMEMstd;
}

parameters {
    real <lower=0,upper=1> xi;
}

model {
    for(i in 1:N){
        CPU[i] ~ normal(uCPUave*population[i]*xi,uCPUstd*sqrt(population[i]*xi));
        MEM[i] ~ normal(uMEMave*population[i]*xi,uMEMstd*sqrt(population[i]*xi));
        traffic[i] ~ poisson(utraffic_ave*population[i]*xi);
    }
}   
"""

data = pd.read_csv(input_file_name,index_col=0)
population = data['pop']
dataNum = len(population)

#合計値を入力とする
traffic = data['traffic']
CPU = data['CPU']
MEM = data['MEM']
# utrafficave = data['utrafficave']
# uCPUave = data['uCPUave']
# uMEMave = data['uMEMave']


#グラフ化するときの位置合わせ
# for i in range(5):
for i in range(sampleNum):
    trafficPred.append(np.nan)
    utraffic1Pred.append(np.nan)
    utraffic2Pred.append(np.nan)
    xi1Pred.append(np.nan)
    xi2Pred.append(np.nan)
    NPred.append(np.nan)
    Nv1Pred.append(np.nan)
    Nv2Pred.append(np.nan)




for i in range(dataNum):
    if i > sampleNum-1 :
        populationDF = population[i-(sampleNum):i:1]#iからサンプル数個分渡す
        populationList = populationDF.values.tolist()#Listへキャスト
        populationInput = [int(f) for f in populationList]
        dataDF = traffic[i-(sampleNum):i:1]
        dataList = dataDF.values.tolist()
        dataInput = [int(f) for f in dataList]
        CPUDF = CPU[i-(sampleNum):i:1]
        CPUList = CPUDF.values.tolist()
        CPUInput = [int(f) for f in CPUList]
        MEMDF = MEM[i-(sampleNum):i:1]
        MEMList = MEMDF.values.tolist()
        MEMInput = [int(f) for f in MEMList]

        # utrafficaveInput = int(utrafficave)
        # uCPUaveInput = int(uCPUave)
        # uMEMaveInput = int(uMEMave)
        utrafficaveInput = float(utrafficave)
        uCPUaveInput = float(uCPUave)
        uMEMaveInput = float(uMEMave)
        # 2022-05-05
        uCPUstdInput = uCPUstd
        uMEMstdInput = uMEMstd
        
        standata = {'N':len(populationInput),
                    'population':populationInput,
                    'traffic':dataInput,
                    'CPU':CPUInput,'MEM':MEMInput,
                    'utraffic_ave':utrafficaveInput,
                    'uCPUave':uCPUaveInput,'uMEMave':uMEMaveInput,
                    'uCPUstd':uCPUstdInput,'uMEMstd':uMEMstdInput}
        print(standata)

        sm = pystan.StanModel(model_code=mcmccode)
        fit_nuts = sm.sampling(data=standata, chains=4, iter=5000)

        print(fit_nuts)

        ms = fit_nuts.extract()
        predictedxi = np.mean(ms['xi'])
        xi1Pred.append(predictedxi)
        NPred.append(population[i])
        Nv1Pred.append(round(population[i]*predictedxi))
        trafficPred.append(np.mean(utrafficave*population[i]*predictedxi))


df = pd.DataFrame(trafficPred,columns=['predicted-traffic'])
df['predicted-xi'] = xi1Pred
df['predicted-population'] = NPred
df['predicted-Nv1'] = Nv1Pred #class-1のアクティブ人口
df.to_csv(output_file_name,index=False)
