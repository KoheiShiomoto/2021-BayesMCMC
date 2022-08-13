#単一クラスとしてみた際のグラフ化
#cオプション(1 or 2)でクラス指定，-rオプション（引数なし）で相対誤差の出力

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from matplotlib import ticker
import argparse

import matplotlib.dates as mdates

from common.tools import mkdir

rcParams['font.size'] = 20


def get_args():
    psr = argparse.ArgumentParser()
    psr.add_argument("-od", "--output", type=str, default="output")  # 結果出力先ディレクトリ
    psr.add_argument("-pd", "--picdir", type=str, default="pic")  # 結果出力先ディレクトリ
    psr.add_argument('--resultFile', help='File name of Input data')  
    psr.add_argument('--inputFile', help='File name of Input data')  
    psr.add_argument('--pjName', default='test', help='ProjectName')  
    psr.add_argument('-r','--relative',action='store_true',help='output relative error graph')
    return psr.parse_args()

if __name__ == '__main__':
    args = get_args()
    output = args.output
    mkdir(output)
    picdir = args.picdir
    mkdir(picdir)
    resultFileName = args.output+"/"+args.resultFile
    inputFileName = args.output+"/"+args.inputFile
    pjName = args.pjName
    p = pd.read_csv(resultFileName)
    d = pd.read_csv(inputFileName)
    #
    #
    #
    df_1 = pd.concat([d,p], axis=1) 
    df_1.index = df_1['time']
    df_1.index = pd.to_datetime(df_1.index)
    fig,ax = plt.subplots(1,1,figsize=(12,9),sharex=True,sharey=True)
    ax.plot(df_1.index,df_1['traffic'],label='actual')
    ax.plot(df_1.index,df_1['predicted-traffic'],label='predicted')
    plt.xlabel("Time")
    plt.ylabel("Traffic volume (Mbps)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"{picdir}/{pjName}_ActualPredictedTraffic.pdf")
    plt.show()
    #
    fig,ax = plt.subplots(1,1,figsize=(12,9),sharex=True,sharey=True)
    ax.plot(df_1.index,df_1['predicted-xi'],label='xi')
    plt.xlabel("Time")
    plt.ylabel("Predicted Activity Factor, Xi")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"{picdir}/{pjName}_PredictedActivityFactor.pdf")
    plt.show()
    #
    fig,ax = plt.subplots(1,1,figsize=(12,9),sharex=True,sharey=True)
    ax.plot(df_1.index,df_1['predicted-population'],label='poplation')
    plt.xlabel("Time")
    plt.ylabel("Predicted Population")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"{picdir}/{pjName}_PredictedPopulation.pdf")
    plt.show()
    #
    fig,ax = plt.subplots(1,1,figsize=(12,9),sharex=True,sharey=True)
    ax.plot(df_1.index,df_1['predicted-Nv1'],label='Nv1')
    plt.xlabel("Time")
    plt.ylabel("Predicted Nv1")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"{picdir}/{pjName}_PredictedNv1.pdf")
    plt.show()
    #
    #
    #
    c = d['traffic']
    r = []
    for i in range(len(c)):
        r.append(NaN)
    dr = pd.DataFrame(r,columns=['rate'])
    if(args.relative):
        for i in range(len(c)):
            if(p['predicted-traffic'][i] != NaN):
                diff = p['predicted-traffic'][i] - c[i]
                diff = abs(diff)
                dr['rate'][i] = diff / c[i]
            else:
                dr['rate'][i] = NaN
        #
        fig = plt.figure(figsize=(12,8))
        ax = subplot(111)
        ax.plot(c,label='actual traffic',color='blue')
        ax.plot(p['predicted-traffic'],label='predicted traffic',color='orange')
        ax.set_xticks([0,96,192,288,384,480])
        ax.set_xticklabels(['0','23','47','71','95','119'])
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(4))
        plt.xlabel('Time(hour)')
        plt.ylabel('Bandwidth(Mbps)')
        plt.tight_layout()
        plt.legend()
        plt.grid()
        plt.savefig(f"{picdir}/{pjName}_IdeActualPredictedTraffic.pdf")
        plt.show()
        #
        fig = plt.figure(figsize=(12,8))
        ax = subplot(111)
        ax.plot(dr,color='orange')
        ax.set_xticks([0,96,192,288,384,480])
        ax.set_xticklabels(['0','23','47','71','95','119'])
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(4))
        plt.xlabel('Time(hour)')
        plt.ylabel('Relative Error')
        plt.tight_layout()
        plt.grid()
        plt.savefig(f"{picdir}/{pjName}_IdeRelativeError.pdf")
        plt.show()
    else:
        #実際の誤差のグラフ化
        diff_list = []

        for i in range(len(c)):
            if(p['predicted-traffic'][i] != NaN):
                diff = p['predicted-traffic'][i] - c[i]
                diff_list.append(diff)
                #diff = abs(diff)
                #dr['rate'][i] = diff / c[i]
            else:
                dr['rate'][i] = NaN
                diff_list.append(np.nan)
        #actual trafficとpredicted-trafficをプロット
        fig = plt.figure(figsize=(12,8))
        ax = subplot(111)
        ax.plot(c,label='actual traffic',color='blue')
        ax.plot(p['predicted-traffic'],label='predicted traffic',color='orange')
        ax.set_xticks([0,96,192,288,384,480])
        ax.set_xticklabels(['0','23','47','71','95','119'])
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(4))
        plt.xlabel('Time(hour)')
        plt.ylabel('Bandwidth(Mbps)')
        plt.tight_layout()
        plt.legend()
        plt.grid()
        plt.savefig(f"{picdir}/{pjName}_IdeActualPredictedTraffic.pdf")
        plt.show()
        #
        fig = plt.figure(figsize=(12,8))
        ax = subplot(111)
        ax.plot(diff_list,color='orange')
        ax.set_xticks([0,96,192,288,384,480])
        ax.set_xticklabels(['0','23','47','71','95','119'])
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(4))
        plt.xlabel('Time(hour)')
        plt.ylabel('Error')
        plt.tight_layout()
        plt.grid()
        plt.savefig(f"{picdir}/{pjName}_IdeRelativeError.pdf")
        plt.show()
