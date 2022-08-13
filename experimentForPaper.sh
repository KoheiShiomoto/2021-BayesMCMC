


#############################################
# Step1.sh

#!/bin/bash

# # エリア例は以下の通り
# Bocconi, one of the most famous Universities in Milan(Square id: 4259);
# Navigli district, one of the most famous nightlifeplaces in Milan (Square id: 4456);
# Duomo, the city centre of Milan (Square id: 5060);
# Duomo, the city centre of Trento (Square id: 5200);
# Mesiano, the department of Engineering of the Uni-versity of Trento (Square id: 5085);
# Bosco della città, a forest near Trento (Square id:4703)

# Please un-comment if needed
# ----------------------------------------------------------------------------------------------------------------------------------------------------
# prepare the traffic data from Milano Grid dataset
# KSHR_make_populationV2.py --> setMGTrfDb.py
python3 setMGTrfDb.py -s 2013-11-04 -e 2013-11-10 -t internet -od output -o trafficData_internet_1104_1110.csv
python3 setMGTrfDb.py -s 2013-11-11 -e 2013-11-17 -t internet -od output -o trafficData_internet_1111_1117.csv
python3 setMGTrfDb.py -s 2013-11-04 -e 2013-11-17 -t internet -od output -o trafficData_internet_1104_1117.csv
# compute the population data
# KS_apd_MilanoGridNeo.py --> setMGPopDbXiDb.py
python3 setMGPopDbXiDb.py -s 2013-11-04 -e 2013-11-10 --alpha 0.1 --xiBase 0.2 -od output -i trafficData_internet_1104_1110.csv -o popData_internet_1104_1110.csv -oXi xiData_internet_1104_1110.csv
python3 setMGPopDbXiDb.py -s 2013-11-11 -e 2013-11-17 --alpha 0.1 --xiBase 0.2 -od output -i trafficData_internet_1111_1117.csv -o popData_internet_1111_1117.csv -oXi xiData_internet_1111_1117.csv
python3 setMGPopDbXiDb.py -s 2013-11-04 -e 2013-11-17 --alpha 0.1 --xiBase 0.2 -od output -i trafficData_internet_1104_1117.csv -o popData_internet_1104_1117.csv -oXi xiData_internet_1104_1117.csv
# make the graph of time series data of traffic and population
# KS_graphTimeseriesTrafficMilano.py --> drawGrphMGTrfTS.py
python3 drawGrphMGTrfTS.py -s 2013-11-04 -e 2013-11-10 -od output -i trafficData_internet_1104_1110.csv -iPop popData_internet_1104_1110.csv -iXi xiData_internet_1104_1110.csv --pjName internet_1104_1110
python3 drawGrphMGTrfTS.py -s 2013-11-11 -e 2013-11-17 -od output -i trafficData_internet_1111_1117.csv -iPop popData_internet_1111_1117.csv -iXi xiData_internet_1111_1117.csv --pjName internet_1111_1117
python3 drawGrphMGTrfTS.py -s 2013-11-04 -e 2013-11-17 -od output -i trafficData_internet_1104_1117.csv -iPop popData_internet_1104_1117.csv -iXi xiData_internet_1104_1117.csv --pjName internet_1104_1117
# make the graph of heatmap of traffic and population
python drawGrphMGHeatmap.py  -s 2013-11-04 -e 2013-11-10 -od output -iPop popData_internet_1104_1110.csv --pjName internet_1104_1110
python drawGrphMGHeatmap.py  -s 2013-11-11 -e 2013-11-17 -od output -iPop popData_internet_1111_1117.csv --pjName internet_1111_1117
python drawGrphMGHeatmap.py  -s 2013-11-04 -e 2013-11-17 -od output -iPop popData_internet_1104_1117.csv --pjName internet_1104_1117


# for cellId in {04259,04456,04703,05060,05085,05200}
for cellId in {04259,04456,05060,05200}
do
    python3 getAreaData.py -s 2013-11-04 -e 2013-11-10 -ci cell${cellId} -od output -i trafficData_internet_1104_1110.csv -o trafficData_internet_1104_1110_cell${cellId}.csv 
    python3 getAreaData.py -s 2013-11-04 -e 2013-11-10 -ci cell${cellId} -od output -i popData_internet_1104_1110.csv -o popData_internet_1104_1110_cell${cellId}.csv 
    cp output/xiData_internet_1104_1110.csv output/xiData_internet_1104_1110_cell${cellId}.csv
    python3 getAreaData.py -s 2013-11-11 -e 2013-11-17 -ci cell${cellId} -od output -i trafficData_internet_1111_1117.csv -o trafficData_internet_1111_1117_cell${cellId}.csv 
    python3 getAreaData.py -s 2013-11-11 -e 2013-11-17 -ci cell${cellId} -od output -i popData_internet_1111_1117.csv -o popData_internet_1111_1117_cell${cellId}.csv 
    cp output/xiData_internet_1111_1117.csv output/xiData_internet_1111_1117_cell${cellId}.csv
    python3 getAreaData.py -s 2013-11-04 -e 2013-11-17 -ci cell${cellId} -od output -i trafficData_internet_1104_1117.csv -o trafficData_internet_1104_1117_cell${cellId}.csv 
    python3 getAreaData.py -s 2013-11-04 -e 2013-11-17 -ci cell${cellId} -od output -i popData_internet_1104_1117.csv -o popData_internet_1104_1117_cell${cellId}.csv 
    cp output/xiData_internet_1104_1117.csv output/xiData_internet_1104_1117_cell${cellId}.csv
done



#######################################
# ToyMode.sh

#!/bin/bash


# expand the limit of number of open files from 1024 to 4096 to allow the stan to open a large number of files 
ulimit -n 4096

# 入力データ作成 人口データとトラフィックデータについてそれぞれ２パータン(Flat, Step)を組み合わせ
for PopType in {Flat,Step}
do
    for XiType in {Flat,Step}
    do
	python3 calcMGInputDataV2.py --duration 600 -c 1 -ci cell04456 -od outputToy -i trafficData_internet_1104_1110_cell04456.csv  -f popData_cell${PopType}.csv -iXi xiData_cell${XiType}.csv -o info_cellPop${PopType}Xi${XiType}.csv  --mixRate1 1.0 --uTraffic1 1.0 --uCPU1ave 0.25 --uMEM1ave 0.80 --uCPU1std 0.1 --uMEM1std 0.3
    done
done

# ベイズ推定　単一クラスモデル sampleNum 1
for PopType in {Flat,Step}
do
    for XiType in {Flat,Step}
    do
	python3 predictBayesModelSingleV2.py --sampleNum 1 -od outputToy -f info_cellPop${PopType}Xi${XiType}.csv -o result_cellPop${PopType}Xi${XiType}_sn01.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3
	python3 drawGrphPredictResultSingle.py -od outputToy -pd picToy --resultFile result_cellPop${PopType}Xi${XiType}_sn01.csv --inputFile info_cellPop${PopType}Xi${XiType}.csv --pjName cellPop${PopType}Xi${XiType}_sn01
    done
done
python3 plotInputAndResultsToy.py  --experimentName _sn01 --ymaxTraffic 2000.0 --ymaxPopulation 15000 -od outputToy -Xi xiData_cell -pT trafficData_internet_1104_1110_cell -pP popData_cell -pI info_cell -pR result_cell --cellIdList PopFlatXiFlat PopFlatXiStep PopStepXiFlat PopStepXiStep 

