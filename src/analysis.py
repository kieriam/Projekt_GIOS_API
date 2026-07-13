import numpy as np

def calculate_stats(df):

    return {
        "Średnia": round(df["Wartość"].mean(),2),
        "Minimum": round(df["Wartość"].min(),2),
        "Maksimum": round(df["Wartość"].max(),2),
        "Mediana": round(df["Wartość"].median(),2),
        "Odchylenie": round(np.std(df["Wartość"]),2)
    }
    