import pandas as pd
import numpy as np
from util.utils import round_time
import inspect
import sys
import os
import re

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

def read_pipeline(data_path="data", resample=False, **kwargs):
    file_Conduvibilita = "TBaia_01m-Conducibilita'.txt"
    file_CTD = "TBaia_01m-CTD.txt"
    file_Ossigeno = "TBaia_01m-Ossigeno.txt"
    file_Winkler = "TBaia_01m-Winkler.txt"

    def convertTime(x):
        try:
            return pd.to_datetime(x["Data"] + "/" + x["Ora(UTC)"], format="%d/%m/%Y/%H:%M:%S")
        except:
            return -1

    ################### Conducibilita ###################
    Conducibilita_raw_df = pd.read_csv(os.path.join(data_path, file_Conduvibilita), encoding='cp1252', header=None, skiprows=11)
    Conducibilita_raw_df.iloc[0, 0] = re.sub("#", "", Conducibilita_raw_df.iloc[0, 0]).strip()
    Conducibilita_raw_df = Conducibilita_raw_df.squeeze().str.strip().apply(lambda x: re.sub("\s+", ",", x)).str.split(",", expand=True)
    # colNames = Conducibilita_raw_df.iloc[0, :].apply(lambda x: re.split(r"[(\\)\'_]", x)[0])
    colNames = Conducibilita_raw_df.iloc[0, :]

    Conducibilita_raw_df.columns = colNames
    Conducibilita_raw_df = Conducibilita_raw_df.iloc[1:, :]

    for j in range(2, Conducibilita_raw_df.shape[1]):
        Conducibilita_raw_df.iloc[:, j] = Conducibilita_raw_df.iloc[:, j].astype(np.float32)

    Conducibilita_raw_df["Time"] = Conducibilita_raw_df[["Data", "Ora(UTC)"]].apply(lambda x: convertTime(x), axis=1)
    Conducibilita_raw_df["Data"] = Conducibilita_raw_df["Time"].dt.date
    Conducibilita_raw_df["Ora(UTC)"] =  Conducibilita_raw_df["Time"].dt.time

    ################### CTD ###################

    CTD_raw_df = pd.read_csv(os.path.join(data_path, file_CTD), encoding='cp1252', header=None, skiprows=15)
    CTD_raw_df.iloc[0, 0] = re.sub("#", "", CTD_raw_df.iloc[0, 0]).strip()
    CTD_raw_df = CTD_raw_df.squeeze().str.strip().apply(lambda x: re.sub("\s+", ",", x)).str.split(",", expand=True)
    # colNames = CTD_raw_df.iloc[0, :].apply(lambda x: re.split(r"[(\\)\'_]", x)[0])
    colNames = CTD_raw_df.iloc[0, :]

    CTD_raw_df.columns = colNames
    CTD_raw_df = CTD_raw_df.iloc[1:, :]

    for j in range(2, CTD_raw_df.shape[1]):
        CTD_raw_df.iloc[:, j] = CTD_raw_df.iloc[:, j].astype(np.float32)

    CTD_raw_df["Time"] = CTD_raw_df[["Data", "Ora(UTC)"]].apply(lambda x: convertTime(x), axis=1)
    CTD_raw_df["Data"] = CTD_raw_df["Time"].dt.date
    CTD_raw_df["Ora(UTC)"] =  CTD_raw_df["Time"].dt.time

    ################### Ossigeno ###################
    Ossigeno_raw_df = pd.read_csv(os.path.join(data_path, file_Ossigeno), encoding='cp1252', header=None, skiprows=11)
    Ossigeno_raw_df.iloc[0, 0] = re.sub("#", "", Ossigeno_raw_df.iloc[0, 0]).strip()
    Ossigeno_raw_df = Ossigeno_raw_df.squeeze().str.strip().apply(lambda x: re.sub("\s+", ",", x)).str.split(",", expand=True)
    # colNames = Ossigeno_raw_df.iloc[0, :].apply(lambda x: re.split(r"[(\\)\'_]", x)[0])
    colNames = Ossigeno_raw_df.iloc[0, :]

    Ossigeno_raw_df.columns = colNames
    Ossigeno_raw_df = Ossigeno_raw_df.iloc[1:, :]

    for j in range(2, Ossigeno_raw_df.shape[1]):
        Ossigeno_raw_df.iloc[:, j] = Ossigeno_raw_df.iloc[:, j].astype(np.float32)

    Ossigeno_raw_df["Time"] = Ossigeno_raw_df[["Data", "Ora(UTC)"]].apply(lambda x: convertTime(x), axis=1)
    Ossigeno_raw_df["Data"] = Ossigeno_raw_df["Time"].dt.date
    Ossigeno_raw_df["Ora(UTC)"] =  Ossigeno_raw_df["Time"].dt.time

    ################### Winkler ###################
    Winkler_raw_df = pd.read_csv(os.path.join(data_path, file_Winkler), encoding='cp1252', header=None, skiprows=10)
    Winkler_raw_df.iloc[0, 0] = re.sub("#", "", Winkler_raw_df .iloc[0, 0]).strip()
    Winkler_raw_df = Winkler_raw_df.squeeze().str.strip().apply(lambda x: re.sub("\s+", ",", x)).str.split(",", expand=True)
    colNames = Winkler_raw_df.iloc[0, :]
    # colNames = Winkler_raw_df.iloc[0, :].apply(lambda x: re.split(r"[(\\)\'_]", x)[0])

    Winkler_raw_df.columns = colNames
    Winkler_raw_df = Winkler_raw_df.iloc[1:, :]

    for j in range(2,  Winkler_raw_df.shape[1]):
        Winkler_raw_df.iloc[:, j] = Winkler_raw_df.iloc[:, j].astype(np.float32)

    Winkler_raw_df["Time"] = Winkler_raw_df[["Data", "Ora(UTC)"]].apply(lambda x: convertTime(x), axis=1)
    Winkler_raw_df["Data"] = Winkler_raw_df["Time"].dt.date
    Winkler_raw_df["Ora(UTC)"] =  Winkler_raw_df["Time"].dt.time

    ################### Drop NA ###################
    Ossigeno_na_df = Ossigeno_raw_df.where( Ossigeno_raw_df!=-9999, other=None )
    Winkler_na_df = Winkler_raw_df.where( Winkler_raw_df!=-9999, other=None )
    CTD_na_df = CTD_raw_df.where( CTD_raw_df!=-9999, other=None )
    Conducibilita_na_df = Conducibilita_raw_df.where( Conducibilita_raw_df!=-9999, other=None )

    Conducibilita_without_na_df = Conducibilita_na_df.dropna()
    Ossigeno_without_na_df = Ossigeno_na_df.dropna(subset=["Ossigeno(mg/l)"])
    Winkler_without_na_df = Winkler_na_df.dropna()
    CTD_without_na_df = CTD_na_df.dropna(subset=["Ossigeno(mg/l)"])

    ################### Subset DF ###################
    Ossigeno_without_na_sub_df = Ossigeno_without_na_df[["Data", "Ora(UTC)", "Pressione(db)", "Ossigeno(mg/l)", "Temperatura(°C)", "Time"]]
    CTD_without_na_sub_df = CTD_without_na_df[["Data", "Ora(UTC)", "Pressione(db)", "Ossigeno(mg/l)", "Temperatura(°C)", "Time"]]
    Conducibilita_without_na_sub_df = Conducibilita_without_na_df[["Data", "Ora(UTC)", "Pressione(db)", "Salinita'(PSU)", "Temperatura(°C)", "Time"]]

    ################### Round Time ###################
    Ossigeno_without_na_sub_df["Time_rounded"] = Ossigeno_without_na_sub_df["Time"]
    CTD_without_na_sub_df["Time_rounded"] = CTD_without_na_sub_df["Time"]
    Conducibilita_without_na_sub_df["Time_rounded"] = Conducibilita_without_na_sub_df["Time"]
    Ossigeno_without_na_sub_df["Time_rounded"] = Ossigeno_without_na_sub_df["Time_rounded"].apply(lambda x: round_time(x))
    CTD_without_na_sub_df["Time_rounded"] = CTD_without_na_sub_df["Time_rounded"].apply(lambda x: round_time(x))
    Conducibilita_without_na_sub_df["Time_rounded"] = Conducibilita_without_na_sub_df["Time_rounded"].apply(lambda x: round_time(x))

    Ossigeno_without_na_sub_df.rename({"Ossigeno(mg/l)": "Ossigeno(mg/l)_Ossigeno", "Pressione(db)": "Pressione(db)_Ossigeno", "Temperatura(°C)": "Temperatura(°C)_Ossigeno"}, axis=1, inplace=True)
    Conducibilita_without_na_sub_df.rename({"Salinita'(PSU)": "Salinita(PSU)_Conducibilita", "Pressione(db)": "Pressione(db)_Conducibilita", "Temperatura(°C)": "Temperatura(°C)_Conducibilita"}, axis=1, inplace=True)
    CTD_without_na_sub_df.rename({"Ossigeno(mg/l)": "Ossigeno(mg/l)_CTD", "Pressione(db)": "Pressione(db)_CTD", "Temperatura(°C)": "Temperatura(°C)_CTD"}, axis=1, inplace=True)
    
    return Ossigeno_without_na_sub_df, Conducibilita_without_na_sub_df, CTD_without_na_sub_df