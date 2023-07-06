#!/usr/bin/env python
# coding: utf-8

# # PyCalcolAr

# ### Inizializzazione

# In[48]:


# Importare le librerie utili per la creazione del codice
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from copy import deepcopy
import os

# se ricevi un errore "ModuleNotFoundError", devi istallare il pacchetto https://github.com/Phlya/adjustText:
# se usi Anaconda, apri "Anaconda prompt" dal menu Start e esegui   conda install -c conda-forge adjusttext
from adjustText import adjust_text


# ### Importazione del file sample_name_config.xlsx
# #### (unico parametro da modificare nel codice)

# In[52]:


# indicate the path of the sample_name_config.xlsx file

while True:
    config_path = input('Enter the path of the config file for the sample or "exit": ')

    if config_path == "exit":
        break

    elif os.path.exists(config_path) is False:
        print("The path does not exist")
        continue

    else:
        # In[53]:

        # read the sheet "analysis_parameter" from the sample_name_config.xlsx file

        df_config_sample_parameters = pd.read_excel(
            io=config_path, sheet_name="analysis_parameter"
        )

        # set the input values from the sample_name_config.xlsx file

        # nome del campione
        sample_name = df_config_sample_parameters.iat[0, 1]

        # definire il percorso del file calibrazione
        file_path_36 = df_config_sample_parameters.iat[1, 1]

        # definire il percorso dei file dati
        file_path_4 = df_config_sample_parameters.iat[2, 1]
        file_path_22 = df_config_sample_parameters.iat[3, 1]
        file_path_faradaysolo = df_config_sample_parameters.iat[4, 1]

        # filtrare il dataframe per numero run
        run_start = df_config_sample_parameters.iat[5, 1]
        run_end = df_config_sample_parameters.iat[6, 1]

        # days passed between the irradiation and the measurement of the sample
        delay = df_config_sample_parameters.iat[7, 1]

        # sample_weight, (cambia per ogni campione)
        sample_weight = df_config_sample_parameters.iat[8, 1]

        # J_factor e J_factor_errors, (cambia per ogni campione)
        J_factor = df_config_sample_parameters.iat[9, 1]
        J_factor_errors = df_config_sample_parameters.iat[10, 1]

        # sensitivity, (valore misurato un paio di volte l'anno)
        sensitivity = df_config_sample_parameters.iat[11, 1]

        # In[11]:

        # valori misurati 4/5 di volte l'anno

        # update_data = df_config_sample_parameters.iat[12, 1]

        background_spectrometer_dict = {
            "Background 40Ar": [
                df_config_sample_parameters.iat[13, 1],
                df_config_sample_parameters.iat[13, 2],
            ],
            "Background 39Ar": [
                df_config_sample_parameters.iat[14, 1],
                df_config_sample_parameters.iat[14, 2],
            ],
            "Background 38Ar": [
                df_config_sample_parameters.iat[15, 1],
                df_config_sample_parameters.iat[15, 2],
            ],
            "Background 37Ar": [
                df_config_sample_parameters.iat[16, 1],
                df_config_sample_parameters.iat[16, 2],
            ],
            "Background 36Ar": [
                df_config_sample_parameters.iat[17, 1],
                df_config_sample_parameters.iat[17, 2],
            ],
        }

        # ### Tabella: IRRADIATIONS CONSTANTS
        # #### (NON SONO DA MODIFICARE, valori costanti)

        # In[12]:

        # read the sheet "irradiation_constants" from the sample_name_config.xlsx file

        df_config_irradiation_constants = pd.read_excel(
            io=config_path, sheet_name="irradiation_constants"
        )

        # In[13]:

        irradiations_constants_dict = {
            "Atmospheric Ratio": [
                df_config_irradiation_constants.iat[0, 1],
                df_config_irradiation_constants.iat[0, 2],
            ],
            "(36Ar/37Ar) Ca": [
                df_config_irradiation_constants.iat[1, 1],
                df_config_irradiation_constants.iat[1, 2],
            ],
            "(38Ar/37Ar) Ca": [
                df_config_irradiation_constants.iat[2, 1],
                df_config_irradiation_constants.iat[2, 2],
            ],
            "(39Ar/37Ar) Ca": [
                df_config_irradiation_constants.iat[3, 1],
                df_config_irradiation_constants.iat[3, 2],
            ],
            "Lambda Ar37 [1/d]": [
                df_config_irradiation_constants.iat[4, 1],
                df_config_irradiation_constants.iat[4, 2],
            ],
            "Lambda Ar40 [1/Ma]": [
                df_config_irradiation_constants.iat[5, 1],
                df_config_irradiation_constants.iat[5, 2],
            ],
            "Interference 40K": [
                df_config_irradiation_constants.iat[6, 1],
                df_config_irradiation_constants.iat[6, 2],
            ],
            "Coefficient 39Ar for J": [
                df_config_irradiation_constants.iat[7, 1],
                df_config_irradiation_constants.iat[7, 2],
            ],
            "Coefficient Ca/K": [
                df_config_irradiation_constants.iat[8, 1],
                df_config_irradiation_constants.iat[8, 2],
            ],
            "Coefficient Cl/K": [
                df_config_irradiation_constants.iat[9, 1],
                df_config_irradiation_constants.iat[9, 2],
            ],
        }

        # ### Importazione files dello spettrometro
        # ### > file Triplo36 (file di calibrazione dell'aria)

        # In[14]:

        # to change the file name of triplo36_..._.txt, see above

        # definire la lista con gli indici delle colonne
        columns_names = [
            "40F",
            "err 40F",
            "38IC0",
            "err 38IC0",
            "36IC1",
            "err 36IC1",
            "36IC0",
            "err 36IC0",
            "36F",
            "err 36F",
            "gain IC0/IC1",
            "err gain IC0/IC1",
            "gain F/IC1",
            "err gain F/IC1",
            "gain F/IC0",
            "err gain F/IC0",
            "40F/36IC1",
            "err 40F/36IC1 ",
            "40F/36F",
            "err 40F/36F",
            "40F/36IC0",
            "err 40F/36IC0",
            "38IC0/36IC0",
            "err 38IC0/36IC0",
            "Run",
            "Path",
        ]

        # definire le colonne che contengono dati numerici (ad eccezione delle colonne 'Run' e 'Path')
        columns_numeric = [
            "40F",
            "err 40F",
            "38IC0",
            "err 38IC0",
            "36IC1",
            "err 36IC1",
            "36IC0",
            "err 36IC0",
            "36F",
            "err 36F",
            "gain IC0/IC1",
            "err gain IC0/IC1",
            "gain F/IC1",
            "err gain F/IC1",
            "gain F/IC0",
            "err gain F/IC0",
            "40F/36IC1",
            "err 40F/36IC1 ",
            "40F/36F",
            "err 40F/36F",
            "40F/36IC0",
            "err 40F/36IC0",
            "38IC0/36IC0",
            "err 38IC0/36IC0",
        ]

        # importare il file utilizzando caratteri separatori (sep = '\t|,') '\t' = tab, ',' = virgola
        airpipette_data = pd.read_csv(
            file_path_36, header=None, names=columns_names, sep="\t|,", engine="python"
        )

        # eliminare i caratteri "{}" dalle colonne relative all'errore
        airpipette_data = airpipette_data.replace(["{", "}"], ["", ""], regex=True)

        # convertire tutte le colonne del dataframe a numeric (float64)
        for i in columns_numeric:
            airpipette_data[i] = pd.to_numeric(airpipette_data[i])

        # definire un dataframe con le "colonne utili" (foglio airpipette_data)
        airpipette_data = airpipette_data[
            [
                "40F",
                "err 40F",
                "38IC0",
                "err 38IC0",
                "36IC1",
                "err 36IC1",
                "36IC0",
                "err 36IC0",
                "36F",
                "err 36F",
                "40F/36F",
                "err 40F/36F",
                "Run",
                "Path",
            ]
        ]

        # stampare il dataframe 'airpipette_data'
        # print("Air pipette initial imported data:")

        # dividere la colonna 'Run' in due colonne: nome del run e data/ora
        run_split = airpipette_data["Run"].str.split(" run on ")

        # formattare la colonna con il nome del run (del campione) in una serie pandas e associarle un nome
        run_name = run_split.str[0]
        run_name = run_name.replace(["'"], [""], regex=True)
        run_name.name = "Run_Name"

        # formattare la colonna con il numero del run
        run_number = airpipette_data["Path"].str.split(".").str[0]
        run_number = run_number.str.split("_").str[-1]
        run_number.name = "Run_Number"
        run_number = pd.to_numeric(run_number)

        # formattare la colonna con la data e l'ora in una serie pandas e associarle un nome, convertire il dato in datetime64
        dataora = run_split.str[1]
        dataora.name = "Date_Time"
        dataora = pd.to_datetime(dataora)

        # concatenare le nuove colonne all'inizio del dataframe airpipette_data
        airpipette_data = pd.concat(
            [run_name, run_number, dataora, airpipette_data], axis=1
        )

        # eliminare la colonna 'Run' (non più utilizzata)
        airpipette_data.drop("Run", axis=1, inplace=True)

        # conversione valore da count a V per tutti IC0,IC1 e relativi errori... (n / 62415000)
        airpipette_data.loc[:, "38IC0"] = (
            airpipette_data.loc[:, "38IC0"].values / 62415000
        )
        airpipette_data.loc[:, "err 38IC0"] = (
            airpipette_data.loc[:, "err 38IC0"].values / 62415000
        )
        airpipette_data.loc[:, "36IC1"] = (
            airpipette_data.loc[:, "36IC1"].values / 62415000
        )
        airpipette_data.loc[:, "err 36IC1"] = (
            airpipette_data.loc[:, "err 36IC1"].values / 62415000
        )
        airpipette_data.loc[:, "36IC0"] = (
            airpipette_data.loc[:, "36IC0"].values / 62415000
        )
        airpipette_data.loc[:, "err 36IC0"] = (
            airpipette_data.loc[:, "err 36IC0"].values / 62415000
        )
        airpipette_data.loc[:, "36F"] = airpipette_data.loc[:, "36F"].values / 62415000
        airpipette_data.loc[:, "err 36F"] = (
            airpipette_data.loc[:, "err 36F"].values / 62415000
        )

        # ### > file Run4 e Run22 (file di misura)

        # In[15]:

        # to change the file name of run4.txt, run22.txt, faradaysolo.txt see above

        # definire la lista con gli indici delle colonne
        column_names_run4 = [
            "40Ar F",
            "err40Ar F",
            "38Ar IC0",
            "err38Ar IC0",
            "36Ar IC1",
            "err36Ar IC1",
            "38Ar F",
            "err38Ar F",
            "36Ar IC0",
            "err36Ar IC0",
            "39Ar F",
            "err39Ar F",
            "37Ar IC0",
            "err37Ar IC0",
            "35Cl IC1",
            "err35Cl IC1",
            "39Ar IC0",
            "err39Ar IC0",
            "37Ar IC1",
            "err37Ar IC1",
            "gainF/IC0",
            "err gainF/IC0",
            "gainIC0/IC1",
            "err gainIC0/IC1",
            "40F/36IC1",
            "err40F/36IC1",
            "40F/36IC0",
            "err40F/36IC0",
            "Run",
            "Path",
        ]

        column_names_run22 = [
            "40Ar F",
            "err40Ar F",
            "38Ar IC0",
            "err38Ar IC0",
            "36Ar IC1",
            "err36Ar IC1",
            "38Ar F",
            "err38Ar F",
            "36Ar IC0",
            "err36Ar IC0",
            "39Ar F",
            "err39Ar F",
            "37Ar IC0",
            "err37Ar IC0",
            "35Cl IC1",
            "err35Cl IC1",
            "gainIC0/IC1",
            "err gainIC0/IC1",
            "40F/36IC1",
            "err40F/36IC1",
            "40F/36IC0",
            "err40F/36IC0",
            "Run",
            "Path",
        ]

        column_names_faradaysolo = [
            "40Ar F",
            "err40Ar F",
            "38Ar F",
            "err38Ar F",
            "36Ar F",
            "err36Ar F",
            "39Ar F",
            "err39Ar F",
            "37Ar F",
            "err37Ar F",
            "Run",
            "Path",
        ]

        # definire le colonne che contengono dati numerici
        colnames_numeric_4 = [
            "40Ar F",
            "err40Ar F",
            "38Ar IC0",
            "err38Ar IC0",
            "36Ar IC1",
            "err36Ar IC1",
            "38Ar F",
            "err38Ar F",
            "36Ar IC0",
            "err36Ar IC0",
            "39Ar F",
            "err39Ar F",
            "37Ar IC0",
            "err37Ar IC0",
            "35Cl IC1",
            "err35Cl IC1",
            "39Ar IC0",
            "err39Ar IC0",
            "37Ar IC1",
            "err37Ar IC1",
            "gainF/IC0",
            "err gainF/IC0",
            "gainIC0/IC1",
            "err gainIC0/IC1",
            "40F/36IC1",
            "err40F/36IC1",
            "40F/36IC0",
            "err40F/36IC0",
        ]

        colnames_numeric_22 = [
            "40Ar F",
            "err40Ar F",
            "38Ar IC0",
            "err38Ar IC0",
            "36Ar IC1",
            "err36Ar IC1",
            "38Ar F",
            "err38Ar F",
            "36Ar IC0",
            "err36Ar IC0",
            "39Ar F",
            "err39Ar F",
            "37Ar IC0",
            "err37Ar IC0",
            "35Cl IC1",
            "err35Cl IC1",
            "gainIC0/IC1",
            "err gainIC0/IC1",
            "40F/36IC1",
            "err40F/36IC1",
            "40F/36IC0",
            "err40F/36IC0",
        ]

        colnames_numeric_faradaysolo = column_names_faradaysolo[:-2]

        # importare i file run
        df_data_4 = pd.read_csv(
            file_path_4,
            header=None,
            index_col=False,
            names=column_names_run4,
            sep="\t|,",
            engine="python",
        )
        df_data_22 = pd.read_csv(
            file_path_22,
            header=None,
            index_col=False,
            names=column_names_run22,
            sep="\t|,",
            engine="python",
        )
        df_data_faradaysolo = pd.read_csv(
            file_path_faradaysolo,
            header=None,
            index_col=False,
            names=column_names_faradaysolo,
            sep="\t|,",
            engine="python",
        )

        # eliminare i caratteri "{}" dalle colonne
        df_data_4 = df_data_4.replace(["{", "}"], ["", ""], regex=True)
        df_data_22 = df_data_22.replace(["{", "}"], ["", ""], regex=True)
        df_data_faradaysolo = df_data_faradaysolo.replace(
            ["{", "}"], ["", ""], regex=True
        )

        # convertire tutte le colonne del dataframe df_data_4 a numeric (float64)
        for i in colnames_numeric_4:
            df_data_4[i] = pd.to_numeric(df_data_4[i])

        # convertire tutte le colonne del dataframe df_data_22 a numeric (float64)
        for i in colnames_numeric_22:
            df_data_22[i] = pd.to_numeric(df_data_22[i])

        # convertire tutte le colonne del dataframe df_data_faradaysolo a numeric (float64)
        for i in colnames_numeric_faradaysolo:
            df_data_faradaysolo[i] = pd.to_numeric(df_data_faradaysolo[i])

        df_data = pd.concat([df_data_4, df_data_22, df_data_faradaysolo], axis=0)

        # dividere la colonna 'Run' in due colonne: nome del run e data/ora
        run_split = df_data["Run"].str.split(" run on ")

        # formattare la colonna con il nome del run (del campione) in una serie pandas e associarle un nome
        run_name = run_split.str[0]
        run_name = run_name.replace(["'"], [""], regex=True)
        run_name.name = "Run_Name"

        # formattare la colonna con il numero del run
        run_number = df_data["Path"].str.split(".").str[0]
        run_number = run_number.str.split("_").str[-1]
        run_number.name = "Run_Number"
        run_number = pd.to_numeric(run_number)

        # formattare la colonna con la data e l'ora in una serie pandas e associarle un nome, convertire il dato in datetime64
        dataora = run_split.str[1]
        dataora.name = "Date_Time"
        dataora = pd.to_datetime(dataora)

        # concatenare le nuove colonne all'inizio del dataframe df_data
        df_data = pd.concat([run_name, run_number, dataora, df_data], axis=1)

        # eliminare la colonna 'Run' (non più utilizzata)
        df_data.drop("Run", axis=1, inplace=True)

        # ### Filtrare i dati per numero run  per selezionare un solo campione
        # #### Verificare correttezza della selezione nel dataframe visualizzato !

        # In[16]:

        df_data = df_data.loc[df_data["Run_Number"].between(run_start, run_end)]

        df_data.reset_index(drop=True, inplace=True)
        df_data.sort_values(
            "Date_Time",
            axis=0,
            ascending=True,
            inplace=True,
            kind="quicksort",
            na_position="last",
        )
        df_data.reset_index(drop=True, inplace=True)

        print("\n   > df_data:")
        print(df_data)

        # In[17]:

        # opzione selezione automatica della calibrazione più recente disponibile tra quelle più vecchie della misura
        sample_min = min(df_data["Date_Time"].to_list())
        older_calibration_df = airpipette_data[
            airpipette_data["Date_Time"] < sample_min
        ]
        data_w = max(older_calibration_df["Date_Time"].to_list())

        airpipette_data_filtered = airpipette_data[
            airpipette_data["Date_Time"] == data_w
        ]
        calibration_data = deepcopy(airpipette_data_filtered)
        print("\n\n   > calibration_data:")
        print(calibration_data)

        # In[18]:

        # CALCOLO GAIN F/ICO ISOTOPO 39Ar
        df_data.loc[:, "F/IC0_39Ar"] = (
            df_data["39Ar F"].values / df_data["39Ar IC0"].values
        )

        # df_data

        # ## Crea cartella specifica per ogni campione

        # In[19]:

        # genera una variabile che registra la data di analisi del campione

        date_analysis = df_data.iat[0, 2]

        # crea le cartelle dove vengono salvati i file di output

        directory_sample = (
            "Results/" + date_analysis.strftime("%Y-%m-%d") + " " + sample_name
        )

        directory_sample_plot = directory_sample + "/" + sample_name + "_plots"

        os.makedirs(directory_sample, exist_ok=True)
        os.makedirs(directory_sample_plot, exist_ok=True)

        # ### Operazioni derivate dal file di calibrazione triplo36 (fogli Excel airpipette_data e sample_data)
        # #### Per calcolare 1sig_rel (errore relativo) = err_abs / _Ar  (err_abs corrisponde all'errore che misura lo spettrometro)
        # #### 1sig_abs = errore assoluto, 1sig_rel = errore relativo

        # In[20]:

        # calcolare sig_rel 36_IC0
        value_err36IC0 = float(calibration_data["err 36IC0"].values)
        value_36IC0 = float(calibration_data["36IC0"].values)
        sig_rel_36IC0 = float(value_err36IC0 / value_36IC0)
        # print ('1sig_rel_36IC0: ', sig_rel_36IC0)

        # calcolare sig_rel 36_IC1
        value_err36IC1 = float(calibration_data["err 36IC1"].values)
        value_36IC1 = float(calibration_data["36IC1"].values)
        sig_rel_36IC1 = float(value_err36IC1 / value_36IC1)
        # print ('1sig_rel_36IC1: ', sig_rel_36IC1)

        # calcolare sig_rel 36_F
        value_err36F = float(calibration_data["err 36F"].values)
        value_36F = float(calibration_data["36F"].values)
        sig_rel_36F = float(value_err36F / value_36F)
        # print ('1sig_rel_36F: ', sig_rel_36F)

        # calcolare sig_rel 40F/36F
        value_err40F_36F = float(calibration_data["err 40F/36F"].values)
        value_40F_36F = float(calibration_data["40F/36F"].values)
        sig_rel_40F_36F = float(value_err40F_36F / value_40F_36F)
        # print ('1sig_rel_40F/36F: ', sig_rel_40F_36F)

        # calcolare GAIN_F/IC0
        value_36F = float(calibration_data["36F"].values)
        value_36IC0 = float(calibration_data["36IC0"].values)
        gain_F_IC0 = float(value_36F / value_36IC0)
        # print ('gain F/IC0: ', gain_F_IC0)

        # calcolare sig_abs GAIN_F/IC0
        sig_abs_F_ICO = gain_F_IC0 * (pow(sig_rel_36IC0, 2) + pow(sig_rel_36F, 2)) ** (
            1 / 2
        )
        # print ('sig_abs_F/ICO: ', sig_abs_F_ICO)

        # calcolare GAIN_F/IC1
        value_36F = float(calibration_data["36F"].values)
        value_36IC1 = float(calibration_data["36IC1"].values)
        gain_F_IC1 = float(value_36F / value_36IC1)
        # print ('gain F/IC1: ', gain_F_IC1)

        # calcolare sig_abs GAIN_F/IC1
        sig_abs_F_IC1 = gain_F_IC1 * (pow(sig_rel_36IC1, 2) + pow(sig_rel_36F, 2)) ** (
            1 / 2
        )
        # print ('sig_abs_F/IC1: ', sig_abs_F_IC1)

        # calcolare 36IC0 correzione gain
        corr_gain_36IC0 = value_36IC0 * gain_F_IC0
        # print ('corr_gain_36IC0: ', corr_gain_36IC0)

        # calcolare 40/36 correzione
        value_40F = float(calibration_data["40F"].values)
        corr_40_36 = (value_40F) / corr_gain_36IC0
        # print ('corr_40_36: ', corr_40_36)

        # calcolare sig_abs 40/36 correzione
        sig_abs_40_36 = corr_40_36 * (
            pow(sig_rel_36F, 2)
            + pow(
                calibration_data["err 40F"].values / calibration_data["40F"].values, 2
            )
        ) ** (1 / 2)
        # print ('sig_abs_40/36: ', sig_abs_40_36)

        # calcolare source frax
        source_frax = float(corr_40_36 / 298.56)
        # print ('source_frax: ', source_frax)

        # calcolare sig_abs source frax
        sig_abs_source_frax = source_frax * (sig_abs_40_36 / corr_40_36)
        # print ('sig_abs_source_frax: ', sig_abs_source_frax)

        # #### Definire tutti i parametri delle tabelle (A) e (B) del file Excel CalcolAr
        # ### Tabella: BACKGROUND SPECTROMETER

        # In[21]:

        # to change the background value measurements, see above

        background_spectrometer_df = pd.DataFrame.from_dict(
            background_spectrometer_dict, orient="index"
        )
        background_spectrometer_df.columns = ["value", "relative error"]

        # ### Tabella: IRRADIATIONS CONSTANTS
        # #### (NON SONO DA MODIFICARE, valori costanti)

        # In[22]:

        # to change the irradiation constants, see above

        irradiations_constants_df = pd.DataFrame.from_dict(
            irradiations_constants_dict, orient="index"
        )
        irradiations_constants_df.columns = ["value", "relative error"]

        # ### Tabella: IRRADIATIONS

        # In[23]:

        # to change sample weight, J factors, and sensitivity, see above

        # i seguenti calcoli vengono svolti dal codice

        # i gain_F_IC1 sono già stati calcolati precedentemente

        measured_40Ar_36Ar_pipettes_sensor36 = "IC1"
        measured_40Ar_36Ar_pipettes = (
            calibration_data["40F"].values / calibration_data["36IC1"].values
        )

        gain_rel_uncertainty_errors = sig_rel_40F_36F
        gain_rel_uncertainty = gain_rel_uncertainty_errors / gain_F_IC1

        # TODO this is just calculating calibration_data[36F] exactly (dividing and multiplying the same numbers)
        gain_corrected_40Ar_36Ar_pipettes = measured_40Ar_36Ar_pipettes / gain_F_IC1
        gain_corrected_40Ar_36Ar_pipettes_errors = (
            gain_corrected_40Ar_36Ar_pipettes
            / irradiations_constants_df.loc["Atmospheric Ratio", "value"]
        )

        pipette_rel_uncertainty = sig_abs_source_frax
        total_fractionation_uncertainty = sig_abs_source_frax

        irradiations_dict = {
            "Sample weight [g]": [sample_weight, 0],
            "J factor": [J_factor, J_factor_errors],
            "Sensitivity (mL/mV)": [sensitivity, 0],
            "Gain F/IC1": [gain_F_IC1, 0],
            "Gain rel uncertainty": [gain_rel_uncertainty, gain_rel_uncertainty_errors],
            "Gain corrected 40Ar/36Ar pipettes": [
                gain_corrected_40Ar_36Ar_pipettes[0],
                gain_corrected_40Ar_36Ar_pipettes_errors[0],
            ],
            "Pipette rel uncertainty": [pipette_rel_uncertainty[0], 0],
            "Total fractionation uncertainty": [total_fractionation_uncertainty[0], 0],
        }

        irradiations_df = pd.DataFrame.from_dict(irradiations_dict, orient="index")
        irradiations_df.columns = ["value", "relative error"]

        # ### Operazioni foglio Excel CalcolAr = file PyCalcolAr
        # #### Le operazione verranno aggiunte in un unico dataframe di risultati simili a quelle del file Excel CalcolAr

        # In[24]:

        # creare il dataframe input_data
        input_data_df = pd.DataFrame()

        # colonna Time costante
        input_data_df.loc[:, "Time"] = pd.Series(
            1 for k in range(0, len(df_data.index))
        )

        # 6° cella del codice (DA MODIFICARE MANUALMENTE DALL'UTENTE)
        input_data_df.loc[:, "Delay"] = pd.Series(
            delay for k in range(0, len(df_data.index))
        )

        # print(input_data_df)

        # ### Input = online Regression

        # In[25]:

        input_data_df.loc[:, "40Ar"] = df_data.loc[:, "40Ar F"].values * 1000
        input_data_df.loc[:, "err40Ar"] = df_data.loc[:, "err40Ar F"].values * 1000

        count_row = df_data.shape[0]

        for i in range(count_row):
            if pd.isna(df_data.loc[i, "39Ar IC0"]):
                input_data_df.loc[i, "39Ar"] = df_data.loc[i, "39Ar F"] * 1000
                input_data_df.loc[i, "err39Ar"] = df_data.loc[i, "err39Ar F"] * 1000
            elif (df_data.loc[i, "39Ar F"]) >= 0.003:
                input_data_df.loc[i, "39Ar"] = df_data.loc[i, "39Ar F"] * 1000
                input_data_df.loc[i, "err39Ar"] = df_data.loc[i, "err39Ar F"] * 1000
            else:
                input_data_df.loc[i, "39Ar"] = (
                    df_data.loc[i, "39Ar IC0"] * gain_F_IC0 * 1000
                )
                input_data_df.loc[i, "err39Ar"] = (
                    df_data.loc[i, "err39Ar IC0"] * gain_F_IC0 * 1000
                )

        for i in range(count_row):
            if pd.isna(df_data.loc[i, "38Ar IC0"]):
                input_data_df.loc[i, "38Ar"] = df_data.loc[i, "38Ar F"] * 1000
                input_data_df.loc[i, "err38Ar"] = df_data.loc[i, "err38Ar F"] * 1000
            else:
                input_data_df.loc[i, "38Ar"] = (
                    df_data.loc[i, "38Ar IC0"] * gain_F_IC0 * 1000
                )
                input_data_df.loc[i, "err38Ar"] = (
                    df_data.loc[i, "err38Ar IC0"] * gain_F_IC0 * 1000
                )

        for i in range(count_row):
            if pd.isna(df_data.loc[i, "37Ar IC0"]):
                input_data_df.loc[i, "37Ar"] = df_data.loc[i, "37Ar F"] * 1000
                input_data_df.loc[i, "err37Ar"] = df_data.loc[i, "err37Ar F"] * 1000
            else:
                input_data_df.loc[i, "37Ar"] = (
                    df_data.loc[i, "37Ar IC0"] * gain_F_IC0 * 1000
                )
                input_data_df.loc[i, "err37Ar"] = (
                    df_data.loc[i, "err37Ar IC0"] * gain_F_IC0 * 1000
                )
            # elif (df_data.loc[i, '37Ar IC1'])<= 0.001:
            # input_data_df.loc[i, '37Ar'] = df_data.loc[i, '37Ar IC0'] * gain_F_IC0 * 1000
            #  input_data_df.loc[i, 'err37Ar'] = df_data.loc[i, 'err37Ar IC0'] * gain_F_IC0 * 1000
        # else:
        # input_data_df.loc[i, '37Ar'] = df_data.loc[i, '37Ar IC1'] * df_data.loc[i, 'gainIC0/IC1'] * 1000
        # input_data_df.loc[i, 'err37Ar'] = df_data.loc[i, 'err37Ar IC1']* df_data.loc[i, 'gainIC0/IC1']  * 1000
        # print("wanrning verificare il gain: ", df_data.loc[i, 'gainIC0/IC1'])
        # print('i = ', i, ' - 37Ar IC0= ', input_data_df.loc[i, '37Ar IC0'], ' - 37Ar IC1= ', input_data_df.loc[i, '37Ar IC1'], ' - 37Ar = ', input_data_df.loc[i, '37Ar'])

        for i in range(count_row):
            if pd.isna(df_data.loc[i, "36Ar IC1"]):
                input_data_df.loc[i, "36Ar"] = df_data.loc[i, "36Ar F"] * 1000
                input_data_df.loc[i, "err36Ar"] = df_data.loc[i, "err36Ar F"] * 1000
            else:
                input_data_df.loc[i, "36Ar"] = (
                    df_data.loc[i, "36Ar IC1"] * gain_F_IC1 * 1000
                )
                input_data_df.loc[i, "err36Ar"] = (
                    df_data.loc[i, "err36Ar IC1"] * gain_F_IC1 * 1000
                )

        # ### Measured values corrected for mass spectrometer background

        # In[26]:

        results_data = input_data_df

        results_data.loc[:, "40Ar BC"] = (
            results_data.loc[:, "40Ar"].values
            - (
                results_data.loc[:, "39Ar"].values
                * irradiations_constants_df.loc["Interference 40K", "value"]
            )
            - background_spectrometer_df.loc["Background 40Ar", "value"]
        )
        results_data.loc[:, "1sigma_abs40"] = (
            pow(results_data.loc[:, "err40Ar"].values, 2)
            + pow(
                background_spectrometer_df.loc["Background 40Ar", "value"]
                * background_spectrometer_df.loc["Background 40Ar", "relative error"],
                2,
            )
        ) ** (1 / 2)
        results_data.loc[:, "1sigma_rel40"] = (
            results_data.loc[:, "1sigma_abs40"].values
            / results_data.loc[:, "40Ar BC"].values
        )

        results_data.loc[:, "39Ar BC"] = (
            results_data.loc[:, "39Ar"].values
            - background_spectrometer_df.loc["Background 39Ar", "value"]
        )
        results_data.loc[:, "1sigma_abs39"] = (
            pow(results_data.loc[:, "err39Ar"].values, 2)
            + pow(
                background_spectrometer_df.loc["Background 39Ar", "value"]
                * background_spectrometer_df.loc["Background 39Ar", "relative error"],
                2,
            )
        ) ** (1 / 2)
        results_data.loc[:, "1sigma_rel39"] = (
            results_data.loc[:, "1sigma_abs39"].values
            / results_data.loc[:, "39Ar BC"].values
        )

        results_data.loc[:, "38Ar BC"] = (
            results_data.loc[:, "38Ar"].values
            - background_spectrometer_df.loc["Background 38Ar", "value"]
        )
        results_data.loc[:, "1sigma_abs38"] = (
            pow(results_data.loc[:, "err38Ar"].values, 2)
            + pow(
                background_spectrometer_df.loc["Background 38Ar", "value"]
                * background_spectrometer_df.loc["Background 38Ar", "relative error"],
                2,
            )
        ) ** (1 / 2)
        results_data.loc[:, "1sigma_rel38"] = (
            results_data.loc[:, "1sigma_abs38"].values
            / results_data.loc[:, "38Ar BC"].values
        )

        results_data.loc[:, "37Ar BC"] = (
            results_data.loc[:, "37Ar"].values
            - background_spectrometer_df.loc["Background 37Ar", "value"]
        )
        results_data.loc[:, "1sigma_abs37"] = (
            pow(results_data.loc[:, "err37Ar"].values, 2)
            + pow(
                background_spectrometer_df.loc["Background 37Ar", "value"]
                * background_spectrometer_df.loc["Background 37Ar", "relative error"],
                2,
            )
        ) ** (1 / 2)
        results_data.loc[:, "1sigma_rel37"] = (
            results_data.loc[:, "1sigma_abs37"].values
            / results_data.loc[:, "37Ar BC"].values
        )

        results_data.loc[:, "36Ar BC"] = (
            results_data.loc[:, "36Ar"].values
            - background_spectrometer_df.loc["Background 36Ar", "value"]
        )
        results_data.loc[:, "1sigma_abs36"] = (
            pow(results_data.loc[:, "err36Ar"].values, 2)
            + pow(
                background_spectrometer_df.loc["Background 36Ar", "value"]
                * background_spectrometer_df.loc["Background 36Ar", "relative error"],
                2,
            )
        ) ** (1 / 2)
        results_data.loc[:, "1sigma_rel36"] = (
            results_data.loc[:, "1sigma_abs36"].values
            / results_data.loc[:, "36Ar BC"].values
        )

        # 37Ar decay

        results_data.loc[:, "Decay Factor"] = (
            irradiations_constants_df.loc["Lambda Ar37 [1/d]", "value"]
            * results_data.loc[0, "Time"]
            * math.exp(
                irradiations_constants_df.loc["Lambda Ar37 [1/d]", "value"]
                * results_data.loc[0, "Delay"]
            )
        ) / (
            1
            - math.exp(
                (-1) * irradiations_constants_df.loc["Lambda Ar37 [1/d]", "value"] * 1
            )
        )

        # Multiplier for Fract Corr: si moltiplichi l'isotopo leggero per il fattore

        results_data.loc[:, "Mult 4amu"] = irradiations_df.loc[
            "Gain corrected 40Ar/36Ar pipettes", "relative error"
        ]
        results_data.loc[:, "Mult 2amu"] = (
            results_data.loc[:, "Mult 4amu"].values + 1
        ) / 2
        results_data.loc[:, "Mult 1amu"] = (
            results_data.loc[:, "Mult 4amu"].values + 3
        ) / 4

        # Bg + Fract + Decay Corrected
        results_data.loc[:, "Ar36tot"] = (
            results_data.loc[:, "36Ar BC"].values
            * results_data.loc[:, "Mult 4amu"].values
        )
        results_data.loc[:, "1sigRel36tot"] = (
            pow(results_data.loc[:, "1sigma_rel36"].values, 2)
            + pow(irradiations_df.loc["Total fractionation uncertainty", "value"], 2)
        ) ** (1 / 2)

        results_data.loc[:, "Ar38tot"] = (
            results_data.loc[:, "38Ar BC"].values
            * results_data.loc[:, "Mult 2amu"].values
        )
        results_data.loc[:, "1sigRel38tot"] = (
            pow(results_data.loc[:, "1sigma_rel38"].values, 2)
            + 0.25
            * pow(irradiations_df.loc["Total fractionation uncertainty", "value"], 2)
        ) ** (1 / 2)

        results_data.loc[:, "Ar39tot"] = (
            results_data.loc[:, "39Ar BC"].values
            * results_data.loc[:, "Mult 1amu"].values
        )
        results_data.loc[:, "1sigRel39tot"] = (
            pow(results_data.loc[:, "1sigma_rel39"].values, 2)
            + 0.0625
            * pow(irradiations_df.loc["Total fractionation uncertainty", "value"], 2)
        ) ** (1 / 2)

        results_data.loc[:, "Ar37day0"] = (
            results_data.loc[:, "Decay Factor"].values
            * results_data.loc[:, "37Ar BC"].values
            * (
                results_data.loc[:, "Mult 4amu"].values
                * results_data.loc[:, "Mult 2amu"]
            )
        )
        results_data.loc[:, "1sigRel37corr"] = (
            pow(results_data.loc[:, "1sigma_rel37"].values, 2)
            + pow(irradiations_df.loc["Total fractionation uncertainty", "value"], 2)
            * 9
            / 16
        ) ** (1 / 2)

        # Interference Corrected
        results_data.loc[:, "Ar39Ca"] = results_data.loc[:, "Ar37day0"].values * (
            irradiations_constants_df.loc["(39Ar/37Ar) Ca", "value"]
        )
        results_data.loc[:, "1sigRel39Ca"] = (
            pow(results_data.loc[:, "1sigRel37corr"].values, 2) + 0.000225
        ) ** (1 / 2)
        results_data.loc[:, "1sigAbs39Ca"] = (
            results_data.loc[:, "1sigRel39Ca"].values
            * results_data.loc[:, "Ar39Ca"].values
        )

        results_data.loc[:, "Ar39K"] = (
            results_data.loc[:, "Ar39tot"].values - results_data.loc[:, "Ar39Ca"].values
        )
        results_data.loc[:, "1sigAbs39K"] = (
            pow(results_data.loc[:, "1sigAbs39Ca"].values, 2)
            + pow(
                results_data.loc[:, "1sigRel39tot"].values
                * results_data.loc[:, "Ar39tot"].values,
                2,
            )
        ) ** (1 / 2)

        results_data.loc[:, "Ar36Ca"] = (
            results_data.loc[:, "Ar37day0"].values
            * irradiations_constants_df.loc["(36Ar/37Ar) Ca", "value"]
        )
        results_data.loc[:, "1sigRel36Ca"] = (
            pow(results_data.loc[:, "1sigRel37corr"].values, 2) + 0.000225
        ) ** (1 / 2)
        results_data.loc[:, "1sigAbs36Ca"] = (
            results_data.loc[:, "1sigRel36Ca"].values
            * results_data.loc[:, "Ar36Ca"].values
        )

        results_data.loc[:, "Ar36Atm"] = (
            results_data.loc[:, "Ar36tot"].values - results_data.loc[:, "Ar36Ca"].values
        )
        results_data.loc[:, "1sigAbs36Atm"] = (
            pow(results_data.loc[:, "1sigAbs36Ca"].values, 2)
            + pow(
                results_data.loc[:, "1sigRel36tot"].values
                * results_data.loc[:, "Ar36tot"].values,
                2,
            )
        ) ** (1 / 2)
        results_data.loc[:, "1sigRel36Atm"] = (
            results_data.loc[:, "1sigAbs36Atm"].values
            / results_data.loc[:, "Ar36Atm"].values
        )

        results_data.loc[:, "Ar40Atm"] = (
            results_data.loc[:, "Ar36Atm"].values
            * irradiations_constants_df.loc["Atmospheric Ratio", "value"]
        )
        results_data.loc[:, "1sigAbs40Atm"] = (
            results_data.loc[:, "Ar40Atm"].values
            * results_data.loc[:, "1sigRel36Atm"].values
        )

        results_data.loc[:, "Ar40*"] = (
            results_data.loc[:, "40Ar BC"].values
            - results_data.loc[:, "Ar40Atm"].values
        )
        results_data.loc[:, "1sigAbs40*"] = (
            pow(results_data.loc[:, "1sigma_abs40"].values, 2)
            + pow(results_data.loc[:, "1sigAbs40Atm"].values, 2)
        ) ** (1 / 2)

        results_data.loc[:, "rendimento rad"] = (
            results_data.loc[:, "Ar40*"].values / results_data.loc[:, "40Ar BC"].values
        )
        results_data.loc[:, "error magnif"] = (
            1 / results_data.loc[:, "rendimento rad"].values - 1
        )
        results_data.loc[:, "error36*magnif"] = (
            results_data.loc[:, "1sigRel36Atm"].values
            * results_data.loc[:, "error magnif"].values
        )

        results_data.loc[:, "1sigRel40*"] = (
            results_data.loc[:, "1sigAbs40*"].values / results_data.loc[:, "Ar40*"]
        )

        results_data.loc[:, "Ar38Cl"] = (
            results_data.loc[:, "Ar38tot"].values
            - results_data.loc[:, "Ar39K"].values / 95
            - results_data.loc[:, "Ar36Atm"].values * 0.1847
            - results_data.loc[:, "Ar37day0"].values * 0.00027
        )
        results_data.loc[:, "1sigAbs38Cl"] = (
            pow(results_data.loc[:, "1sigRel38tot"].values, 2)
            + pow((results_data.loc[:, "1sigAbs39K"].values / 85), 2)
            + pow((results_data.loc[:, "1sigAbs36Atm"].values * 0.18855), 2)
            + pow(
                (
                    results_data.loc[:, "1sigRel37corr"].values
                    * results_data.loc[:, "Ar37day0"].values
                    * 0.00027
                ),
                2,
            )
        ) ** (1 / 2)
        results_data.loc[:, "1sigRel38Cl"] = (
            results_data.loc[:, "1sigAbs38Cl"].values
            / results_data.loc[:, "Ar38Cl"].values
        )

        # RESULTS

        results_data.loc[:, "40Ar_total"] = (
            irradiations_df.loc["Sensitivity (mL/mV)", "value"]
            * results_data.loc[:, "40Ar BC"].values
        )
        results_data.loc[:, "err_40Ar"] = (
            results_data.loc[:, "40Ar_total"].values
            * results_data.loc[:, "1sigma_rel40"].values
        )

        results_data.loc[:, "40Ar*"] = (
            irradiations_df.loc["Sensitivity (mL/mV)", "value"]
            * results_data.loc[:, "Ar40*"].values
        )
        results_data.loc[:, "err_40Ar*"] = (
            results_data.loc[:, "1sigRel40*"].values
            * results_data.loc[:, "40Ar*"].values
        )

        results_data.loc[:, "39_Ar"] = (
            irradiations_df.loc["Sensitivity (mL/mV)", "value"]
            * results_data.loc[:, "Ar39tot"].values
        )
        results_data.loc[:, "err_39Ar"] = (
            results_data.loc[:, "39_Ar"].values
            * results_data.loc[:, "1sigRel39tot"].values
        )

        # inserire variabile cella BP3 = sommatoria colonne 39Ar (BP)
        total_mL_39Ar = results_data.loc[:, "39_Ar"].sum()
        print("\n   > total_mL_39Ar:")
        print(total_mL_39Ar)

        results_data.loc[:, "% 39Ar"] = 100 * (
            results_data.loc[:, "39_Ar"].values / total_mL_39Ar
        )

        results_data.loc[:, "38_Ar"] = (
            irradiations_df.loc["Sensitivity (mL/mV)", "value"]
            * results_data.loc[:, "Ar38tot"].values
        )
        results_data.loc[:, "err_38Ar"] = (
            results_data.loc[:, "38_Ar"].values
            * results_data.loc[:, "1sigRel38tot"].values
        )

        results_data.loc[:, "38Ar_Cl"] = (
            irradiations_df.loc["Sensitivity (mL/mV)", "value"]
            * results_data.loc[:, "Ar38Cl"].values
        )
        results_data.loc[:, "err_38Cl"] = (
            results_data.loc[:, "1sigRel38Cl"].values
            * results_data.loc[:, "38Ar_Cl"].values
        )

        results_data.loc[:, "37_Ar"] = (
            irradiations_df.loc["Sensitivity (mL/mV)", "value"]
            * results_data.loc[:, "Ar37day0"].values
        )
        results_data.loc[:, "err_37Ar"] = (
            results_data.loc[:, "1sigRel37corr"].values
            * results_data.loc[:, "37_Ar"].values
        )

        results_data.loc[:, "36_Ar"] = (
            irradiations_df.loc["Sensitivity (mL/mV)", "value"]
            * results_data.loc[:, "Ar36tot"].values
        )
        results_data.loc[:, "err_36Ar"] = (
            results_data.loc[:, "1sigRel36tot"].values
            * results_data.loc[:, "36_Ar"].values
        )

        results_data.loc[:, "Age"] = (
            np.log(
                1
                + (
                    results_data.loc[:, "Ar40*"].values
                    * irradiations_df.loc["J factor", "value"]
                    / results_data.loc[:, "Ar39K"].values
                )
            )
            / irradiations_constants_df.loc["Lambda Ar40 [1/Ma]", "value"]
        )
        results_data.loc[:, "1sigma_err_Age"] = results_data.loc[:, "Age"].values * (
            pow(irradiations_df.loc["J factor", "relative error"], 2)
            + pow(results_data.loc[:, "1sigRel40*"].values, 2)
            + pow(
                results_data.loc[:, "1sigAbs39K"].values
                / results_data.loc[:, "Ar39K"].values,
                2,
            )
        ) ** (1 / 2)
        results_data.loc[:, "Age+2error"] = (
            results_data.loc[:, "Age"].values
            + 2 * results_data.loc[:, "1sigma_err_Age"].values
        )
        results_data.loc[:, "Age-2error"] = (
            results_data.loc[:, "Age"].values
            - 2 * results_data.loc[:, "1sigma_err_Age"].values
        )

        results_data.loc[:, "Ca/K"] = results_data.loc[:, "Ar37day0"].values * (
            1.94 / results_data.loc[:, "Ar39K"].values
        )
        results_data.loc[:, "err_Ca/K"] = results_data.loc[:, "Ca/K"].values * (
            pow(results_data.loc[:, "1sigRel37corr"].values, 2)
            + pow(
                results_data.loc[:, "1sigAbs39K"].values
                / results_data.loc[:, "Ar39K"].values,
                2,
            )
        ) ** (1 / 2)

        results_data.loc[:, "Cl/K"] = irradiations_constants_df.loc[
            "Coefficient Cl/K", "value"
        ] * (
            results_data.loc[:, "38Ar_Cl"].values / results_data.loc[:, "39_Ar"].values
        )
        results_data.loc[:, "err_Cl/K"] = results_data.loc[:, "Cl/K"].values * (
            pow(results_data.loc[:, "1sigRel38Cl"].values, 2)
            + pow(
                results_data.loc[:, "1sigAbs39K"].values
                / results_data.loc[:, "Ar39K"].values,
                2,
            )
        ) ** (1 / 2)

        results_data.loc[:, "39/40"] = (
            results_data.loc[:, "Ar39K"].values / results_data.loc[:, "40Ar BC"].values
        )
        results_data.loc[:, "err39/40"] = results_data.loc[:, "39/40"] * (
            pow(results_data.loc[:, "1sigma_rel40"].values, 2)
            + pow(
                results_data.loc[:, "1sigAbs39K"].values
                / results_data.loc[:, "Ar39K"].values,
                2,
            )
        ) ** (1 / 2)

        results_data.loc[:, "36/40"] = (
            results_data.loc[:, "Ar36tot"].values
            - (
                results_data.loc[:, "Ar37day0"].values
                * irradiations_constants_df.loc["(36Ar/37Ar) Ca", "value"]
            )
        ) / results_data.loc[:, "40Ar BC"].values
        results_data.loc[:, "err36/40"] = results_data.loc[:, "36/40"].values * (
            pow(results_data.loc[:, "1sigma_rel40"].values, 2)
            + pow(results_data.loc[:, "1sigRel36Atm"].values, 2)
        ) ** (1 / 2)
        print("\n   > results_data:")
        print(results_data)

        # ## Crea un dataframe di riassunto di dati di input e output ed esporta in .xlsx

        # In[27]:

        with pd.ExcelWriter(
            directory_sample + "/" + sample_name + "_results.xlsx"
        ) as writer:
            irradiations_df.to_excel(writer, sheet_name="Irradiation")
            irradiations_constants_df.to_excel(
                writer, sheet_name="Irradiation_constants"
            )
            calibration_data.to_excel(writer, sheet_name="Calibration")
            results_data.to_excel(writer, sheet_name="Results")

        # # Creazione dei grafici (FOR SPECTRUM)

        # In[28]:

        # read the sheet "plots_parameters" from the sample_name_config.xlsx file

        df_config_plot_parameters = pd.read_excel(
            io=config_path,
            sheet_name="plot_parameters",
        )

        # zoom_to_steps_str = df_config_plot_parameters.iat[1, 1]
        #     zoom_to_steps_str_list = zoom_to_steps_str.split(',')
        #
        #     zoom_to_steps = []
        #
        #     for element_str in zoom_to_steps_str_list:
        #
        #         element = int(element_str)
        #         zoom_to_steps.append(element)
        #

        # In[29]:

        # convert the variable "steps_to_show" to a list

        # zoom_to_steps_cl_k_age
        zoom_to_steps_str = df_config_plot_parameters.iat[1, 1]
        zoom_to_steps_str_list = zoom_to_steps_str.split(",")

        zoom_to_steps_cl_k_age = []

        for element_str in zoom_to_steps_str_list:
            element = int(element_str)
            zoom_to_steps_cl_k_age.append(element)

        # zoom_to_steps_ca_k_age
        zoom_to_steps_str = df_config_plot_parameters.iat[3, 1]
        zoom_to_steps_str_list = zoom_to_steps_str.split(",")

        zoom_to_steps_ca_k_age = []

        for element_str in zoom_to_steps_str_list:
            element = int(element_str)
            zoom_to_steps_ca_k_age.append(element)

        # zoom_to_steps_ca_k_cl_k
        zoom_to_steps_str = df_config_plot_parameters.iat[5, 1]
        zoom_to_steps_str_list = zoom_to_steps_str.split(",")

        zoom_to_steps_ca_k_cl_k = []

        for element_str in zoom_to_steps_str_list:
            element = int(element_str)
            zoom_to_steps_ca_k_cl_k.append(element)

        # zoom_to_steps_spectrum

        zoom_to_steps_str = df_config_plot_parameters.iat[7, 1]
        zoom_to_steps_str_list = zoom_to_steps_str.split(",")

        zoom_to_steps_spectrum = []

        for element_str in zoom_to_steps_str_list:
            element = int(element_str)
            zoom_to_steps_spectrum.append(element)

        # show_labels_for_steps

        zoom_to_steps_str = df_config_plot_parameters.iat[8, 1]
        zoom_to_steps_str_list = zoom_to_steps_str.split(",")

        show_labels_for_steps = []

        for element_str in zoom_to_steps_str_list:
            element = int(element_str)
            show_labels_for_steps.append(element)

        # In[30]:

        # funzione che se usa dopo
        def point_plot(x_data, y_data, zoom_to_steps, color):
            plt.plot(
                x_data,
                y_data,
                marker="o",
                markersize=8,
                markeredgecolor="black",
                markerfacecolor=color,
                linestyle="dashed",
                linewidth=1,
                color="grey",
            )

            ymin = y_data[zoom_to_steps].min()
            ymax = y_data[zoom_to_steps].max()
            plt.ylim((ymin - (ymax - ymin) / 8, ymax + (ymax - ymin) / 8))

            xmin = x_data[zoom_to_steps].min()
            xmax = x_data[zoom_to_steps].max()
            plt.xlim((xmin - (xmax - xmin) / 8, xmax + (xmax - xmin) / 8))

            texts = []

            # etichetta con numero step
            for i in results_data.index:
                step_annotation = plt.annotate(
                    i + 1,
                    (x_data[i], y_data[i]),
                    # horizontalalignment="center",
                    xytext=(5, 4),
                    textcoords="offset points",
                )
                texts.append(step_annotation)

            adjust_text(texts, x=list(x_data), y=list(y_data))

            plt.grid(color="grey", linestyle="--", linewidth=0.5)

        # In[31]:

        # Crea 'Cl/K vs Age'

        def plot_cl_k_age():
            # sceglie su quale steps voui zoomare (inizia da 0), DA MODIFICARE MANUALMENTE DALL'UTENTE

            point_plot(
                results_data["Cl/K"],
                results_data["Age"],
                zoom_to_steps_cl_k_age,
                color="green",
            )

            plt.ylabel("Apparent age [Ma]")
            plt.xlabel("Cl/K")

        plot_cl_k_age()

        # salva in formato SVG
        # SVG è un format di immagine vettoriale, puoi usarlo direttamente in Word come un'altra immagine

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_cl_k_age" + ".svg",
            bbox_inches="tight",
            pad_inches=0,
        )

        # salva in formato PNG

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_cl_k_age" + ".png",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.1,
        )

        plt.close()

        # In[32]:

        # Crea 'Ca/K vs Age'

        def plot_ca_k_age():
            # sceglie su quale steps voui zoomare (inizia da 0), DA MODIFICARE MANUALMENTE DALL'UTENTE

            point_plot(
                results_data["Ca/K"],
                results_data["Age"],
                zoom_to_steps_ca_k_age,
                color="yellow",
            )

            # plt.title('Ca/K vs Age')
            plt.xlabel("Ca/K")
            plt.ylabel("Apparent age [Ma]")

        plot_ca_k_age()

        # salva in formato SVG

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_ca_k_age" + ".svg",
            bbox_inches="tight",
            pad_inches=0,
        )

        # salva in formato PNG

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_ca_k_age" + ".png",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.1,
        )

        plt.close()

        # In[33]:

        # Crea 'Ca/K vs Cl/K'

        def plot_ca_k_cl_k():
            # sceglie su quale steps voui zoomare (inizia da 0), DA MODIFICARE MANUALMENTE DALL'UTENTE
            point_plot(
                results_data["Ca/K"],
                results_data["Cl/K"],
                zoom_to_steps_ca_k_cl_k,
                color="cyan",
            )

            # plt.title('Ca/K vs Cl/K')
            plt.xlabel("Ca/K")
            plt.ylabel("Cl/K")
            plt.grid(color="grey", linestyle="--", linewidth=0.5)

        plot_ca_k_cl_k()

        # salva in formato SVG

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_ca_k_cl_k" + ".svg",
            bbox_inches="tight",
            pad_inches=0,
        )

        # salva in formato PNG

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_ca_k_cl_k" + ".png",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.1,
        )

        plt.close()

        # In[34]:

        # Crea Isocrona '36Ar/39Ar vs 39Ar/40Ar'
        x = results_data["39/40"].dropna()
        y = results_data["36/40"].dropna()

        plt.plot(x, y, "o", color="black"),

        m, b = np.polyfit(x, y, 1)

        plt.plot(x, m * x + b, color="black")
        plt.title("36Ar/39Ar vs 39Ar/40Ar")
        plt.xlabel("39Ar/40Ar")
        plt.ylabel("36Ar/39Ar")
        plt.grid(color="grey", linestyle="--", linewidth=0.5)

        # salva in formato SVG

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_isochron" + ".svg",
            bbox_inches="tight",
            pad_inches=0,
        )

        # salva in formato PNG

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_isochron" + ".png",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.1,
        )

        plt.close()

        # ### Crea Spectrum Age plot

        # In[35]:

        # Crea la cumulata dei valori nella colonna '% 39Ar' del dataframe results data
        cumulative = results_data["% 39Ar"].cumsum()
        cumulative_df = pd.DataFrame(cumulative)

        # Crea dataframe Age+2error
        age_più_2error_df = pd.DataFrame(results_data["Age+2error"])

        # Crea dataframe Age-2error
        age_meno_2error_df = pd.DataFrame(results_data["Age-2error"])

        # Duplica i valori della cumulata
        double_cumulative_df = pd.DataFrame(np.repeat(cumulative_df.values, 2, axis=0))
        double_cumulative_df.columns = cumulative_df.columns

        # Rinomina il database double_cumulative (Cum%39)
        double_cumulative_df = double_cumulative_df.rename(columns={"% 39Ar": "Cum%39"})

        # Cancella l'ultima riga di (Cum%39)
        # print(double_cumulative_df.index[-1])
        double_cumulative_df = pd.DataFrame(
            double_cumulative_df.drop(index=double_cumulative_df.index[-1])
        )

        # Aggiungi "O" alla prima riga di (Cum%39)
        double_cumulative_df.loc[-1] = [0]  # adding a row
        double_cumulative_df.index = double_cumulative_df.index + 1  # shifting index
        double_cumulative_df = double_cumulative_df.sort_index()  # sorting by index

        # Duplica i valori di (Age+2error)
        double_age_più_2error_df = pd.DataFrame(
            np.repeat(age_più_2error_df.values, 2, axis=0)
        )
        double_age_più_2error_df.columns = age_più_2error_df.columns

        # Duplica i valori di (Age+2error)
        double_age_meno_2error_df = pd.DataFrame(
            np.repeat(age_meno_2error_df.values, 2, axis=0)
        )
        double_age_meno_2error_df.columns = age_meno_2error_df.columns

        # Unione dei dataframe
        double_cumulative_df["Age+2error"] = double_age_più_2error_df["Age+2error"]
        double_cumulative_df["Age-2error"] = double_age_meno_2error_df["Age-2error"]

        # In[36]:

        # Spectrum Age
        def plot_spectrum_age():
            plt.plot(
                double_cumulative_df["Cum%39"],
                double_cumulative_df["Age+2error"],
                label="Age+2error",
                color="blue",
            )
            plt.plot(
                double_cumulative_df["Cum%39"],
                double_cumulative_df["Age-2error"],
                label="Age−2error",
                color="orange",
            )
            # plt.title('Age Spectrum')
            plt.xlabel("Cumulative %Ar39 released")
            plt.ylabel("Apparent age [Ma]")
            plt.grid(color="grey", linestyle="--", linewidth=0.5)

            ymin = results_data["Age-2error"][zoom_to_steps_spectrum].min()
            ymax = results_data["Age+2error"][zoom_to_steps_spectrum].max()

            if (ymin - (ymax - ymin) / 4) < 0:
                plt.ylim((0, ymax + (ymax - ymin) / 8))
            else:
                plt.ylim((ymin - (ymax - ymin) / 4, ymax + (ymax - ymin) / 8))
            plt.xlim(0, 100)

            # etichette sul grafico
            for i in results_data.index:
                if i not in show_labels_for_steps:
                    continue

                xpos = (
                    double_cumulative_df["Cum%39"][i * 2]
                    + double_cumulative_df["Cum%39"][i * 2 + 1]
                ) / 2

                # etichetta con età
                plt.annotate(
                    "%.1f" % results_data["Age"][i],
                    (xpos, results_data["Age-2error"][i]),
                    rotation=-90,
                    horizontalalignment="center",
                    va="top",
                    xytext=(-1, -4),
                    textcoords="offset points",
                )

                # etichetta con numero step
                plt.annotate(
                    i + 1,
                    (xpos, results_data["Age+2error"][i]),
                    horizontalalignment="center",
                    xytext=(0, 4),
                    textcoords="offset points",
                )

            plt.legend(loc="lower right")

        plot_spectrum_age()

        # salva in formato SVG

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_spectrum" + ".svg",
            bbox_inches="tight",
            pad_inches=0,
        )

        # salva in formato PNG

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_spectrum" + ".png",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.1,
        )

        plt.close()

        # In[37]:

        # CONTROLLO SUL GUADAGNO
        # Crea 'F/IC0_39Ar vs Cum%39'

        def plot_gain_39():
            plt.scatter(cumulative_df, df_data["F/IC0_39Ar"], marker="o", color="black")
            # plt.title('F/IC0_39Ar vs Cum%39')
            plt.xlabel("Cum%39")
            plt.ylabel("F/IC0 39Ar")
            plt.grid(color="grey", linestyle="--", linewidth=0.5)
            # print(df_data.loc[:,'F/IC0_39Ar'])
            # print(cumulative_df)

        # plot_gain_39()

        # #### PLOT 'gainF/IC0 vs 40Ar F' and 'gainIC0/IC1 vs gainF/IC0'
        #

        # In[38]:

        # Crea 'gainF/IC0 vs 40Ar F'

        def plot_gain_40():
            plt.scatter(
                df_data["40Ar F"], df_data["gainF/IC0"], marker="o", color="black"
            )
            # plt.title('gainF/IC0 vs 40Ar F')
            plt.xlabel("40Ar F")
            plt.ylabel("gainF/IC0")
            plt.grid(color="grey", linestyle="--", linewidth=0.5)

        # plot_gain_40()

        # In[39]:

        # Crea la variabile 'gainIC1/IC0' da 'gainIC0/IC1

        df_data.loc[:, "gainIC1/IC0"] = pow(df_data["gainIC0/IC1"].values, -1)

        # In[40]:

        # Crea 'gainIC1/IC0 vs gainF/IC0'

        def plot_gain_gain_1():
            plt.scatter(
                df_data["gainF/IC0"], df_data["gainIC1/IC0"], marker="o", color="black"
            )
            # plt.title('gainIC1/IC0 vs gainF/IC0')
            plt.xlabel("gainF/IC0")
            plt.ylabel("gainIC1/IC0")
            plt.grid(color="grey", linestyle="--", linewidth=0.5)

        # plot_gain_gain()

        # In[41]:

        # Crea 'gainIC0/IC1 vs gainF/IC0'

        def plot_gain_gain_2():
            plt.scatter(
                df_data["gainF/IC0"], df_data["gainIC0/IC1"], marker="o", color="black"
            )
            # plt.title('gainIC1/IC0 vs gainF/IC0')
            plt.xlabel("gainF/IC0")
            plt.ylabel("gainIC0/IC1")
            plt.grid(color="grey", linestyle="--", linewidth=0.5)

        # plot_gain_gain_2()

        # ## Crea figura composta dati campioni (2x2)

        # In[42]:

        text_scale = 0.75

        cm = 1 / 2.54
        plt.subplots(figsize=(25 * cm / text_scale, 15 * cm / text_scale))

        grid_col = 2
        grid_row = 2

        plt.subplot(grid_col, grid_row, 1)
        plot_ca_k_age()

        plt.subplot(grid_col, grid_row, 2)
        plot_cl_k_age()

        plt.subplot(grid_col, grid_row, 3)
        plot_ca_k_cl_k()

        plt.subplot(grid_col, grid_row, 4)
        plot_spectrum_age()

        # salva in formato SVG

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_all" + ".svg",
            bbox_inches="tight",
            pad_inches=0,
        )

        # salva in formato PNG

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_all" + ".png",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.1,
        )

        plt.close()

        # ## Crea figura composta dati strumento (2x2)

        # In[43]:

        text_scale = 0.6

        cm = 1 / 2.54
        plt.subplots(figsize=(25 * cm / text_scale, 15 * cm / text_scale))

        grid_col = 2
        grid_row = 2

        plt.subplot(grid_col, grid_row, 1)
        plot_gain_39()

        plt.subplot(grid_col, grid_row, 2)
        plot_gain_40()

        plt.subplot(grid_col, grid_row, 3)
        plot_gain_gain_1()

        plt.subplot(grid_col, grid_row, 4)
        plot_gain_gain_2()

        filter_data_min = df_data.iat[0, 0]

        plt.suptitle(
            sample_name + ", " + date_analysis.strftime("%d %b %Y"), fontsize=18
        )

        # salva in formato SVG

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_instrument" + ".svg",
            bbox_inches="tight",
            pad_inches=0,
        )

        # salva in formato PNG

        plt.savefig(
            directory_sample_plot + "/" + sample_name + "_instrument" + ".png",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.1,
        )

        # salva in formato PNG nella cartella "plots_instruments" dove sono raccolti insieme tutti i dati dello strumento

        directory = "Instrument_plots"
        os.makedirs(directory, exist_ok=True)
        plt.savefig(
            os.path.join(
                directory,
                date_analysis.strftime("%Y-%m-%d") + " " + sample_name + ".png",
            ),
            bbox_inches="tight",
            pad_inches=0.1,
        )

        plt.close()
        print("Calculations and plotting finished")
        print("------------------------------------------")
