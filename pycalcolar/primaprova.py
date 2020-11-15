# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 22:01:35 2020

@author: teresa


"""

import pandas as pd

# importo file run.triplo36 (air_pipette)
colNamesInitData=['40F', 'err40F', '38IC0', 'err38IC0', '36IC1', 'err36IC1', '36IC0', 'err36IC0','36F', 'err 36F', 'gain IC0/IC1', 'err gain IC0/IC1', 'gain F/IC1', 'err gain F/IC1' , 'gain F/IC0', 'err gain F/IC0', '40F/36IC1', 'err 40F/36IC1 ', '40F/36F', 'err 40F/36F', '40F/36IC0', 'err 40F/36IC0' , '38IC0/36IC0', 'err 38IC0/36IC0', 'Run', 'Path']


# filePath = "../test_data/Triplo36esempio.txt"
filePath = "C:\\Users\\teres\\Documents\\PyCalcolAr\\test_data\\Triplo36esempio.txt"


airpipette_initData = pd.read_csv(filePath, header = None, names = colNamesInitData)

# creo un nuovo dataframe con le colonne utili
airpipette_utilData = airpipette_initData[['40F', 'err40F', '38IC0', 'err38IC0', '36IC1', 'err36IC1', '36IC0', 'err36IC0','36F', 'err 36F']]


#df.replace(to_replace ="Boston Celtics", 
                # value ="Omega Warrior") 

# airpipette_utilData.replace(to_replace = ["{", "}"], value = "", inplace=True)


# svolgo le operazioni utili che saranno presenti nel file excel (airpipette_Data)

# calcolo gain F/IC0
A = airpipette_utilData.loc[0,'36F']
B = airpipette_utilData.loc[0,'36IC0']

gain_F_IC0 = A/B
print ('gain F/IC0: ', gain_F_IC0)

# calcolo gain F/IC1 
A = airpipette_utilData.loc[0,'36F']
C = airpipette_utilData.loc[0,'36IC1']

gain_F_IC1 = A/C
print ('gain F/IC1: ', gain_F_IC1)

# calcolo 36IC0 correzione gain
A = airpipette_utilData.loc[0,'36IC0']
corr_gain_36IC0 = A * gain_F_IC0
print ('corr_gain_36IC0: ', corr_gain_36IC0) 

# calcolo 40/36 correzione
A = airpipette_utilData.loc[0,'40F']
B = 62415000 
corr_40_36 = (A * B) / corr_gain_36IC0
print ('corr_40_36: ', corr_40_36)

# calcolo source frax
A = 298.56
source_frax = corr_40_36 / A
print ('source_frax: ', source_frax)




# #lista con i nomi delle colonne
# colNamesInitData=['40F', 'err40F', '38IC0', 'err38IC0', '36IC1', 'err36IC1', '38F', 'err38F','36IC0', 'err 36', '39F', 'err39F', '37IC0', 'err37IC0' , '35IC1', 'err35IC1', '39IC0',  'err39IC0',  '37IC1', 'err37IC1', 'F/IC0', 'errF/IC0' , 'IC0/IC1', 'errIC0/IC1', '40F/36IC1',  'err40F/36IC1',  '40F/36IC0' ,'err40F/36IC0', 'Run', 'Path']

# filePath = "C:\\Users\\teres\\Desktop\\Tesi\\Run4esempio.txt"

# #importazione del file Run.txt in un data frame pandas
# initData = pd.read_csv(filePath, header = None, names = colNamesInitData)

# #eliminare ultima riga della tabella (dataframe) che contiene dati sbagliati 
# initData = initData.drop([5]) #da togliere nella versione finale (solo per il file Run4esempio.txt)

# gain_F_IC = float(1.2528)
# 36IC_corr = 339160
# 40_36_corr = float(297.34)
# source_frax= float(0.9959)


# sampleData_V = initData.loc[:, ["40F", "err40F", "38IC0", "err38IC0", "36IC1", "err36IC1", "39F", "err39F", "37IC0", "err37IC0"]]
# sampleData_V = sampleData_V.replace("{", "", regex=True)
# sampleData_V = sampleData_V.replace("}", "", regex=True)

# sampleData_mV ["40F"] = pd.to_numeric(sampleData_V ["40F"]) * 1000
# sampleData_mV ["err40F"] = pd.to_numeric(sampleData_V ["err40F"]) * 1000
# sampleData_mV ["38IC0"] = pd.to_numeric(sampleData_V ["38IC0"]) * 1000
# sampleData_mV ["err38IC0"] = pd.to_numeric(sampleData_V ["err38IC0"]) * 1000
# sampleData_mV ["36IC1"] = pd.to_numeric(sampleData_V ["36IC1"]) * 1000
# sampleData_mV ["err36IC1"] = pd.to_numeric(sampleData_V ["err36IC1"]) * 1000
# sampleData_mV ["39F"] = pd.to_numeric(sampleData_V ["39F"]) * 1000
# sampleData_mV ["err39F"] = pd.to_numeric(sampleData_V ["err39F"]) * 1000
# sampleData_mV ["37IC0"] = pd.to_numeric(sampleData_V ["37IC0"]) * 1000
# sampleData_mV ["err37IC0"] = pd.to_numeric(sampleData_V ["err37IC0"]) * 1000


# initData