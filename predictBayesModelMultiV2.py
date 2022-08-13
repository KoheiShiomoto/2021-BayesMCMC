# モデル式において各uCPU,uMEMは100倍されているのでその逆処理をする必要があることに注意
# トラフィックデータの単位時間が900秒の場合は係数を9とする。geant
# トラフィックデータの単位時間が600秒の場合は係数を6とする。milano grid


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
parser.add_argument("--uTraffic1","-t1",default=1.0, type=float, help='bps for class 1 (Mbps)')
parser.add_argument("--uTraffic2","-t2",default=4.0, type=float, help='bps for class 2 (Mbps)')
parser.add_argument("--uCPU1ave","-cave1",default=25, type=float, help='CPU for class 1')
parser.add_argument("--uCPU2ave","-cave2",default=25, type=float, help='CPU for class 2')
parser.add_argument("--uMEM1ave","-mave1",default=80, type=float, help='MEM for class 1')
parser.add_argument("--uMEM2ave","-mave2",default=80, type=float, help='MEM for class 2')
parser.add_argument("--uCPU1std","-cstd1",default=0.1, type=float, help='CPU for class 1')
parser.add_argument("--uCPU2std","-cstd2",default=0.1, type=float, help='CPU for class 2')
parser.add_argument("--uMEM1std","-mstd1",default=0.3, type=float, help='MEM for class 1')
parser.add_argument("--uMEM2std","-mstd2",default=0.3, type=float, help='MEM for class 2')
#
parser.add_argument("--sampleNum","-sN", default=6, type=int, help="sliding window size for MCMC")

args=parser.parse_args()
output = args.output
mkdir(output)
input_file_name = args.output+"/"+args.fileName
output_file_name = args.output+"/"+args.outfileName
utraffic1ave = args.uTraffic1
utraffic2ave = args.uTraffic2
uCPU1ave = args.uCPU1ave
uCPU2ave = args.uCPU2ave
uMEM1ave = args.uMEM1ave
uMEM2ave = args.uMEM2ave
# 2022-05-05
uCPU1std = args.uCPU1std
uCPU2std = args.uCPU2std
uMEM1std = args.uMEM1std
uMEM2std = args.uMEM2std
#sampleNum = 5
sampleNum = args.sampleNum


trafficPred = []
utraffic1Pred = []
utraffic2Pred = []
uCPU_1 = []
uCPU_2 = []
uMEM_1 = []
uMEM_2 = []
xiPred = []
xi1Pred = []
xi2Pred = []
NPred = []
Nv1Pred = []
Nv2Pred = []
ptraffic_1 = []
ptraffic_2 = []


