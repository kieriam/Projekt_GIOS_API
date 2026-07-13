import requests
import pandas as pd

core_url = "https://api.gios.gov.pl/pjp-api/v1/rest"

def get_stations():
    url = f"{core_url}/station/findAll?page=0&size=500"

    response = requests.get(
        url,
        headers={"accept":"application/ld+json"}
    )

    data = response.json()

    return pd.DataFrame(data["Lista stacji pomiarowych"])

def get_sensors(station_id):
    url = f"{core_url}/station/sensors/{station_id}"

    response = requests.get(url)
    data = response.json()

    return data["Lista stanowisk pomiarowych dla podanej stacji"]

def get_measurements(sensor_id):
    url = f"{core_url}/data/getData/{station_id}"

    response = requests.get(url)

    data =  response.json()
    df = pd.DataFrame(data["values"])

    df["value"] = pd.to_numeric(df["value"], errors = "coerce")
    df = df.dropna()

    return df