# ベイズ推定　単一クラスモデル sampleNum 2
for PopType in {Flat,Step}
do
    for XiType in {Flat,Step}
    do
	python3 predictBayesModelSingleV2.py --sampleNum 2 -od outputToy -f info_cellPop${PopType}Xi${XiType}.csv -o result_cellPop${PopType}Xi${XiType}_sn02.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3
	python3 drawGrphPredictResultSingle.py -od outputToy -pd picToy --resultFile result_cellPop${PopType}Xi${XiType}_sn02.csv --inputFile info_cellPop${PopType}Xi${XiType}.csv --pjName cellPop${PopType}Xi${XiType}_sn02
    done
done
python3 plotInputAndResultsToy.py  --experimentName _sn02 --ymaxTraffic 2000.0 --ymaxPopulation 15000 -od outputToy -Xi xiData_cell -pT trafficData_internet_1104_1110_cell -pP popData_cell -pI info_cell -pR result_cell --cellIdList PopFlatXiFlat PopFlatXiStep PopStepXiFlat PopStepXiStep 

# ベイズ推定　単一クラスモデル sampleNum 3
for PopType in {Flat,Step}
do
    for XiType in {Flat,Step}
    do
	python3 predictBayesModelSingleV2.py --sampleNum 3 -od outputToy -f info_cellPop${PopType}Xi${XiType}.csv -o result_cellPop${PopType}Xi${XiType}_sn03.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3
	python3 drawGrphPredictResultSingle.py -od outputToy -pd picToy --resultFile result_cellPop${PopType}Xi${XiType}_sn03.csv --inputFile info_cellPop${PopType}Xi${XiType}.csv --pjName cellPop${PopType}Xi${XiType}_sn03
    done
done
python3 plotInputAndResultsToy.py  --experimentName _sn03 --ymaxTraffic 2000.0 --ymaxPopulation 15000 -od outputToy -Xi xiData_cell -pT trafficData_internet_1104_1110_cell -pP popData_cell -pI info_cell -pR result_cell --cellIdList PopFlatXiFlat PopFlatXiStep PopStepXiFlat PopStepXiStep 

# ベイズ推定　単一クラスモデル sampleNum 4
for PopType in {Flat,Step}
do
    for XiType in {Flat,Step}
    do
	python3 predictBayesModelSingleV2.py --sampleNum 4 -od outputToy -f info_cellPop${PopType}Xi${XiType}.csv -o result_cellPop${PopType}Xi${XiType}_sn04.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3
	python3 drawGrphPredictResultSingle.py -od outputToy -pd picToy --resultFile result_cellPop${PopType}Xi${XiType}_sn04.csv --inputFile info_cellPop${PopType}Xi${XiType}.csv --pjName cellPop${PopType}Xi${XiType}_sn04
    done
done
python3 plotInputAndResultsToy.py  --experimentName _sn04 --ymaxTraffic 2000.0 --ymaxPopulation 15000 -od outputToy -Xi xiData_cell -pT trafficData_internet_1104_1110_cell -pP popData_cell -pI info_cell -pR result_cell --cellIdList PopFlatXiFlat PopFlatXiStep PopStepXiFlat PopStepXiStep 

# ベイズ推定　単一クラスモデル sampleNum 6
for PopType in {Flat,Step}
do
    for XiType in {Flat,Step}
    do
	python3 predictBayesModelSingleV2.py --sampleNum 6 -od outputToy -f info_cellPop${PopType}Xi${XiType}.csv -o result_cellPop${PopType}Xi${XiType}_sn06.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3
	python3 drawGrphPredictResultSingle.py -od outputToy -pd picToy --resultFile result_cellPop${PopType}Xi${XiType}_sn06.csv --inputFile info_cellPop${PopType}Xi${XiType}.csv --pjName cellPop${PopType}Xi${XiType}_sn06
    done
done
python3 plotInputAndResultsToy.py  --experimentName _sn06 --ymaxTraffic 2000.0 --ymaxPopulation 15000 -od outputToy -Xi xiData_cell -pT trafficData_internet_1104_1110_cell -pP popData_cell -pI info_cell -pR result_cell --cellIdList PopFlatXiFlat PopFlatXiStep PopStepXiFlat PopStepXiStep 






##########################################################################
# Step2Single.sh

#!/bin/bash

# # エリア例は以下の通り
# Bocconi, one of the most famous Universities in Milan(Square id: 4259);
# Navigli district, one of the most famous nightlifeplaces in Milan (Square id: 4456);
# Duomo, the city centre of Milan (Square id: 5060);
# Duomo, the city centre of Trento (Square id: 5200);
# Mesiano, the department of Engineering of the Uni-versity of Trento (Square id: 5085);
# Bosco della città, a forest near Trento (Square id:4703)


# expand the limit of number of open files from 1024 to 4096 to allow the stan to open a large number of files 
ulimit -n 4096

# 1104-1110 ----------------------------------------------------------------------------------------------------------------------------------------------------
# 単一クラス
# 入力トラフィックモデルの生成
# 入力トラフィックはMilano Gridのオリジナルデータを使用 
# for cellId in {04259,04456,04703,05060,05085,05200}
for cellId in {04259,04456,05060,05200}
do
    python3 calcMGInputDataV2.py --duration 600 --isOriginalTraffic -ci cell${cellId} -od output -i trafficData_internet_1104_1110_cell${cellId}.csv -f popData_internet_1104_1110_cell${cellId}.csv  -iXi xiData_internet_1104_1110.csv -o info_internet_Original_1104_1110_cell${cellId}.csv  --mixRate1 1.0 --uTraffic1 1.0 --uCPU1ave 0.25 --uMEM1ave 0.80 --uCPU1std 0.1 --uMEM1std 0.3
done

# ベイズ推定　入力：単一クラスモデル
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Original_1104_1110_cell${cellId}.csv -o result_SglOrg_1104_1110_cell${cellId}.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
    python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_SglOrg_1104_1110_cell${cellId}.csv --inputFile info_internet_Original_1104_1110_cell${cellId}.csv --pjName SglOrg_1104_1110_cell${cellId}
done
python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Original_1104_1110_cell -pR result_SglOrg_1104_1110_cell --cellIdList 04259 04456 05060 05200

# # 入力トラフィックモデルの生成
# # 入力トラフィックは人口データから生成したものを使う
for cellId in {04259,04456,05060,05200}
do
    python3 calcMGInputDataV2.py --duration 600 -c 1 -ci cell${cellId} -od output -i trafficData_internet_1104_1110_cell${cellId}.csv -f popData_internet_1104_1110_cell${cellId}.csv -iXi xiData_internet_1104_1110.csv -o info_internet_Single_1104_1110_cell${cellId}.csv --mixRate1 1.0 --uTraffic1 1.0  --uCPU1ave 0.25 --uMEM1ave 0.80 --uCPU1std 0.1 --uMEM1std 0.3 > /dev/null
done

# # ベイズ推定　単一クラスモデル
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Single_1104_1110_cell${cellId}.csv -o result_SglSgl_1104_1110_cell${cellId}.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
    python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_SglSgl_1104_1110_cell${cellId}.csv --inputFile info_internet_Single_1104_1110_cell${cellId}.csv --pjName SglSgl_1104_1110_cell${cellId}
done
python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Single_1104_1110_cell -pR result_SglSgl_1104_1110_cell --cellIdList 04259 04456 05060 05200

