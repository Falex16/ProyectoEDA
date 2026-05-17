import io

import numpy as np
import pandas as pd


class DataAnalyzer:
    """Clase para encapsular tareas principales de analisis del dataset."""

    def __init__(self, dataframe):
        self.df_original = dataframe.copy()
        self.df = self._preparar_dataframe(dataframe)

    def _preparar_dataframe(self, dataframe):
        df = dataframe.copy()

        if "TotalCharges" in df.columns:
            df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

        if "SeniorCitizen" in df.columns:
            df["SeniorCitizen"] = df["SeniorCitizen"].map({0: "No", 1: "Yes"})

        return df

    def informacion_general(self):
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()

    def clasificar_variables(self):
        numericas = self.df.select_dtypes(include=np.number).columns.tolist()
        categoricas = self.df.select_dtypes(include=["object", "category"]).columns.tolist()
        return numericas, categoricas

    def estadisticas_descriptivas(self):
        return self.df.describe(include="all").T

    def valores_nulos(self):
        nulos = self.df.isnull().sum().reset_index()
        nulos.columns = ["Variable", "Valores nulos"]
        nulos["Porcentaje"] = (nulos["Valores nulos"] / len(self.df) * 100).round(2)
        return nulos

    def moda_variable(self, columna):
        if columna not in self.df.columns:
            return None

        moda = self.df[columna].mode(dropna=True)

        if moda.empty:
            return None

        return moda.iloc[0]

    def tasa_churn(self):
        if "Churn" not in self.df.columns:
            return None

        return (self.df["Churn"].value_counts(normalize=True) * 100).round(2)

    def resumen_por_churn(self, columna):
        return self.df.groupby("Churn")[columna].agg(["mean", "median", "std"]).round(2)
