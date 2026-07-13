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
    url = f"{core_url}/data/getData/{sensor_id}"

    response = requests.get(url)

    data =  response.json()

    print(f"\nSensor ID: {sensor_id}")
    print(data)

    if "Lista danych pomiarowych" not in data:
        print(data)
        return pd.DataFrame()

    return pd.DataFrame(data["Lista danych pomiarowych"])
    
    


