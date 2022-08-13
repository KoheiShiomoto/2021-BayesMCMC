import math
import numpy as np
import numpy.random as rd
import scipy.stats as st

def PoissonRv(rate):
    #平均rateのポアソン分布に従う乱数を生成する関数（1は個数）
    value = rd.poisson(rate,1)
    return value

class UserTraffic:
    #averageArrivalRate = 1/sec, averageDataSize = kB
    def __init__(self,averageArrivalRate=0.3,averageDataSize=100.0, aveCPU=0.25, stdCPU=0.1, aveMEM=0.8, stdMEM = 0.3):
        
        
        self.averageDataSize = averageDataSize * 1000 * 8
        self.averageArrivalRate = averageArrivalRate

        #u^CPU = Normal(0.25, 0.1)
        self.aveCPU = aveCPU
        self.stdCPU = stdCPU

        #u^MEM = Normal(0.8, 0,3)
        self.aveMEM = aveMEM
        self.stdMEM = stdMEM

    #duration秒間のトラフィック量(bits)を計算する関数
    def getGeneratedData(self,NoUsers,duration):
        return(self.averageDataSize*PoissonRv(NoUsers*self.averageArrivalRate*duration))

    def getGeneratedActiveData(self,NoUsers,duration,xi):
        return(self.averageDataSize*PoissonRv(NoUsers*xi*self.averageArrivalRate*duration))

    def getGeneratedCPU(self,NoUsers):
        # return(rd.normal(self.aveCPU,self.stdCPU)*NoUsers)
        return(rd.normal(self.aveCPU*NoUsers,self.stdCPU*math.sqrt(NoUsers)))

    def getGeneratedMEM(self,NoUsers):
        # return(rd.normal(self.aveMEM,self.stdMEM)*NoUsers)
        return(rd.normal(self.aveMEM*NoUsers,self.stdMEM*math.sqrt(NoUsers)))

    def getGeneratedOrigin(self,ActiveUsers,xi):
        return(int(PoissonRv(ActiveUsers/xi)))
    
    def show_config(self):#設定したパラメータが出るようプリントする
        print('AveAR{},AveDS{},AveC{},StdC{},AveM{},StdM{}'.format(self.averageArrivalRate,self.averageDataSize,self.aveCPU,self.stdCPU,self.aveMEM,self.stdMEM))
        return 0
    '''
        def show_config(self,averageArrivalRate,averageDataSize, aveCPU, stdCPU, aveMEM, stdMEM):
            print('AveAR{},AveDS{},AveC{},StdC{},AveM{},StdM{}'.format(averageArrivalRate,averageDataSize,aveCPU,stdCPU,aveMEM,stdMEM))#設定したパラメータが出るようプリントする
            return 0
    '''

    #returns aveCPU or aveMEM
    def rCPUave(self):
        return(self.aveCPU)

    def rMEMave(self):
        return(self.aveMEM)

    
