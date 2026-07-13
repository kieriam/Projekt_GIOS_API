import numpy as np
import matplotlib.pyplot as plt

def calculate_stats(df):

    return {
        "Średnia": round(df["Wartość"].mean(),2),
        "Minimum": round(df["Wartość"].min(),2),
        "Maksimum": round(df["Wartość"].max(),2),
        "Mediana": round(df["Wartość"].median(),2),
        "Odchylenie": round(np.std(df["Wartość"]),2)
    }

def compare_stations(df1, station1_name,df2, station2_name, pollutant):

    df1["Data"] = pd.to_datetime(df1["Data"])
    df2["Data"] = pd.to_datetime(df2["Data"])

    plt.figure(figsize = (12,6))

    plt.plot(
        df1["Data"],
        df1["Wartość"],
        label = station1_name,
        marker="o"
    )

    plt.tittle(f"Porównanie stacji - {pollutant}")

    plt.xlabel("Data")
    plt.ylabel("µg/m³")

    plt.legend()
    plt.grid()

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()
    