# 1111-1117 ----------------------------------------------------------------------------------------------------------------------------------------------------
# 単一クラス
# 入力トラフィックモデルの生成
# 入力トラフィックはMilano Gridのオリジナルデータを使用 
for cellId in {04259,04456,05060,05200}
do
    python3 calcMGInputDataV2.py --duration 600 --isOriginalTraffic -ci cell${cellId} -od output -i trafficData_internet_1111_1117_cell${cellId}.csv -f popData_internet_1111_1117_cell${cellId}.csv  -iXi xiData_internet_1111_1117.csv -o info_internet_Original_1111_1117_cell${cellId}.csv  --mixRate1 1.0 --uTraffic1 1.0 --uCPU1ave 0.25 --uMEM1ave 0.80 --uCPU1std 0.1 --uMEM1std 0.3
done

# ベイズ推定　入力：単一クラスモデル
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Original_1111_1117_cell${cellId}.csv -o result_SglOrg_1111_1117_cell${cellId}.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
    python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_SglOrg_1111_1117_cell${cellId}.csv --inputFile info_internet_Original_1111_1117_cell${cellId}.csv --pjName SglOrg_1111_1117_cell${cellId}
done
python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1111_1117 -pT trafficData_internet_1111_1117_cell -pP popData_internet_1111_1117_cell -pI info_internet_Original_1111_1117_cell -pR result_SglOrg_1111_1117_cell --cellIdList 04259 04456 05060 05200

# 入力トラフィックモデルの生成
# 入力トラフィックは人口データから生成したものを使う
for cellId in {04259,04456,05060,05200}
do
    python3 calcMGInputDataV2.py --duration 600 -c 1 -ci cell${cellId} -od output -i trafficData_internet_1111_1117_cell${cellId}.csv -f popData_internet_1111_1117_cell${cellId}.csv -iXi xiData_internet_1111_1117.csv -o info_internet_Single_1111_1117_cell${cellId}.csv --mixRate1 1.0 --uTraffic1 1.0 --uCPU1ave 0.25 --uMEM1ave 0.80 --uCPU1std 0.1 --uMEM1std 0.3 > /dev/null
done

# ベイズ推定　単一クラスモデル
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Single_1111_1117_cell${cellId}.csv -o result_SglSgl_1111_1117_cell${cellId}.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
    python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_SglSgl_1111_1117_cell${cellId}.csv --inputFile info_internet_Single_1111_1117_cell${cellId}.csv --pjName SingleSingle1_internet_1111_1117_cell${cellId}
done
python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1111_1117 -pT trafficData_internet_1111_1117_cell -pP popData_internet_1111_1117_cell -pI info_internet_Single_1111_1117_cell -pR result_SglSgl_1111_1117_cell --cellIdList 04259 04456 05060 05200

#############################################
# Step2Mult.sh
#!/bin/bash

# # エリア例は以下の通り
# Bocconi, one of the most famous Universities in Milan(Square id: 4259);
# Navigli district, one of the most famous nightlifeplaces in Milan (Square id: 4456);
# Duomo, the city centre of Milan (Square id: 5060);
# Duomo, the city centre of Trento (Square id: 5200);
# Mesiano, the department of Engineering of the Uni-versity of Trento (Square id: 5085);
# Bosco della città, a forest near Trento (Square id:4703)


# expand the limit of number of open files from 1024 to 4096 to allow the stan to open a large number of files 
ulimit -n 4096

# 1104-1110 ----------------------------------------------------------------------------------------------------------------------------------------------------
# 複数クラス
# 入力トラフィックモデルの生成
# 入力トラフィックは人口データから生成したものを使う
# for cellId in {04259,04456,04703,05060,05085,05200}
for cellId in {04259,04456,05060,05200}
do
    python3 calcMGInputDataV2.py --duration 600  -ci cell${cellId} -od output -i trafficData_internet_1104_1110_cell${cellId}.csv -f popData_internet_1104_1110_cell${cellId}.csv -iXi xiData_internet_1104_1110.csv -o info_internet_Multi8020_1104_1110_cell${cellId}.csv --mixRate1 0.8 --mixRate2 0.2 --uTraffic1 1.0 --uTraffic2 4.0 --uCPU1ave 0.25 --uCPU2ave 0.25 --uMEM1ave 0.80 --uMEM2ave 0.80 --uCPU1std 0.1 --uCPU2std 0.1 --uMEM1std 0.3 --uMEM2std 0.3 
done

# ベイズ推定　入力：複数クラスモデル
# 複数クラス入力で複数クラスとして予測するプログラムと結果のグラフ化 
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelMultiV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1104_1110_cell${cellId}.csv -o result_MltMlt_1104_1110_cell${cellId}.csv --uTraffic1 1.0 --uTraffic2 4.0 --uCPU1ave 0.25 --uCPU2ave 0.25 --uMEM1ave 0.80 --uMEM2ave 0.80 --uCPU1std 0.1 --uCPU2std 0.1 --uMEM1std 0.3 --uMEM2std 0.3  > /dev/null
    python3 drawGrphPredictResultMulti.py -od output -pd pic --resultFile result_MltMlt_1104_1110_cell${cellId}.csv --inputFile info_internet_Multi8020_1104_1110_cell${cellId}.csv --pjName MltMlt_1104_1110_cell${cellId}
done
python3 plotInputAndResults.py --didMultiPrediction -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -rXi1 0.8 -rXi2 0.2 -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Multi8020_1104_1110_cell -pR result_MltMlt_1104_1110_cell --cellIdList 04259 04456 05060 05200

# ベイズ推定　入力：複数クラスモデル
# 複数クラス入力で単一クラス（クラス1）として予測するプログラムと結果のグラフ化
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1104_1110_cell${cellId}.csv -o result_MltSgl1_1104_1110_cell${cellId}.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
    python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_MltSgl1_1104_1110_cell${cellId}.csv --inputFile info_internet_Multi8020_1104_1110_cell${cellId}.csv --pjName Multi8020Single1_internet_1104_1110_cell${cellId}
done
python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Multi8020_1104_1110_cell -pR result_MltSgl1_1104_1110_cell --cellIdList 04259 04456 05060 05200

# ベイズ推定　入力：複数クラスモデル
# 複数クラス入力で単一クラス（クラス2）として予測するプログラムと結果のグラフ化
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1104_1110_cell${cellId}.csv -o result_MltSgl2_1104_1110_cell${cellId}.csv --uTraffic 4.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
    python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_MltSgl2_1104_1110_cell${cellId}.csv --inputFile info_internet_Multi8020_1104_1110_cell${cellId}.csv --pjName Multi8020Single2_internet_1104_1110_cell${cellId}
done
# 1104-1110 ----------------------------------------------------------------------------------------------------------------------------------------------------
python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Multi8020_1104_1110_cell -pR result_MltSgl2_1104_1110_cell --cellIdList 04259 04456 05060 05200


# マルチクラスをクラス１とクラス２で推定した結果との比較のグラフを一枚に作成
python3 plotInputAndResults.py   --cellIdList 04259 04456 05060 05200 -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Multi8020_1104_1110_cell --switchMultiSingle -pR1 result_MltSgl1_1104_1110_cell -pR2 result_MltSgl2_1104_1110_cell



