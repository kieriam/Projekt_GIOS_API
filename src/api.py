import requests
from requests.exceptions import RequestException
import pandas as pd

core_url = "https://api.gios.gov.pl/pjp-api/v1/rest"

def get_stations():
    """
    Funkcja pobiera kompletną listę stacji pomiarowych dostępnych z API GIOŚ.

    Returns:
       pd.DataFrame: DataFrame zawierający id i nazwę stacji, gdy błąd zwraca pusty DataFrame.

    """
    url = f"{core_url}/station/findAll?page=0&size=500"

    try:
        response = requests.get(
            url,
            headers={"accept":"application/ld+json"},
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        return pd.DataFrame(data["Lista stacji pomiarowych"])

    except RequestException:
        return pd.DataFrame()

def get_sensors(station_id):
    """
    Pobiera listę czujników dla konkretnej stacji pomiarowej.

    Args: 
        station_id(int): identyfikator stacji.

    Returns:
        list : lista czujników dostępnych na danej stacji, w przypadku błędu zwraca pustą listę.
    """
    url = f"{core_url}/station/sensors/{station_id}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        return data["Lista stanowisk pomiarowych dla podanej stacji"]
    
    except RequestException:
        return []

def get_measurements(sensor_id):
    """
    Pobiera dane z wybranego czujnika.

    Args: 
        sensor_id(int): identyfikator stanowiska pomiarowego.

    Returns:
        pd.DataFrame: DataFrame zawierający datę i wartość pomiaru.
        W przypadu blędu pusty DataFrame
    """
    url = f"{core_url}/data/getData/{sensor_id}"

    try:
        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data =  response.json()

        if "Lista danych pomiarowych" not in data:
            return pd.DataFrame()

        return pd.DataFrame(data["Lista danych pomiarowych"])
    
    except RequestException:
        return pd.DataFrame()


