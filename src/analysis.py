import numpy as np

def calculate_stats(df):

    return {
        "Średnia": round(df["value"].mean(),2),
        "Minimum": round(df["value"].min(),2),
        "Maksimum": round(df["value"].max(),2),
        "Mediana": round(df["value"].median(),2),
        "Odchylenie": round(np.std(df["value"]),2)
    }
    