# 1111-1117 ----------------------------------------------------------------------------------------------------------------------------------------------------
# 複数クラス
# 入力トラフィックモデルの生成
# 入力トラフィックは人口データから生成したものを使う
# for cellId in {04259,04456,04703,05060,05085,05200}
for cellId in {04259,04456,05060,05200}
do
    python3 calcMGInputDataV2.py --duration 600  -ci cell${cellId} -od output -i trafficData_internet_1111_1117_cell${cellId}.csv -f popData_internet_1111_1117_cell${cellId}.csv -iXi xiData_internet_1111_1117.csv -o info_internet_Multi8020_1111_1117_cell${cellId}.csv --mixRate1 0.8 --mixRate2 0.2 --uTraffic1 1.0 --uTraffic2 4.0 --uCPU1ave 0.25 --uCPU2ave 0.25 --uMEM1ave 0.80 --uMEM2ave 0.80 --uCPU1std 0.1 --uCPU2std 0.1 --uMEM1std 0.3 --uMEM2std 0.3 
done

# ベイズ推定　入力：複数クラスモデル
# 複数クラス入力で複数クラスとして予測するプログラムと結果のグラフ化 
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelMultiV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1111_1117_cell${cellId}.csv -o result_MltMlt_1111_1117_cell${cellId}.csv --uTraffic1 1.0 --uTraffic2 4.0 --uCPU1ave 0.25 --uCPU2ave 0.25 --uMEM1ave 0.80 --uMEM2ave 0.80 --uCPU1std 0.1 --uCPU2std 0.1 --uMEM1std 0.3 --uMEM2std 0.3  > /dev/null
    python3 drawGrphPredictResultMulti.py -od output -pd pic --resultFile result_MltMlt_1111_1117_cell${cellId}.csv --inputFile info_internet_Multi8020_1111_1117_cell${cellId}.csv --pjName MltMlt_1111_1117_cell${cellId}
done
python3 plotInputAndResults.py --didMultiPrediction -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -rXi1 0.8 -rXi2 0.2 -Xi xiData_internet_1111_1117 -pT trafficData_internet_1111_1117_cell -pP popData_internet_1111_1117_cell -pI info_internet_Multi8020_1111_1117_cell -pR result_MltMlt_1111_1117_cell --cellIdList 04259 04456 05060 05200

# ベイズ推定　入力：複数クラスモデル
# 複数クラス入力で単一クラス（クラス1）として予測するプログラムと結果のグラフ化
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1111_1117_cell${cellId}.csv -o result_MltSgl1_1111_1117_cell${cellId}.csv --uTraffic 1.0  --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
    python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_MltSgl1_1111_1117_cell${cellId}.csv --inputFile info_internet_Multi8020_1111_1117_cell${cellId}.csv --pjName Multi8020Single1_internet_1111_1117_cell${cellId}
done
python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1111_1117 -pT trafficData_internet_1111_1117_cell -pP popData_internet_1111_1117_cell -pI info_internet_Multi8020_1111_1117_cell -pR result_MltSgl1_1111_1117_cell --cellIdList 04259 04456 05060 05200

# ベイズ推定　入力：複数クラスモデル
# 複数クラス入力で単一クラス（クラス2）として予測するプログラムと結果のグラフ化
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1111_1117_cell${cellId}.csv -o result_MltSgl2_1111_1117_cell${cellId}.csv --uTraffic 4.0  --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
    python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_MltSgl2_1111_1117_cell${cellId}.csv --inputFile info_internet_Multi8020_1111_1117_cell${cellId}.csv --pjName Multi8020Single2_internet_1111_1117_cell${cellId}
done
python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1111_1117 -pT trafficData_internet_1111_1117_cell -pP popData_internet_1111_1117_cell -pI info_internet_Multi8020_1111_1117_cell -pR result_MltSgl2_1111_1117_cell --cellIdList 04259 04456 05060 05200

# マルチクラスをクラス１とクラス２で推定した結果との比較のグラフを一枚に作成
python3 plotInputAndResults.py   --cellIdList 04259 04456 05060 05200 -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1111_1117 -pT trafficData_internet_1111_1117_cell -pP popData_internet_1111_1117_cell -pI info_internet_Multi8020_1111_1117_cell --switchMultiSingle -pR1 result_MltSgl1_1111_1117_cell -pR2 result_MltSgl2_1111_1117_cell


############################################
# Step2Mult_1104_1117.sh

#!/bin/bash

# # エリア例は以下の通り
# Bocconi, one of the most famous Universities in Milan(Square id: 4259);
# Navigli district, one of the most famous nightlifeplaces in Milan (Square id: 4456);
# Duomo, the city centre of Milan (Square id: 5060);
# Duomo, the city centre of Trento (Square id: 5200);
# Mesiano, the department of Engineering of the Uni-versity of Trento (Square id: 5085);
# Bosco della città, a forest near Trento (Square id:4703)


# expand the limit of number of open files from 1024 to 4096 to allow the stan to open a large number of files 
ulimit -n 4096

# # 1104-1110 ----------------------------------------------------------------------------------------------------------------------------------------------------
# # 複数クラス
# # 入力トラフィックモデルの生成
# # 入力トラフィックは人口データから生成したものを使う
# # for cellId in {04259,04456,04703,05060,05085,05200}
# for cellId in {04259,04456,05060,05200}
# do
#     python3 calcMGInputDataV2.py --duration 600  -ci cell${cellId} -od output -i trafficData_internet_1104_1110_cell${cellId}.csv -f popData_internet_1104_1110_cell${cellId}.csv -iXi xiData_internet_1104_1110.csv -o info_internet_Multi8020_1104_1110_cell${cellId}.csv --mixRate1 0.8 --mixRate2 0.2 --uTraffic1 1.0 --uTraffic2 4.0 --uCPU1ave 0.25 --uCPU2ave 0.25 --uMEM1ave 0.80 --uMEM2ave 0.80 --uCPU1std 0.1 --uCPU2std 0.1 --uMEM1std 0.3 --uMEM2std 0.3 
# done

# # ベイズ推定　入力：複数クラスモデル
# # 複数クラス入力で複数クラスとして予測するプログラムと結果のグラフ化 
# for cellId in {04259,04456,05060,05200}
# do
#     python3 predictBayesModelMultiV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1104_1110_cell${cellId}.csv -o result_MltMlt_1104_1110_cell${cellId}.csv --uTraffic1 1.0 --uTraffic2 4.0 --uCPU1ave 0.25 --uCPU2ave 0.25 --uMEM1ave 0.80 --uMEM2ave 0.80 --uCPU1std 0.1 --uCPU2std 0.1 --uMEM1std 0.3 --uMEM2std 0.3  > /dev/null
#     python3 drawGrphPredictResultMulti.py -od output -pd pic --resultFile result_MltMlt_1104_1110_cell${cellId}.csv --inputFile info_internet_Multi8020_1104_1110_cell${cellId}.csv --pjName MltMlt_1104_1110_cell${cellId}
# done
# python3 plotInputAndResults.py --didMultiPrediction -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -rXi1 0.8 -rXi2 0.2 -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Multi8020_1104_1110_cell -pR result_MltMlt_1104_1110_cell --cellIdList 04259 04456 05060 05200

# # ベイズ推定　入力：複数クラスモデル
# # 複数クラス入力で単一クラス（クラス1）として予測するプログラムと結果のグラフ化
# for cellId in {04259,04456,05060,05200}
# do
#     python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1104_1110_cell${cellId}.csv -o result_MltSgl1_1104_1110_cell${cellId}.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
#     python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_MltSgl1_1104_1110_cell${cellId}.csv --inputFile info_internet_Multi8020_1104_1110_cell${cellId}.csv --pjName Multi8020Single1_internet_1104_1110_cell${cellId}
# done
# python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Multi8020_1104_1110_cell -pR result_MltSgl1_1104_1110_cell --cellIdList 04259 04456 05060 05200

