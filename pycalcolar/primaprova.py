# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 22:01:35 2020

@author: teresa


"""

import pandas as pd

"""importo file run.triplo36 (air_pipette)"""
colNamesInitData = ['40F', 'err40F', '38IC0', 'err38IC0', '36IC1', 'err36IC1', '36IC0', 'err36IC0', '36F', 'err 36F', 'gain IC0/IC1', 'err gain IC0/IC1', 'gain F/IC1', 'err gain F/IC1', 'gain F/IC0', 'err gain F/IC0', '40F/36IC1', 'err 40F/36IC1 ', '40F/36F', 'err 40F/36F', '40F/36IC0', 'err 40F/36IC0', '38IC0/36IC0', 'err 38IC0/36IC0', 'Run', 'Path']

"""filePath"""
filePath = "../test_data/Triplo36esempio.txt"

"""creo nuovo dataframe con tutti i dati"""
airpipette_initData = pd.read_csv(filePath, header=None, names=colNamesInitData)

"""estraggo dataframe con le colonne utili"""
airpipette_utilData = airpipette_initData[['40F', 'err40F', '38IC0', 'err38IC0', '36IC1', 'err36IC1', '36IC0', 'err36IC0', '36F', 'err 36F']]
print(airpipette_utilData)

# df.replace(to_replace ="Boston Celtics",
# value ="Omega Warrior")

# airpipette_utilData.replace(to_replace = ["{", "}"], value = "", inplace=True)


"""svolgo le operazioni utili che saranno presenti nel file excel (airpipette_Data)"""

"""invece di stampare semplicemente con print, qui sotto puoi salvare i risultati in nuove colonne del dataframe ____________________________AB"""

"""qui sotto ho cambiato il riferimento alle colonne usando ":" e "values" in modo da poter usare lo stesso codice con file con più riche di dati ____________________________AB"""

# calcolo gain F/IC0
A = airpipette_utilData.loc[:, '36F'].values
B = airpipette_utilData.loc[:, '36IC0'].values

gain_F_IC0 = A / B
print('gain F/IC0: ', gain_F_IC0)

# calcolo gain F/IC1 
A = airpipette_utilData.loc[:, '36F'].values
C = airpipette_utilData.loc[:, '36IC1'].values

gain_F_IC1 = A / C
print('gain F/IC1: ', gain_F_IC1)

# calcolo 36IC0 correzione gain
A = airpipette_utilData.loc[:, '36IC0'].values
corr_gain_36IC0 = A * gain_F_IC0
print('corr_gain_36IC0: ', corr_gain_36IC0)

# calcolo 40/36 correzione
A = airpipette_utilData.loc[:, '40F'].values
B = 62415000
corr_40_36 = (A * B) / corr_gain_36IC0
print('corr_40_36: ', corr_40_36)

# calcolo source frax
A = 298.56
source_frax = corr_40_36 / A
print('source_frax: ', source_frax)


# Tabella sample_data


# importo file run.4 e creo la lista con i nomi delle colonne 
colNamesInitData=['40Ar F', 'err40Ar F', '38Ar IC0', 'err38Ar IC0', '36Ar IC1', 'err36Ar IC1','38Ar F', 'err38Ar F','36Ar IC0', 'err36Ar IC0 ', '39Ar F', 'err39Ar F', '37Ar IC0', 'err37Ar IC0' , '35Cl IC1', 'err35Cl IC1', '39Ar IC0',  'err39Ar IC0',  '37Ar IC1', 'err37Ar IC1', 'gainF/IC0', 'err gainF/IC0' , 'gainIC0/IC1', 'err gainIC0/IC1', '40F/36IC1',  'err40F/36IC1',  '40F/36IC0' ,'err40F/36IC0', 'Run', 'Path']

# filePath = "../test_data/Run4esempio.txt"
filePath = "C:\\Users\\teres\\Documents\\PyCalcolAr\\test_data\\Run4esempio.txt"

df_initData = pd.read_csv(filePath, header = None, names = colNamesInitData)

# creo un nuovo dataframe con le colonne utili
sampleData_utilData = df_initData[['40Ar F', 'err40Ar F', '38Ar IC0', 'err38Ar IC0', '36Ar IC1', 'err36Ar IC1', '39Ar F', 'err39Ar F','37Ar IC1', 'err37Ar IC1']]

#eliminare ultima riga del dataframe che contiene "dati sbagliati"
sampleData_V = sampleData_utilData.drop([5]) #da togliere nella versione finale (solo per il file Run4esempio.txt)

print (sampleData_V)

sampleData_V = sampleData_V.replace(["{", "}"], ["", ""], regex=True)

sampleData_mV = pd.DataFrame()
sampleData_mV ["40Ar F"] = pd.to_numeric(sampleData_V ["40Ar F"]) * 1000
sampleData_mV ["err40Ar F"] = pd.to_numeric(sampleData_V ["err40Ar F"]) * 1000
sampleData_mV ["38Ar IC0"] = pd.to_numeric(sampleData_V ["38Ar IC0"]) * 1000
sampleData_mV ["err38Ar IC0"] = pd.to_numeric(sampleData_V ["err38Ar IC0"]) * 1000
sampleData_mV ["36Ar IC1"] = pd.to_numeric(sampleData_V ["36Ar IC1"]) * 1000
sampleData_mV ["err36Ar IC1"] = pd.to_numeric(sampleData_V ["err36Ar IC1"]) * 1000
sampleData_mV ["39Ar F"] = pd.to_numeric(sampleData_V ["39Ar F"]) * 1000
sampleData_mV ["err39Ar F"] = pd.to_numeric(sampleData_V ["err39Ar F"]) * 1000
sampleData_mV ["37Ar IC1"] = pd.to_numeric(sampleData_V ["37Ar IC1"]) * 1000
sampleData_mV ["err37Ar IC1"] = pd.to_numeric(sampleData_V ["err37Ar IC1"]) * 1000

print (sampleData_mV)

# sampleData_mV 40Ar F, err40Ar F, 39Ar F, err39Ar F, 38Ar F, err38Ar F, 37Ar F, err37Ar F, 36Ar F, err36Ar F,  