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
