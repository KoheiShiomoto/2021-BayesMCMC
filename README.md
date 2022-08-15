# 2021-BayesMCMC

This repository is for the paper titled
"A Network Traffic Prediction Method based on a Bayesian Network Model for Relationship between Traffic and Population"
co-authored by Kohei Shiomoto, Tatsuya Otoshi, and Masayuki Murata.

 We have proposed a method to predict network and computing resources
 using population estimates based on the past variable network and
 computing resource usage.
 We have proposed a Bayesian model to study the relationship between
 population in an area and network and computing resource requirement.
 The following assumptions were utilized:
 (1) User terminal traffic data can be profiled with reasonable
 accuracy.
 (2) User mobility and numbers in an area can be predicted with
 reasonable accuracy.
 The parameters governing the Bayesian network are estimated from the
 data.
 To predict traffic volume and computing resources for the next time
 epoch, the Bayesian model estimates a latent variable, which
 denotes the number of active user terminals utilizing computing
 resources and generating traffic. For this purpose, Observable variables,
 such as previous traffic volume, computing resource usage,
 and expected number of users (in the next time epoch) are utilized. 

 In our previous work presented in the NoF 2021, we presented preliminary
 evaluation results using Geant traffic data.
 In this model, the ratio of the number of communicating users in the
 overall population was considered fixed during the evaluation period. 
 In contrast, this paper assumes that the ratio of the number of
 communicating users dynamically changes and presents a detailed
 performance evaluation using the Toy model and the Milan Grid model. 
 First, we examined the basic performance of the proposed
 Bayesian network-based forecasting method using the Toy model, and
 confirmed that the proposed method provides highly accurate forecasts
 even in scenarios where the ratio of the number of communicating users
 changes dynamically during the evaluation period. 
 We also evaluated the performance of the proposed method in a practical
 scenario using the Milan Grid traffic dataset in spatio-temporal space,
 deriving changes in the population distribution in spatio-temporal
 space from the Milan Grid traffic data, and constructed and evaluated
 an evaluation model. 
 The results confirmed that the proposed method provides accurate
 prediction results for both single and multiple traffic classes.  

 ## Dataset creation from Milan Grid
 We create the traffic data from Milano Grid dataset.
 In order to prepare the traffic data from 2013-11-04 to 2013-11-10, you need to do the following:
 ```
 python3 setMGTrfDb.py -s 2013-11-04 -e 2013-11-10 -t internet -od output -o trafficData_internet_1104_1110.csv
 ```

 Then, in order to compute the population data, you need to do the following:
 ```
 python3 setMGPopDbXiDb.py -s 2013-11-04 -e 2013-11-10 --alpha 0.1 --xiBase 0.2 -od output -i trafficData_internet_1104_1110.csv -o popData_internet_1104_1110.csv -oXi xiData_internet_1104_1110.csv
 ```

 You may wan to make the graph of time series data of traffic and population by doing the following:
 ```
 python3 drawGrphMGTrfTS.py -s 2013-11-04 -e 2013-11-10 -od output -i trafficData_internet_1104_1110.csv -iPop popData_internet_1104_1110.csv -iXi xiData_internet_1104_1110.csv --pjName internet_1104_1110
 ```
 You may also want to make the graph of heatmap of traffic and population by doing the following:
 ```
 python drawGrphMGHeatmap.py  -s 2013-11-04 -e 2013-11-10 -od output -iPop popData_internet_1104_1110.csv --pjName internet_1104_1110
 ```
 Then, you need to create the traffic data of a area named `cellID`. `cellID` in the range of 00000 to 09999 designates the area(Bocconi is 04259).
 ```
 python3 getAreaData.py -s 2013-11-04 -e 2013-11-10 -ci cell${cellId} -od output -i trafficData_internet_1104_1110.csv -o trafficData_internet_1104_1110_cell${cellId}.csv
 ```

 Then you will creat the input data to run the simulater.
 You should choose to use either original, artificial (single class), artificial (two classes) traffic.

 ## For the original traffic simulation
 First, to use the original traffic, you need to prepate the input data to run the simulator by doing the following:
 ```
 python3 calcMGInputDataV2.py --duration 600 --isOriginalTraffic -ci cell${cellId} -od output -i trafficData_internet_1104_1110_cell${cellId}.csv -f popData_internet_1104_1110_cell${cellId}.csv  -iXi xiData_internet_1104_1110.csv -o info_internet_Original_1104_1110_cell${cellId}.csv  --mixRate1 1.0 --uTraffic1 1.0 --uCPU1ave 0.25 --uMEM1ave 0.80 --uCPU1std 0.1 --uMEM1std 0.3
 ```
 You will run the simulater.
 ```
 python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Original_1104_1110_cell${cellId}.csv -o result_SglOrg_1104_1110_cell${cellId}.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
 ```
 You can make the graph from the results.
 ```
 python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_SglOrg_1104_1110_cell${cellId}.csv --inputFile info_internet_Original_1104_1110_cell${cellId}.csv --pjName SglOrg_1104_1110_cell${cellId}
 ```
 You can also make the graphs from the multiple areas. For example, 04259, 04456, 05060, and 05200.
 ```
 python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Original_1104_1110_cell -pR result_SglOrg_1104_1110_cell --cellIdList 04259 04456 05060 05200
 ```




 ## For an artifical traffic (single class) simulation
 Second, to use an artificial traffic (single class), you need to prepate the input data to run the simulator by doing the following:
 ```
 python3 calcMGInputDataV2.py --duration 600 -c 1 -ci cell${cellId} -od output -i trafficData_internet_1111_1117_cell${cellId}.csv -f popData_internet_1111_1117_cell${cellId}.csv -iXi xiData_internet_1111_1117.csv -o info_internet_Single_1111_1117_cell${cellId}.csv --mixRate1 1.0 --uTraffic1 1.0 --uCPU1ave 0.25 --uMEM1ave 0.80 --uCPU1std 0.1 --uMEM1std 0.3 > /dev/null
 ```

 You will run the simulater.
 ```
 python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Single_1111_1117_cell${cellId}.csv -o result_SglSgl_1111_1117_cell${cellId}.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
 ```

 You can make the graph from the results.
 ```
 python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_SglSgl_1111_1117_cell${cellId}.csv --inputFile info_internet_Single_1111_1117_cell${cellId}.csv --pjName SingleSingle1_internet_1111_1117_cell${cellId}
 ```

 You can also make the graphs from the multiple areas. For example, 04259, 04456, 05060, and 05200.
 ```
 python3 plotInputAndResults.py -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1111_1117 -pT trafficData_internet_1111_1117_cell -pP popData_internet_1111_1117_cell -pI info_internet_Single_1111_1117_cell -pR result_SglSgl_1111_1117_cell --cellIdList 04259 04456 05060 05200
 ```




 ## For an artifical traffic (two classes) simulation
 Second, to use an artificial traffic (two class), you need to prepate the input data to run the simulator by doing the following:
 ```
 python3 calcMGInputDataV2.py --duration 600  -ci cell${cellId} -od output -i trafficData_internet_1104_1110_cell${cellId}.csv -f popData_internet_1104_1110_cell${cellId}.csv -iXi xiData_internet_1104_1110.csv -o info_internet_Multi8020_1104_1110_cell${cellId}.csv --mixRate1 0.8 --mixRate2 0.2 --uTraffic1 1.0 --uTraffic2 4.0 --uCPU1ave 0.25 --uCPU2ave 0.25 --uMEM1ave 0.80 --uMEM2ave 0.80 --uCPU1std 0.1 --uCPU2std 0.1 --uMEM1std 0.3 --uMEM2std 0.3 
 ```

 ### Two classes are assumed in Bayesian inference
 You will run the simulater.
 ```
 python3 predictBayesModelMultiV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1104_1110_cell${cellId}.csv -o result_MltMlt_1104_1110_cell${cellId}.csv --uTraffic1 1.0 --uTraffic2 4.0 --uCPU1ave 0.25 --uCPU2ave 0.25 --uMEM1ave 0.80 --uMEM2ave 0.80 --uCPU1std 0.1 --uCPU2std 0.1 --uMEM1std 0.3 --uMEM2std 0.3  > /dev/null
 ```

 You can make the graph from the results.
 ```
 python3 drawGrphPredictResultMulti.py -od output -pd pic --resultFile result_MltMlt_1104_1110_cell${cellId}.csv --inputFile info_internet_Multi8020_1104_1110_cell${cellId}.csv --pjName MltMlt_1104_1110_cell${cellId}
 ```

 You can also make the graphs from the multiple areas. For example, 04259, 04456, 05060, and 05200.
 ```
 python3 plotInputAndResults.py --didMultiPrediction -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -rXi1 0.8 -rXi2 0.2 -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Multi8020_1104_1110_cell -pR result_MltMlt_1104_1110_cell --cellIdList 04259 04456 05060 05200
 ```



 ### Single class (class #1) is assumed in Bayesian inference
 You will run the simulater.
 ```
 python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1104_1110_cell${cellId}.csv -o result_MltSgl1_1104_1110_cell${cellId}.csv --uTraffic 1.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
 ```

 You can make the graph from the results.
 ```
 python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_MltSgl1_1104_1110_cell${cellId}.csv --inputFile info_internet_Multi8020_1104_1110_cell${cellId}.csv --pjName Multi8020Single1_internet_1104_1110_cell${cellId}
 ```

 You can also make the graphs from the multiple areas. For example, 04259, 04456, 05060, and 05200.
 ```
 python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Multi8020_1104_1110_cell -pR result_MltSgl1_1104_1110_cell --cellIdList 04259 04456 05060 05200
 ```
 
 ### Single class (class #2) is assumed in Bayesian inference
 You will run the simulater.
 ```
 python3 predictBayesModelSingleV2.py --sampleNum 1 -od output -f info_internet_Multi8020_1104_1110_cell${cellId}.csv -o result_MltSgl2_1104_1110_cell${cellId}.csv --uTraffic 4.0 --uCPUave 0.25 --uMEMave 0.80 --uCPUstd 0.1 --uMEMstd 0.3 > /dev/null
 ```

 You can make the graph from the results.
 ```
 python3 drawGrphPredictResultSingle.py -od output -pd pic --resultFile result_MltSgl2_1104_1110_cell${cellId}.csv --inputFile info_internet_Multi8020_1104_1110_cell${cellId}.csv --pjName Multi8020Single2_internet_1104_1110_cell${cellId}
 ```

 You can also make the graphs from the multiple areas. For example, 04259, 04456, 05060, and 05200.
 ```
 python3 plotInputAndResults.py  -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Multi8020_1104_1110_cell -pR result_MltSgl2_1104_1110_cell --cellIdList 04259 04456 05060 05200
 ```

 ### Compare Single class (class #1) and Single class (class #2) is assumed in Bayesian inference
 You can also make the graphs from the multiple areas. For example, 04259, 04456, 05060, and 05200.
 ```
 python3 plotInputAndResults.py   --cellIdList 04259 04456 05060 05200 -s 2013-11-01 -e 2013-12-31  --ymaxTraffic 4000.0 --ymaxPopulation 10000 -od output -Xi xiData_internet_1104_1110 -pT trafficData_internet_1104_1110_cell -pP popData_internet_1104_1110_cell -pI info_internet_Multi8020_1104_1110_cell --switchMultiSingle -pR1 result_MltSgl1_1104_1110_cell -pR2 result_MltSgl2_1104_1110_cell
 ```

