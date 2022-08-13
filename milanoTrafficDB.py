# milano gridトラフィック変動の時系列グラフを作成するプログラム
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15,10
import datetime
import argparse
import seaborn as sns
import numpy as np

import sys

import matplotlib.dates as mdates

class milanoTrafficDB():
    # milano grid traffic data
    # trafficData_internet_1104_1117.csv
    # time,Norimalized Sum (total),Sum (total),cell04259,cell04456,cell05060,cell05200,cell05085,cell04703
    # 2013-11-03 23:00:00,0.5560133731168918,589247.9261802054,164.54480015570186,724.1616341721386,143.1902454320498,51.51321121658152,14.019635271759675,1.6079584682686865
    def __init__(self,
                 csvInputFileName,
                 ts_type,
                 pjName,
                 t0,
                 t1
    ) :
        self.csvInputFileName = csvInputFileName
        self.ts_type = ts_type
        self.pjName = pjName
        self.t0 = t0
        self.t1 = t1
        #
        self.df = pd.read_csv(self.csvInputFileName, header=0)
        # self.df.index=self.df['times']
        self.df.index=self.df['time']

        self.t0str = self.t0.strftime('%Y-%m-%d %H:%M:%S')
        self.t1str = self.t1.strftime('%Y-%m-%d %H:%M:%S')
        print(f'# start time is {self.t0str}.')
        print(f'# end time is {self.t1str}.')
        #
        self.df = self.df[self.t0str:self.t1str]
        # self.df.index = pd.to_datetime(self.df['times'], format='%Y-%m-%d %H:%M:%S') # 2005-05-04 15:30:00
        self.df.index = pd.to_datetime(self.df['time'], format='%Y-%m-%d %H:%M:%S') # 2005-05-04 15:30:00
        #
        self.cityList = [['cell04259','cell04456','cell05060','cell05200','cell05085','cell04703']]
        # self.cityList = [['cell04259','cell04456','cell05060','cell05200','cell05085','cell04703','Sum (total)']]
        self.fileNamePrefix = f"milano{self.ts_type}TS_{self.pjName}"
        self.ghFileNamePrefix = f"pic/milano{self.ts_type}TS_{self.pjName}"
        self.texFileNamePrefix = f"tex/milano{self.ts_type}TS_{self.pjName}"


    def show(self):
        print(self.df)

    def plot_gh(self,
                explanation_xlabel,
                explanation_ylabel):
        # cityGroupの要素は3つ上にする必要がある。axを2次元にするため。
        for cityGroup in self.cityList:
            idx = self.cityList.index(cityGroup)
            print(idx)
            print(cityGroup)
            fig, ax = plt.subplots(nrows=-(-len(cityGroup) // 2), ncols=2, figsize=(12, 9),sharex=True, sharey=True) # 切り上げ演算 -(-4 // 3)
            i = 0
            for city in cityGroup :
                ax[i//2, i%2].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))
                ax[i//2, i%2].plot(self.df.index,self.df[city])
                ax[i//2, i%2].set_title(city)
                # ax[i//2, i%2].set_xlabel("Time")
                # ax[i//2, i%2].set_ylabel("Traffic volume")
                ax[i//2, i%2].set_xlabel(explanation_xlabel)
                ax[i//2, i%2].set_ylabel(explanation_ylabel)
                i = i+1
            plt.tight_layout()
            plt.legend()
            ghFileName = self.ghFileNamePrefix+f'_{idx}.pdf'
            plt.savefig(ghFileName)
            plt.show()

    def plot_ghByCity(self):
        texFileName = self.texFileNamePrefix+'_ByCity.tex'
        with open(texFileName, 'w') as tex_source :
            tex_source.write("%%%%%\n")
            tex_source.write("%%%%%\n")
            tex_source.write("%%%%%\n")
        for cityGroup in self.cityList:
            idx = self.cityList.index(cityGroup)
            print(idx)
            print(cityGroup)
            i = 0
            for city in cityGroup :
                fig,ax = plt.subplots(1,1,figsize=(12,9),sharex=True,sharey=True)
                plt.xlabel("Time")
                plt.ylabel("Traffic volume per unit time")
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))
                ax.plot(self.df.index,self.df[city])
                i = i+1
                plt.tight_layout()
                plt.legend()
                ghFileName = self.ghFileNamePrefix+f'_{city}.pdf'
                plt.savefig(ghFileName)
                plt.show()
                # ghFileNamePrefixCity = self.fileNamePrefix+f'_{city}'
                # msg = 'Fig.~\\ref{gh-'+ghFileNamePrefixCity+'} shows time series of traffic volume of city '+city+' (period: from '+self.t0.strftime('%Y-%m-%d')+' to '+self.t1.strftime('%Y-%m-%d')+', city: '+city+').\n'
                # msg = msg+'\\begin{figure}[ht] \n'\
                # '  \\includegraphics[clip,width=0.9\hsize]{'+self.ghFileNamePrefix+'_'+city+'.pdf}\n'\
                # '  \\caption{Time Series of the traffic volume of city '+city+' (period: from '+self.t0.strftime('%Y-%m-%d')+' to '+self.t1.strftime('%Y-%m-%d')+', city: '+city+').}\n'\
                # '  \\label{gh-'+ghFileNamePrefixCity+'}\n' \
                # '\\end{figure}\n\n'
                # with open(texFileName, 'a') as tex_source :
                #     tex_source.write(msg)
                # print(msg)

    def _genTeXFigureBlock(self,pjNameIdx,explanation1,explanation2,explanation3) :
        msg = f'Fig.~\\ref{{gh-{pjNameIdx}}} shows {explanation1} {explanation2} {explanation3}.\n'
        msg = msg+f'\\begin{{figure}}[ht] \n'\
            +f'  \\includegraphics[clip,width=0.9\hsize]{{pic/{pjNameIdx}.pdf}}\n'\
            +f'  \\caption{{{explanation1} {explanation2} {explanation3}.}}\n'\
            +f'  \\label{{gh-{pjNameIdx}}}\n' \
            +f'\\end{{figure}}\n\n'
        return msg
    
    def gen_tex(self,explanation1,explanation2):
        texFileName = self.texFileNamePrefix+'.tex'
        with open(texFileName, 'w') as tex_source :
            tex_source.write("%%%%%\n")
            tex_source.write("%%%%%\n")
            tex_source.write("%%%%%\n")
        for cityGroup in self.cityList:
            idx = self.cityList.index(cityGroup)
            print(idx)
            print(cityGroup)
            cityList = ''
            for city in cityGroup :
                cityList += ' '
                cityList += city
            print(cityList)
            pjNameIdx = self.pjName+f'_{idx}'
            explanation3 = '(city: '+str(cityList)+')'
            msg = self._genTeXFigureBlock(pjNameIdx,explanation1,explanation2, explanation3)
            with open(texFileName, 'a') as tex_source :
                tex_source.write(msg)
            print(msg)


class simpleTSDB():
    def __init__(self,
                 csvInputFileName,
                 ts_type,
                 pjName,
                 t0,
                 t1
    ) :
        self.csvInputFileName = csvInputFileName
        self.ts_type = ts_type
        self.pjName = pjName
        self.t0 = t0
        self.t1 = t1
        #
        self.df = pd.read_csv(self.csvInputFileName, header=0)
        self.df.index=self.df['time']

        self.t0str = self.t0.strftime('%Y-%m-%d %H:%M:%S')
        self.t1str = self.t1.strftime('%Y-%m-%d %H:%M:%S')
        print(f'# start time is {self.t0str}.')
        print(f'# end time is {self.t1str}.')
        #
        self.df = self.df[self.t0str:self.t1str]
        self.df.index = pd.to_datetime(self.df['time'], format='%Y-%m-%d %H:%M:%S') # 2005-05-04 15:30:00
        self.fileNamePrefix = f"milano{self.ts_type}TS_{self.pjName}"
        self.ghFileNamePrefix = f"pic/milano{self.ts_type}TS_{self.pjName}"
        self.texFileNamePrefix = f"tex/milano{self.ts_type}TS_{self.pjName}"


    def show(self):
        print(self.df)

    def plot_gh(self,
                explanation_xlabel,
                explanation_ylabel):
        fig,ax = plt.subplots(1,1,figsize=(6,3),sharex=True,sharey=True)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))
        #
        # self.df.plot()
        ax.plot(self.df.index,self.df.iloc[:,1])
        ax.set_xlabel(explanation_xlabel)
        ax.set_ylabel(explanation_ylabel)
        plt.tight_layout()
        plt.legend()
        ghFileName = self.ghFileNamePrefix+f'.pdf'
        plt.savefig(ghFileName)
        plt.show()

    def _genTeXFigureBlock(self,pjNameIdx,explanation1,explanation2,explanation3) :
        msg = f'Fig.~\\ref{{gh-{pjNameIdx}}} shows {explanation1} {explanation2} {explanation3}.\n'
        msg = msg+f'\\begin{{figure}}[ht] \n'\
            +f'  \\includegraphics[clip,width=0.9\hsize]{{pic/{pjNameIdx}.pdf}}\n'\
            +f'  \\caption{{{explanation1} {explanation2} {explanation3}.}}\n'\
            +f'  \\label{{gh-{pjNameIdx}}}\n' \
            +f'\\end{{figure}}\n\n'
        return msg
    
    def gen_tex(self,explanation1,explanation2):
        texFileName = self.texFileNamePrefix+'.tex'
        with open(texFileName, 'w') as tex_source :
            tex_source.write("%%%%%\n")
            tex_source.write("%%%%%\n")
            tex_source.write("%%%%%\n")
        pjNameIdx = self.pjName
        explanation3 = ''
        msg = self._genTeXFigureBlock(pjNameIdx,explanation1,explanation2, explanation3)
        with open(texFileName, 'a') as tex_source :
            tex_source.write(msg)
        print(msg)

            

class milanoHeatMap():
    # milano grid traffic data
    # trafficData_internet_1104_1117.csv
    # time,Norimalized Sum (total),Sum (total),cell04259,cell04456,cell05060,cell05200,cell05085,cell04703
    # 2013-11-03 23:00:00,0.5560133731168918,589247.9261802054,164.54480015570186,724.1616341721386,143.1902454320498,51.51321121658152,14.019635271759675,1.6079584682686865
    def __init__(self,
                 csvInputFileName,
                 hm_type,
                 pjName,
                 t0,
                 t1
    ) :
        self.csvInputFileName = csvInputFileName
        self.hm_type = hm_type
        self.pjName = pjName
        self.t0 = t0
        self.t1 = t1
        #
        self.df = pd.read_csv(self.csvInputFileName, header=0)
        # self.df.index=self.df['times']
        self.df.index=self.df['time']

        self.t0str = self.t0.strftime('%Y-%m-%d %H:%M:%S')
        self.t1str = self.t1.strftime('%Y-%m-%d %H:%M:%S')
        print(f'# start time is {self.t0str}.')
        print(f'# end time is {self.t1str}.')
        #
        #
        # self.cityList = [['cell04259','cell04456','cell05060','cell05200','cell05085','cell04703']]
        #
        listOfGroupCellIds = [i for i in range(1,10001)]
        self.cityList = []
        for cell in listOfGroupCellIds:
            self.cityList.append(f'cell{cell:05}')
        #
        self.df = self.df[self.t0str:self.t1str]
        # self.df.index = pd.to_datetime(self.df['times'], format='%Y-%m-%d %H:%M:%S') # 2005-05-04 15:30:00
        self.df.index = pd.to_datetime(self.df['time'], format='%Y-%m-%d %H:%M:%S') # 2005-05-04 15:30:00
        self.listOfHMData = {}
        # self.listOfSampleHours = [2,6,10,14,18,22]
        self.listOfSampleHours = [6,9,12,14,16,18,20,22]
        self.maxData = 0.0
        self.minData = float('inf')
        for time, rows in self.df.iterrows():
            if time >= self.t0 and time <= self.t1:
                year = time.year
                month = time.month
                day = time.day
                hour = time.hour
                minute = time.minute
                second = time.second
                if hour in self.listOfSampleHours :
                    if minute == 0 and second == 0 :
                        data = np.zeros((100, 100))
                        for city in self.cityList:
                            idx = self.cityList.index(city)
                            x = (idx - 1) % 100
                            y = (idx - 1) // 100
                            # if float(rows[city]) > 50.:
                            #     rows[city] = 50.
                            data[x,y] = float(rows[city])
                        if np.nanmax(data) >= self.maxData :
                            self.maxData = np.nanmax(data)
                        if np.nanmin(data) <= self.minData :
                            self.minData = np.nanmax(data)
                        self.listOfHMData[time]=data
        # self.maxData = self.df.max(numeric_only=True).max()
        print("maxData")
        print(self.maxData)
        print("minData")
        print(self.minData)
        self.fileNamePrefix = f"milano{self.hm_type}HM_{self.pjName}"
        self.ghFileNamePrefix = f"pic/milano{self.hm_type}HM_{self.pjName}"
        self.texFileNamePrefix = f"tex/milano{self.hm_type}HM_{self.pjName}"

    def show(self):
        print(self.df)

    def plotHeatMap(self,
                    explanation_xlabel,
                    explanation_ylabel):
        isFirst = True
        nrows = -(-len(self.listOfSampleHours) // 2)  # 切り上げ演算 -(-4 // 3)
        for epoch, data in self.listOfHMData.items() :
            if isFirst == True:
                isFirst = False
                day = epoch.day
                i = 0
                idx = 0
                # fig, ax = plt.subplots(nrows=-(-len(self.listOfSampleHours) // 2), ncols=2, figsize=(12, 9),sharex=True, sharey=True) # 切り上げ演算 -(-4 // 3)
                fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(9, 9),sharex=True, sharey=True)
                cbar_ax = fig.add_axes([.91, .3, .03, .4])
            elif epoch.day != day :
                # plt.tight_layout()
                plt.legend()
                ghFileName = self.ghFileNamePrefix+f'_{idx}.pdf'
                plt.savefig(ghFileName)
                plt.show()
                day = epoch.day
                i = 0
                idx += 1
                # fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(9, 9),sharex=True, sharey=True) 
                fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(9, 9/0.96),sharex=True, sharey=True) 
                # cbar_ax = fig.add_axes([.91, .3, .03, .4])
                cbar_ax = fig.add_axes([.91, .3, .01, .1])
            t = sns.heatmap(data, ax = ax[i%nrows, i//nrows],
                            cbar=i == 0,
                            # vmin = self.minData, vmax = self.maxData,
                            vmin = 0, vmax = self.maxData,
                            square=True,
                            cmap="Reds",
                            cbar_ax=None if i else cbar_ax,
                            cbar_kws = dict(use_gridspec=False,label='population'))
            # fig.tight_layout(rect=[0, 0, .9, 1])
            fig.tight_layout(rect=[0,0,1,0.96])
            ax[i%nrows, i//nrows].set_title(epoch)
            ax[i%nrows, i//nrows].axes.xaxis.set_ticklabels([])
            ax[i%nrows, i//nrows].axes.yaxis.set_ticklabels([])
            ax[i%nrows, i//nrows].invert_yaxis() # (1,1) and (100,100) are the bottom-left and top-right in the milano grid
            i = i+1
        # plt.tight_layout()
        plt.legend()
        ghFileName = self.ghFileNamePrefix+f'_{idx}.pdf'
        plt.savefig(ghFileName)
        plt.show()

        # #
        # df = pd.DataFrame(np.random.random((10,10,)))
        # fig, axn = plt.subplots(2, 2, sharex=True, sharey=True)
        # cbar_ax = fig.add_axes([.91, .3, .03, .4])
        # for i, ax in enumerate(axn.flat):
        #     sns.heatmap(df, ax=ax,
        #                 cbar=i == 0,
        #                 vmin=0, vmax=1,
        #                 cbar_ax=None if i else cbar_ax)
        #     fig.tight_layout(rect=[0, 0, .9, 1])
        # #


    # def _genTeXFigureBlock(self,pjNameIdx,explanation1,explanation2,explanation3) :
    #     msg = f'Fig.~\\ref{{gh-{pjNameIdx}}} shows {explanation1} {explanation2} {explanation3}.\n'
    #     msg = msg+f'\\begin{{figure}}[ht] \n'\
    #         +f'  \\includegraphics[clip,width=0.9\hsize]{{pic/{pjNameIdx}.pdf}}\n'\
    #         +f'  \\caption{{{explanation1} {explanation2} {explanation3}.}}\n'\
    #         +f'  \\label{{gh-{pjNameIdx}}}\n' \
    #         +f'\\end{{figure}}\n\n'
    #     return msg
    
    # def gen_tex(self,explanation1,explanation2):
    #     texFileName = self.texFileNamePrefix+'.tex'
    #     with open(texFileName, 'w') as tex_source :
    #         tex_source.write("%%%%%\n")
    #         tex_source.write("%%%%%\n")
    #         tex_source.write("%%%%%\n")
    #     for cityGroup in self.cityList:
    #         idx = self.cityList.index(cityGroup)
    #         print(idx)
    #         print(cityGroup)
    #         cityList = ''
    #         for city in cityGroup :
    #             cityList += ' '
    #             cityList += city
    #         print(cityList)
    #         pjNameIdx = self.pjName+f'_{idx}'
    #         explanation3 = '(city: '+str(cityList)+')'
    #         msg = self._genTeXFigureBlock(pjNameIdx,explanation1,explanation2, explanation3)
    #         with open(texFileName, 'a') as tex_source :
    #             tex_source.write(msg)
    #         print(msg)

        