mcmccode = """
data {
    int N;
    int traffic[N];
    int population[N];
    real CPU[N];
    real MEM[N];
    real utraffic1ave;
    real utraffic2ave;
    real uCPU1ave;
    real uCPU2ave;
    real uMEM1ave;
    real uMEM2ave;
    real uCPU1std;
    real uCPU2std;
    real uMEM1std;
    real uMEM2std;
}

parameters {
    real <lower=0,upper=1.0> xi1;
    real <lower=0,upper=1.0> xi2;
}

model {
    for(i in 1:N){
        MEM[i] ~ normal(uMEM1ave*population[i]*xi1+uMEM2ave*population[i]*xi2,sqrt(population[i]*xi1*uMEM1std*uMEM1std+population[i]*xi2*uMEM2std*uMEM2std)); 
        CPU[i] ~ normal(uCPU1ave*population[i]*xi1+uCPU2ave*population[i]*xi2,sqrt(population[i]*xi1*uCPU1std*uCPU1std+population[i]*xi2*uCPU2std*uCPU2std));
        traffic[i] ~ poisson((utraffic1ave*population[i]*xi1)+(utraffic2ave*xi2*population[i]));
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


#グラフ化するときの位置合わせ
# for i in range(5):
for i in range(sampleNum):
    trafficPred.append(np.nan)
    utraffic1Pred.append(np.nan)
    utraffic2Pred.append(np.nan)
    xiPred.append(np.nan)
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

        # utraffic1aveInput = int(utraffic1ave)
        # utraffic2aveInput = int(utraffic2ave)
        utraffic1aveInput = float(utraffic1ave)
        utraffic2aveInput = float(utraffic2ave)

        # uCPU1aveInput = int(uCPU1ave)
        # uCPU2aveInput = int(uCPU2ave)
        uCPU1aveInput = float(uCPU1ave)
        uCPU2aveInput = float(uCPU2ave)

        # uMEM1aveInput = int(uMEM1ave)
        # uMEM2aveInput = int(uMEM2ave)
        uMEM1aveInput = float(uMEM1ave)
        uMEM2aveInput = float(uMEM2ave)

        # 2022-05-05
        uCPU1stdInput = float(uCPU1std)
        uCPU2stdInput = float(uCPU2std)
        uMEM1stdInput = float(uMEM1std)
        uMEM2stdInput = float(uMEM2std)
 
        standata = {'N':len(populationInput), 'population':populationInput, 'traffic':dataInput, 'CPU':CPUInput, 'MEM':MEMInput,
                    'utraffic1ave':utraffic1aveInput, 'utraffic2ave':utraffic2aveInput,
                    'uCPU1ave':uCPU1aveInput, 'uCPU2ave':uCPU2aveInput,
                    'uMEM1ave':uMEM1aveInput, 'uMEM2ave':uMEM2aveInput,
                    'uCPU1std':uCPU1stdInput,'uCPU2std':uCPU2stdInput,
                    'uMEM1std':uMEM1stdInput,'uMEM2std':uMEM2stdInput}
        print(standata)

        sm = pystan.StanModel(model_code=mcmccode)
        fit_nuts = sm.sampling(data=standata,
                               chains=4, # chain is normally 4.
                               iter=5000, # iter is normally 2000.
                               warmup=1000, # warmup is normally 1/iter.
                               thin=1)  # thin is normally 3.
        # https://logics-of-blue.com/stan%E3%81%AB%E3%82%88%E3%82%8B%E3%83%99%E3%82%A4%E3%82%BA%E6%8E%A8%E5%AE%9A%E3%81%AE%E5%9F%BA%E7%A4%8E/
        #
        # https://mc-stan.org/rstan/reference/stanmodel-method-sampling.html
        #
        # object	
        # An object of class stanmodel.
        #
        # data	
        # A named list or environment providing the data for the model
        # or a character vector for all the names of objects used as
        # data. See the Passing data to Stan section in stan. 
        #
        # pars	
        # A vector of character strings specifying parameters of
        # interest. The default is NA indicating all parameters in the
        # model. If include = TRUE, only samples for parameters named
        # in pars are stored in the fitted results. Conversely, if
        # include = FALSE, samples for all parameters except those
        # named in pars are stored in the fitted results.  
        #
        # chains	
        # A positive integer specifying the number of Markov
        # chains. The default is 4. 
        # iter	
        # A positive integer specifying the number of iterations for
        # each chain (including warmup). The default is 2000. 
        #
        # warmup	
        # A positive integer specifying the number of warmup (aka
        # burnin) iterations per chain. If step-size adaptation is on
        # (which it is by default), this also controls the number of
        # iterations for which adaptation is run (and hence these
        # warmup samples should not be used for inference). The number
        # of warmup iterations should be smaller than iter and the
        # default is iter/2. 
        #
        # thin	
        # A positive integer specifying the period for saving
        # samples. The default is 1, which is usually the recommended
        # value. 
        #
        # seed	
        # The seed for random number generation. The default is
        # generated from 1 to the maximum integer supported by R on
        # the machine. Even if multiple chains are used, only one seed
        # is needed, with other chains having seeds derived from that
        # of the first chain to avoid dependent samples. When a seed
        # is specified by a number, as.integer will be applied to
        # it. If as.integer produces NA, the seed is generated
        # randomly. The seed can also be specified as a character
        # string of digits, such as "12345", which is converted to
        # integer. 
        #
        # init	
        # Initial values specification. See the detailed documentation
        # for the init argument in stan. 
        #
        # check_data	
        # Logical, defaulting to TRUE. If TRUE the data will be
        # preprocessed; otherwise not. See the Passing data to Stan
        # section in stan. 
        #
        # sample_file	
        # An optional character string providing the name of a
        # file. If specified the draws for all parameters and other
        # saved quantities will be written to the file. If not
        # provided, files are not created. When the folder specified
        # is not writable, tempdir() is used. When there are multiple
        # chains, an underscore and chain number are appended to the
        # file name prior to the .csv extension. 
        # 
        # diagnostic_file	
        # An optional character string providing the name of a
        # file. If specified the diagnostics data for all parameters
        # will be written to the file. If not provided, files are not
        # created. When the folder specified is not writable,
        # tempdir() is used. When there are multiple chains, an
        # underscore and chain number are appended to the file name
        # prior to the .csv extension. 
        # 
        # verbose	
        # TRUE or FALSE: flag indicating whether to print intermediate
        # output from Stan on the console, which might be helpful for
        # model debugging. 
        #
        # algorithm	
        # One of sampling algorithms that are implemented in
        # Stan. Current options are "NUTS" (No-U-Turn sampler, Hoffman
        # and Gelman 2011, Betancourt 2017), "HMC" (static HMC), or
        # "Fixed_param". The default and preferred algorithm is
        # "NUTS". 
        # 
        # control	
        # A named list of parameters to control the sampler's
        # behavior. See the details in the documentation for the
        # control argument in stan. 
        # 
        # include	
        # Logical scalar defaulting to TRUE indicating whether to
        # include or exclude the parameters given by the pars
        # argument. If FALSE, only entire multidimensional parameters
        # can be excluded, rather than particular elements of them. 
        # 
        # cores	
        # Number of cores to use when executing the chains in
        # parallel, which defaults to 1 but we recommend setting the
        # mc.cores option to be as many processors as the hardware and
        # RAM allow (up to the number of chains). 
        # 
        # open_progress	
        # Logical scalar that only takes effect if cores > 1 but is
        # recommended to be TRUE in interactive use so that the
        # progress of the chains will be redirected to a file that is
        # automatically opened for inspection. For very short runs,
        # the user might prefer FALSE. 
        # 
        # show_messages	
        # Either a logical scalar (defaulting to TRUE) indicating
        # whether to print the summary of Informational Messages to
        # the screen after a chain is finished or a character string
        # naming a path where the summary is stored. Setting to FALSE
        # is not recommended unless you are very sure that the model
        # is correct up to numerical error. 


        print(fit_nuts)

        ms = fit_nuts.extract()
        predictedxi1 = np.mean(ms['xi1'])
        predictedxi2 = np.mean(ms['xi2'])
        xiPred.append(predictedxi1+predictedxi2)
        xi1Pred.append(predictedxi1)
        xi2Pred.append(predictedxi2)
        NPred.append(population[i])
        Nv1Pred.append(round(population[i]*predictedxi1))
        Nv2Pred.append(round(population[i]*predictedxi2))
        trafficPred.append(np.mean(utraffic1ave*population[i]*predictedxi1)+
        np.mean(utraffic2ave*population[i]*predictedxi2))



df = pd.DataFrame(trafficPred,columns=['predicted-traffic'])
df['predicted-xi'] = xiPred
df['predicted-xi1'] = xi1Pred
df['predicted-xi2'] = xi2Pred
#df['utraffic1'] = utraffic1Pred
#df['utraffic2'] = utraffic2Pred
df['predicted-population'] = NPred
df['predicted-Nv1'] = Nv1Pred #class-1のアクティブ人口
df['predicted-Nv2'] = Nv2Pred #class-2のアクティブ人口
df.to_csv(output_file_name,index=False)