# # ベイズ推定　入力：複数クラスモデル
# # 複数クラス入力で単一クラス（クラス2）として予測するプログラムと結果のグラフ化
# for cellId in {04259,04456,05060,05200}
# do
#     python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1104_1110_cell${cellId}.csv -o result_MltSgl2_1104_1110_cell${cellId}.csv --uTraffic 4.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
#     python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_MltSgl2_1104_1110_cell${cellId}.csv --inputFile info_internet_Multi8020_1104_1110_cell${cellId}.csv --pjName Multi8020Single2_internet_1104_1110_cell${cellId}
# done
# # 1104-1110 ----------------------------------------------------------------------------------------------------------------------------------------------------
# python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Multi8020_1104_1110_cell -pR result_MltSgl2_1104_1110_cell --cellIdList 04259 04456 05060 05200

# 1111-1117 ----------------------------------------------------------------------------------------------------------------------------------------------------
# 複数クラス
# 入力トラフィックモデルの生成
# 入力トラフィックは人口データから生成したものを使う
# for cellId in {04259,04456,04703,05060,05085,05200}
for cellId in {04259,04456,05060,05200}
do
    python3 calcMGInputDataV2.py --duration 600  -ci cell${cellId} -od output -i trafficData_internet_1104_1117_cell${cellId}.csv -f popData_internet_1104_1117_cell${cellId}.csv -iXi xiData_internet_1104_1117.csv -o info_internet_Multi8020_1104_1117_cell${cellId}.csv --mixRate1 0.8 --mixRate2 0.2 --uTraffic1 1.0 --uTraffic2 4.0 --uCPU1ave 0.25 --uCPU2ave 0.25 --uMEM1ave 0.80 --uMEM2ave 0.80 --uCPU1std 0.1 --uCPU2std 0.1 --uMEM1std 0.3 --uMEM2std 0.3 
done

# ベイズ推定　入力：複数クラスモデル
# 複数クラス入力で複数クラスとして予測するプログラムと結果のグラフ化 
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelMultiV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1104_1117_cell${cellId}.csv -o result_MltMlt_1104_1117_cell${cellId}.csv --uTraffic1 1.0 --uTraffic2 4.0 --uCPU1ave 0.25 --uCPU2ave 0.25 --uMEM1ave 0.80 --uMEM2ave 0.80 --uCPU1std 0.1 --uCPU2std 0.1 --uMEM1std 0.3 --uMEM2std 0.3  > /dev/null
    python3 drawGrphPredictResultMulti.py -od output -pd pic --resultFile result_MltMlt_1104_1117_cell${cellId}.csv --inputFile info_internet_Multi8020_1104_1117_cell${cellId}.csv --pjName MltMlt_1104_1117_cell${cellId}
done
python3 plotInputAndResults.py --didMultiPrediction -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -rXi1 0.8 -rXi2 0.2 -Xi xiData_internet_1104_1117 -pT trafficData_internet_1104_1117_cell -pP popData_internet_1104_1117_cell -pI info_internet_Multi8020_1104_1117_cell -pR result_MltMlt_1104_1117_cell --cellIdList 04259 04456 05060 05200

# ベイズ推定　入力：複数クラスモデル
# 複数クラス入力で単一クラス（クラス1）として予測するプログラムと結果のグラフ化
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1104_1117_cell${cellId}.csv -o result_MltSgl1_1104_1117_cell${cellId}.csv --uTraffic 1.0  --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
    python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_MltSgl1_1104_1117_cell${cellId}.csv --inputFile info_internet_Multi8020_1104_1117_cell${cellId}.csv --pjName Multi8020Single1_internet_1104_1117_cell${cellId}
done
python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1117 -pT trafficData_internet_1104_1117_cell -pP popData_internet_1104_1117_cell -pI info_internet_Multi8020_1104_1117_cell -pR result_MltSgl1_1104_1117_cell --cellIdList 04259 04456 05060 05200

# ベイズ推定　入力：複数クラスモデル
# 複数クラス入力で単一クラス（クラス2）として予測するプログラムと結果のグラフ化
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1104_1117_cell${cellId}.csv -o result_MltSgl2_1104_1117_cell${cellId}.csv --uTraffic 4.0  --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
    python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_MltSgl2_1104_1117_cell${cellId}.csv --inputFile info_internet_Multi8020_1104_1117_cell${cellId}.csv --pjName Multi8020Single2_internet_1104_1117_cell${cellId}
done
python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1117 -pT trafficData_internet_1104_1117_cell -pP popData_internet_1104_1117_cell -pI info_internet_Multi8020_1104_1117_cell -pR result_MltSgl2_1104_1117_cell --cellIdList 04259 04456 05060 05200

# マルチクラスをクラス１とクラス２で推定した結果との比較のグラフを一枚に作成
python3 plotInputAndResults.py   --cellIdList 04259 04456 05060 05200 -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1117 -pT trafficData_internet_1104_1117_cell -pP popData_internet_1104_1117_cell -pI info_internet_Multi8020_1104_1117_cell --switchMultiSingle -pR1 result_MltSgl1_1104_1117_cell -pR2 result_MltSgl2_1104_1117_cell

########################################
# Step2Single_1104_1117.sh

#!/bin/bash

# # エリア例は以下の通り
# Bocconi, one of the most famous Universities in Milan(Square id: 4259);
# Navigli district, one of the most famous nightlifeplaces in Milan (Square id: 4456);
# Duomo, the city centre of Milan (Square id: 5060);
# Duomo, the city centre of Trento (Square id: 5200);
# Mesiano, the department of Engineering of the Uni-versity of Trento (Square id: 5085);
# Bosco della città, a forest near Trento (Square id:4703)


# expand the limit of number of open files from 1024 to 4096 to allow the stan to open a large number of files 
ulimit -n 4096

# # 1104-1110 ----------------------------------------------------------------------------------------------------------------------------------------------------
# # 単一クラス
# # 入力トラフィックモデルの生成
# # 入力トラフィックはMilano Gridのオリジナルデータを使用 
# # for cellId in {04259,04456,04703,05060,05085,05200}
# for cellId in {04259,04456,05060,05200}
# do
#     python3 calcMGInputDataV2.py --duration 600 --isOriginalTraffic -ci cell${cellId} -od output -i trafficData_internet_1104_1110_cell${cellId}.csv -f popData_internet_1104_1110_cell${cellId}.csv  -iXi xiData_internet_1104_1110.csv -o info_internet_Original_1104_1110_cell${cellId}.csv  --mixRate1 1.0 --uTraffic1 1.0 --uCPU1ave 0.25 --uMEM1ave 0.80 --uCPU1std 0.1 --uMEM1std 0.3
# done

# # ベイズ推定　入力：単一クラスモデル
# for cellId in {04259,04456,05060,05200}
# do
#     python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Original_1104_1110_cell${cellId}.csv -o result_SglOrg_1104_1110_cell${cellId}.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
#     python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_SglOrg_1104_1110_cell${cellId}.csv --inputFile info_internet_Original_1104_1110_cell${cellId}.csv --pjName SglOrg_1104_1110_cell${cellId}
# done
# python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Original_1104_1110_cell -pR result_SglOrg_1104_1110_cell --cellIdList 04259 04456 05060 05200

# # # 入力トラフィックモデルの生成
# # # 入力トラフィックは人口データから生成したものを使う
# for cellId in {04259,04456,05060,05200}
# do
#     python3 calcMGInputDataV2.py --duration 600 -c 1 -ci cell${cellId} -od output -i trafficData_internet_1104_1110_cell${cellId}.csv -f popData_internet_1104_1110_cell${cellId}.csv -iXi xiData_internet_1104_1110.csv -o info_internet_Single_1104_1110_cell${cellId}.csv --mixRate1 1.0 --uTraffic1 1.0  --uCPU1ave 0.25 --uMEM1ave 0.80 --uCPU1std 0.1 --uMEM1std 0.3 > /dev/null
# done

# # # ベイズ推定　単一クラスモデル
# for cellId in {04259,04456,05060,05200}
# do
#     python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Single_1104_1110_cell${cellId}.csv -o result_SglSgl_1104_1110_cell${cellId}.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
#     python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_SglSgl_1104_1110_cell${cellId}.csv --inputFile info_internet_Single_1104_1110_cell${cellId}.csv --pjName SglSgl_1104_1110_cell${cellId}
# done
# python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Single_1104_1110_cell -pR result_SglSgl_1104_1110_cell --cellIdList 04259 04456 05060 05200

# 1111-1117 ----------------------------------------------------------------------------------------------------------------------------------------------------
# 単一クラス
# 入力トラフィックモデルの生成
# 入力トラフィックはMilano Gridのオリジナルデータを使用 
for cellId in {04259,04456,05060,05200}
do
    python3 calcMGInputDataV2.py --duration 600 --isOriginalTraffic -ci cell${cellId} -od output -i trafficData_internet_1104_1117_cell${cellId}.csv -f popData_internet_1104_1117_cell${cellId}.csv  -iXi xiData_internet_1104_1117.csv -o info_internet_Original_1104_1117_cell${cellId}.csv  --mixRate1 1.0 --uTraffic1 1.0 --uCPU1ave 0.25 --uMEM1ave 0.80 --uCPU1std 0.1 --uMEM1std 0.3
done

# ベイズ推定　入力：単一クラスモデル
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Original_1104_1117_cell${cellId}.csv -o result_SglOrg_1104_1117_cell${cellId}.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
    python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_SglOrg_1104_1117_cell${cellId}.csv --inputFile info_internet_Original_1104_1117_cell${cellId}.csv --pjName SglOrg_1104_1117_cell${cellId}
done
python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1117 -pT trafficData_internet_1104_1117_cell -pP popData_internet_1104_1117_cell -pI info_internet_Original_1104_1117_cell -pR result_SglOrg_1104_1117_cell --cellIdList 04259 04456 05060 05200

# 入力トラフィックモデルの生成
# 入力トラフィックは人口データから生成したものを使う
for cellId in {04259,04456,05060,05200}
do
    python3 calcMGInputDataV2.py --duration 600 -c 1 -ci cell${cellId} -od output -i trafficData_internet_1104_1117_cell${cellId}.csv -f popData_internet_1104_1117_cell${cellId}.csv -iXi xiData_internet_1104_1117.csv -o info_internet_Single_1104_1117_cell${cellId}.csv --mixRate1 1.0 --uTraffic1 1.0 --uCPU1ave 0.25 --uMEM1ave 0.80 --uCPU1std 0.1 --uMEM1std 0.3 > /dev/null
done

# ベイズ推定　単一クラスモデル
for cellId in {04259,04456,05060,05200}
do
    python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Single_1104_1117_cell${cellId}.csv -o result_SglSgl_1104_1117_cell${cellId}.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
    python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_SglSgl_1104_1117_cell${cellId}.csv --inputFile info_internet_Single_1104_1117_cell${cellId}.csv --pjName SglSgl1_1104_1117_cell${cellId}
done
python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1117 -pT trafficData_internet_1104_1117_cell -pP popData_internet_1104_1117_cell -pI info_internet_Single_1104_1117_cell -pR result_SglSgl_1104_1117_cell --cellIdList 04259 04456 05060 05200


#################################
# SARIMA.sh

#!/bin/bash

# # エリア例は以下の通り
# Bocconi, one of the most famous Universities in Milan(Square id: 4259);
# Navigli district, one of the most famous nightlifeplaces in Milan (Square id: 4456);
# Duomo, the city centre of Milan (Square id: 5060);
# Duomo, the city centre of Trento (Square id: 5200);
# Mesiano, the department of Engineering of the Uni-versity of Trento (Square id: 5085);
# Bosco della città, a forest near Trento (Square id:4703)


# Please un-comment if needed
# ----------------------------------------------------------------------------------------------------------------------------------------------------
# prepare the traffic data from Milano Grid dataset
# KSHR_make_populationV2.py --> setMGTrfDb.py
python3 setMGTrfDb.py -s 2013-11-04 -e 2013-11-17 -t internet -od output -o trafficData_internet_1104_1117.csv
# compute the population data
# KS_apd_MilanoGridNeo.py --> setMGPopDbXiDb.py
python3 setMGPopDbXiDb.py -s 2013-11-04 -e 2013-11-17 --alpha 0.05 --xiBase 0.2 -od output -i trafficData_internet_1104_1117.csv -o popData_internet_1104_1117.csv -oXi xiData_internet_1104_1117.csv
# make the graph of time series data of traffic and population
# KS_graphTimeseriesTrafficMilano.py --> drawGrphMGTrfTS.py
python3 drawGrphMGTrfTS.py -s 2013-11-04 -e 2013-11-17 -od output -i trafficData_internet_1104_1117.csv -iPop popData_internet_1104_1117.csv -iXi xiData_internet_1104_1117.csv --pjName internet_1104_1117
# make the graph of heatmap of traffic and population
python drawGrphMGHeatmap.py  -s 2013-11-04 -e 2013-11-17 -od output -iPop popData_internet_1104_1117.csv --pjName internet_1104_1117
# ----------------------------------------------------------------------------------------------------------------------------------------------------

# expand the limit of number of open files from 1024 to 4096 to allow the stan to open a large number of files 
ulimit -n 4096

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# エリア別入力データの作成　トラフィックと人口
# for cellId in {04259,04456,04703,05060,05085,05200}
for cellId in {04259,04456,05060,05200}
do
    python3 getAreaData.py -s 2013-11-04 -e 2013-11-17 -ci cell${cellId} -od output -i trafficData_internet_1104_1117.csv -o trafficData_internet_1104_1117_cell${cellId}.csv 
    python3 getAreaData.py -s 2013-11-04 -e 2013-11-17 -ci cell${cellId} -od output -i popData_internet_1104_1117.csv -o popData_internet_1104_1117_cell${cellId}.csv 
done

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# 単一クラス
# 入力トラフィックモデルの生成
# 入力トラフィックはMilano Gridのオリジナルデータを使用 
for cellId in {04259,04456,05060,05200}
do
    python3 calcMGInputDataV2.py --duration 600 --isOriginalTraffic -ci cell${cellId} -od output -i trafficData_internet_1104_1117_cell${cellId}.csv -f popData_internet_1104_1117_cell${cellId}.csv  -iXi xiData_internet_1104_1117.csv -o info_internet_Original_1104_1117_cell${cellId}.csv --mixRate1 1.0 --uTraffic1 1.0 --uCPU1ave 0.25 --uMEM1ave 0.80 --uCPU1std 0.1 --uMEM1std 0.3
done

# SARIMA推定　入力：単一クラスモデル 1 day 周期 1/6サンプル
for cellId in {04259,04456,05060,05200}
do
    python3 predictSARIMA.py --lengthCycle 1 --sampleRate 6 -s_train 2013-11-04 -e_train 2013-11-10 -s_test 2013-11-11 -e_test 2013-11-17 -od output -f info_internet_Original_1104_1117_cell${cellId}.csv -o resultSARIMA_D1S6_SglOrg_1104_1117_cell${cellId}.csv 
    python3 drawGrphPredictSARIMAResult.py -od output --resultFile resultSARIMA_D1S6_SglOrg_1104_1117_cell${cellId}.csv --inFileName info_internet_Original_1104_1117_cell${cellId}.csv --pjName SARIMA_D1S6_SglOrg_1104_1117_cell${cellId}
done
python3 plotInputAndResultsSARIMA.py  -s 2013-11-04 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -xi xiData_internet_1104_1117 -pI info_internet_Original_1104_1117_cell -pR resultSARIMA_D1S6_SglOrg_1104_1117_cell --cellIdList 04259 04456 05060 05200

# SARIMA推定　入力：単一クラスモデル 7 day 周期 1/12サンプル
for cellId in {04259,04456,05060,05200}
do
    python3 predictSARIMA.py --lengthCycle 7 --sampleRate 12 -s_train 2013-11-04 -e_train 2013-11-10 -s_test 2013-11-11 -e_test 2013-11-17 -od output -f info_internet_Original_1104_1117_cell${cellId}.csv -o resultSARIMA_D7S12_SglOrg_1104_1117_cell${cellId}.csv 
    python3 drawGrphPredictSARIMAResult.py -od output --resultFile resultSARIMA_D7S12_SglOrg_1104_1117_cell${cellId}.csv --inFileName info_internet_Original_1104_1117_cell${cellId}.csv --pjName SARIMA_D7S12_SglOrg_1104_1117_cell${cellId}
done
python3 plotInputAndResultsSARIMA.py  -s 2013-11-04 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -xi xiData_internet_1104_1117 -pI info_internet_Original_1104_1117_cell -pR resultSARIMA_D7S12_SglOrg_1104_1117_cell --cellIdList 04259 04456 05060 05200


# SARIMA推定　入力：単一クラスモデル 1 day 周期 1/2サンプル
for cellId in {04259,04456,05060,05200}
do
    python3 predictSARIMA.py --lengthCycle 1 --sampleRate 2 -s_train 2013-11-04 -e_train 2013-11-10 -s_test 2013-11-11 -e_test 2013-11-17 -od output -f info_internet_Original_1104_1117_cell${cellId}.csv -o resultSARIMA_D1S2_SglOrg_1104_1117_cell${cellId}.csv 
    python3 drawGrphPredictSARIMAResult.py -od output --resultFile resultSARIMA_D1S2_SglOrg_1104_1117_cell${cellId}.csv --inFileName info_internet_Original_1104_1117_cell${cellId}.csv --pjName SARIMA_D1S2_SglOrg_1104_1117_cell${cellId}
done
python3 plotInputAndResultsSARIMA.py  -s 2013-11-04 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -xi xiData_internet_1104_1117 -pI info_internet_Original_1104_1117_cell -pR resultSARIMA_D1S2_SglOrg_1104_1117_cell --cellIdList 04259 04456 05060 05200

# SARIMA推定　入力：単一クラスモデル 7 day 周期 1/6サンプル
for cellId in {04259,04456,05060,05200}
do
    python3 predictSARIMA.py --lengthCycle 7 --sampleRate 6 -s_train 2013-11-04 -e_train 2013-11-10 -s_test 2013-11-11 -e_test 2013-11-17 -od output -f info_internet_Original_1104_1117_cell${cellId}.csv -o resultSARIMA_D7S6_SglOrg_1104_1117_cell${cellId}.csv 
    python3 drawGrphPredictSARIMAResult.py -od output --resultFile resultSARIMA_D7S6_SglOrg_1104_1117_cell${cellId}.csv --inFileName info_internet_Original_1104_1117_cell${cellId}.csv --pjName SARIMA_D7S6_SglOrg_1104_1117_cell${cellId}
done
python3 plotInputAndResultsSARIMA.py  -s 2013-11-04 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -xi xiData_internet_1104_1117 -pI info_internet_Original_1104_1117_cell -pR resultSARIMA_D7S6_SglOrg_1104_1117_cell --cellIdList 04259 04456 05060 05200



# SARIMA推定　入力：単一クラスモデル 1 day 周期 フルサンプル
for cellId in {04259,04456,05060,05200}
do
    python3 predictSARIMA.py --lengthCycle 1 --sampleRate 1 -s_train 2013-11-04 -e_train 2013-11-10 -s_test 2013-11-11 -e_test 2013-11-17 -od output -f info_internet_Original_1104_1117_cell${cellId}.csv -o resultSARIMA_D1S1_SglOrg_1104_1117_cell${cellId}.csv 
    python3 drawGrphPredictSARIMAResult.py -od output --resultFile resultSARIMA_D1S1_SglOrg_1104_1117_cell${cellId}.csv --inFileName info_internet_Original_1104_1117_cell${cellId}.csv --pjName SARIMA_D1S1_SglOrg_1104_1117_cell${cellId}
done
python3 plotInputAndResultsSARIMA.py  -s 2013-11-04 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -xi xiData_internet_1104_1117 -pI info_internet_Original_1104_1117_cell -pR resultSARIMA_D1S1_SglOrg_1104_1117_cell --cellIdList 04259 04456 05060 05200



# ----------------------------------------------------------------------------------------------------------------------------------------------------
# 単一クラス
# # 入力トラフィックモデルの生成
# # 入力トラフィックは人口データから生成したものを使う
for cellId in {04259,04456,05060,05200}
do
    python3 calcMGInputDataV2.py --duration 600 -c 1 -ci cell${cellId} -od output -i trafficData_internet_1104_1117_cell${cellId}.csv -f popData_internet_1104_1117_cell${cellId}.csv -iXi xiData_internet_1104_1117.csv -o info_internet_Single_1104_1117_cell${cellId}.csv --mixRate1 1.0 --uTraffic1 1.0  --uCPU1ave 0.25 --uMEM1ave 0.80 --uCPU1std 0.1 --uMEM1std 0.3
done

# SARIMA推定　入力：単一クラスモデル 1 day 周期 1/6サンプル
for cellId in {04259,04456,05060,05200}
do
    python3 predictSARIMA.py --lengthCycle 1 --sampleRate 6 -s_train 2013-11-04 -e_train 2013-11-10 -s_test 2013-11-11 -e_test 2013-11-17 -od output -f info_internet_Single_1104_1117_cell${cellId}.csv -o resultSARIMA_D1S6_SglSgl_1104_1117_cell${cellId}.csv 
    python3 drawGrphPredictSARIMAResult.py -od output --resultFile resultSARIMA_D1S6_SglSgl_1104_1117_cell${cellId}.csv --inFileName info_internet_Single_1104_1117_cell${cellId}.csv --pjName SARIMA_D1S6_SglSgl_1104_1117_cell${cellId}
done
python3 plotInputAndResultsSARIMA.py  -s 2013-11-04 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -xi xiData_internet_1104_1117 -pI info_internet_Single_1104_1117_cell -pR resultSARIMA_D1S6_SglSgl_1104_1117_cell --cellIdList 04259 04456 05060 05200

# SARIMA推定　入力：単一クラスモデル 7 day 周期 1/12サンプル
for cellId in {04259,04456,05060,05200}
do
    python3 predictSARIMA.py --lengthCycle 7 --sampleRate 12 -s_train 2013-11-04 -e_train 2013-11-10 -s_test 2013-11-11 -e_test 2013-11-17 -od output -f info_internet_Single_1104_1117_cell${cellId}.csv -o resultSARIMA_D7S12_SglSgl_1104_1117_cell${cellId}.csv 
    python3 drawGrphPredictSARIMAResult.py -od output --resultFile resultSARIMA_D7S12_SglSgl_1104_1117_cell${cellId}.csv --inFileName info_internet_Single_1104_1117_cell${cellId}.csv --pjName SARIMA_D7S12_SglSgl_1104_1117_cell${cellId}
done
python3 plotInputAndResultsSARIMA.py  -s 2013-11-04 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -xi xiData_internet_1104_1117 -pI info_internet_Single_1104_1117_cell -pR resultSARIMA_D7S12_SglSgl_1104_1117_cell --cellIdList 04259 04456 05060 05200

# SARIMA推定　入力：単一クラスモデル 1 day 周期 1/2サンプル
for cellId in {04259,04456,05060,05200}
do
    python3 predictSARIMA.py --lengthCycle 1 --sampleRate 2 -s_train 2013-11-04 -e_train 2013-11-10 -s_test 2013-11-11 -e_test 2013-11-17 -od output -f info_internet_Single_1104_1117_cell${cellId}.csv -o resultSARIMA_D1S2_SglSgl_1104_1117_cell${cellId}.csv 
    python3 drawGrphPredictSARIMAResult.py -od output --resultFile resultSARIMA_D1S2_SglSgl_1104_1117_cell${cellId}.csv --inFileName info_internet_Single_1104_1117_cell${cellId}.csv --pjName SARIMA_D1S2_SglSgl_1104_1117_cell${cellId}
done
python3 plotInputAndResultsSARIMA.py  -s 2013-11-04 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -xi xiData_internet_1104_1117 -pI info_internet_Single_1104_1117_cell -pR resultSARIMA_D1S2_SglSgl_1104_1117_cell --cellIdList 04259 04456 05060 05200

# SARIMA推定　入力：単一クラスモデル 7 day 周期 1/6サンプル
for cellId in {04259,04456,05060,05200}
do
    python3 predictSARIMA.py --lengthCycle 7 --sampleRate 6 -s_train 2013-11-04 -e_train 2013-11-10 -s_test 2013-11-11 -e_test 2013-11-17 -od output -f info_internet_Single_1104_1117_cell${cellId}.csv -o resultSARIMA_D7S6_SglSgl_1104_1117_cell${cellId}.csv 
    python3 drawGrphPredictSARIMAResult.py -od output --resultFile resultSARIMA_D7S6_SglSgl_1104_1117_cell${cellId}.csv --inFileName info_internet_Single_1104_1117_cell${cellId}.csv --pjName SARIMA_D7S6_SglSgl_1104_1117_cell${cellId}
done
python3 plotInputAndResultsSARIMA.py  -s 2013-11-04 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -xi xiData_internet_1104_1117 -pI info_internet_Single_1104_1117_cell -pR resultSARIMA_D7S6_SglSgl_1104_1117_cell --cellIdList 04259 04456 05060 05200


# SARIMA推定　入力：単一クラスモデル 1 day 周期 フルサンプル
for cellId in {04259,04456,05060,05200}
do
    python3 predictSARIMA.py --lengthCycle 1 --sampleRate 1 -s_train 2013-11-04 -e_train 2013-11-10 -s_test 2013-11-11 -e_test 2013-11-17 -od output -f info_internet_Single_1104_1117_cell${cellId}.csv -o resultSARIMA_D1S1_SglSgl_1104_1117_cell${cellId}.csv 
    python3 drawGrphPredictSARIMAResult.py -od output --resultFile resultSARIMA_D1S1_SglSgl_1104_1117_cell${cellId}.csv --inFileName info_internet_Single_1104_1117_cell${cellId}.csv --pjName SARIMA_D1S1_SglSgl_1104_1117_cell${cellId}
done
python3 plotInputAndResultsSARIMA.py  -s 2013-11-04 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -xi xiData_internet_1104_1117 -pI info_internet_Single_1104_1117_cell -pR resultSARIMA_D1S1_SglSgl_1104_1117_cell --cellIdList 04259 04456 05060 05200

############################################
# experimentSARIMA-Grhp.sh
# # BayiesianとSARIMA (1 day) とSARIMA (1 week) との比較のグラフを一枚に作成
# python3 plotInputAndResults.py   --cellIdList 04259 04456 05060 05200 -s 2013-11-11 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1117 -pT trafficData_internet_1104_1117_cell -pP popData_internet_1104_1117_cell -pI info_internet_Single_1104_1117_cell --switchSARIMA -pR1 result_SglSgl_1104_1117_cell -pR2 resultSARIMA_internet_SingleOriginal_1104_1117_cell -pR3 resultSARIMA_internet_SingleOriginal_1104_1117_cell --pjName D1S6_D7S12

# 1104-1117
# BayiesianとSARIMA (1 day) とSARIMA (1 week) との比較のグラフを一枚に作成
# Original
python3 plotInputAndResults.py   --cellIdList 04259 04456 05060 05200 -s 2013-11-04 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1117 -pT trafficData_internet_1104_1117_cell -pP popData_internet_1104_1117_cell -pI info_internet_Original_1104_1117_cell --switchSARIMA -pR1 result_SglOrg_1104_1117_cell -pR2 resultSARIMA_D1S2_SglSgl_1104_1117_cell -pR3 resultSARIMA_D7S6_SglSgl_1104_1117_cell --pjName D1S2D7S6_SglOrg_1104_1117
# BayiesianとSARIMA (1 day) とSARIMA (1 week) との比較のグラフを一枚に作成
# Single
python3 plotInputAndResults.py   --cellIdList 04259 04456 05060 05200 -s 2013-11-04 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1117 -pT trafficData_internet_1104_1117_cell -pP popData_internet_1104_1117_cell -pI info_internet_Single_1104_1117_cell --switchSARIMA -pR1 result_SglSgl_1104_1117_cell -pR2 resultSARIMA_D1S2_SglSgl_1104_1117_cell -pR3 resultSARIMA_D7S6_SglSgl_1104_1117_cell --pjName D1S2D7S6_SglSgl_1104_1117



# 1111-1117
# BayiesianとSARIMA (1 day) とSARIMA (1 week) との比較のグラフを一枚に作成
# Original
python3 plotInputAndResults.py   --cellIdList 04259 04456 05060 05200 -s 2013-11-11 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1117 -pT trafficData_internet_1104_1117_cell -pP popData_internet_1104_1117_cell -pI info_internet_Original_1104_1117_cell --switchSARIMA -pR1 result_SglOrg_1104_1117_cell -pR2 resultSARIMA_D1S2_SglSgl_1104_1117_cell -pR3 resultSARIMA_D7S6_SglSgl_1104_1117_cell --pjName D1S2_D7S6_SglOrg_1111_1117
# BayiesianとSARIMA (1 day) とSARIMA (1 week) との比較のグラフを一枚に作成
# Single
python3 plotInputAndResults.py   --cellIdList 04259 04456 05060 05200 -s 2013-11-11 -e 2013-11-17  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1117 -pT trafficData_internet_1104_1117_cell -pP popData_internet_1104_1117_cell -pI info_internet_Single_1104_1117_cell --switchSARIMA -pR1 result_SglSgl_1104_1117_cell -pR2 resultSARIMA_D1S2_SglSgl_1104_1117_cell -pR3 resultSARIMA_D7S6_SglSgl_1104_1117_cell --pjName D1S2D7S6_SglSgl_1111_1117

