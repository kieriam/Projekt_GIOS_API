import tkinter as tk
from tkinter import ttk

from api import get_stations
from api import get_sensors
from api import get_measurements
from analysis import calculate_stats
from analysis import compare_stations

class AirQualityApp:

    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Analiza jakości powietrza")
        self.root.geometry("900x600")

        stations = get_stations()

        self.station_map = dict(
            zip(
                stations["Nazwa stacji"],
                stations["Identyfikator stacji"]
            )
        )

        tk.Label(
            self.root,
            text = "Wybierz stację 1"
        ).pack()

        self.station_combo = ttk.Combobox(
            self.root,
            values=list(self.station_map.keys()),
            width=60
        )

        self.station_combo.pack()

        tk.Label(
            self.root,
            text = "Wybierz stację 2"
        ).pack()

        self.station2_combo = ttk.Combobox(
            self.root,
            values=list(self.station_map.keys()),
            width=60
        )

        self.station2_combo.pack()

        tk.Label(
            self.root,
            text = "Wybierz statystykę"
        ).pack()

        #self.pollutant_combo =ttk.Combobox(
         #   self.root,
          #  values = ["PM10","PM2.5","NO2","NO","NOx","O3","SO2","CO","C6H6","BaP(PM10)"],
           # width=60
        #)
        self.pollutant_combo.pack()

        tk.Button(
            self.root,
            text="Pobierz dane",
            command=self.download_data
        ).pack(pady=10)

        self.text = tk.Text(
            self.root,
            height=10,
            width=50
        )
        self.text.pack()

        tk.Button(
            self.root,
            text="Oblicz statystyki",
            command=self.calculate_statistics
        ).pack(pady=10)

        self.stats_text = tk.Text(
            self.root,
            height=10,
            width=50
        )
        self.stats_text.pack(pady=10)

        tk.Button(
            self.root,
            text="Porównaj stacje",
           # command= self.compare_two_stations
            command= self.compare_stations
        ).pack(pady=10)

    def download_data(self):
        station_name = self.station_combo.get()

        if not station_name:
            self.text.insert(tk.END, "Nie wybrano stacji\n")
            return
        
        station_id = self.station_map[station_name]

        sensors = get_sensors(station_id)
       #print(type(sensors))
       #print(sensors)
       #self.text.delete("1.0",tk.END)

        #sensors = get_sensors(station_id)

        for sensor in sensors:
            self.text.insert(
                tk.END,
                f"{sensor['Wskaźnik - kod']}"
                f"(ID:{sensor['Identyfikator stanowiska']})\n"
            )

    def find_sensor(self, station_id,pollutant):
        sensors = get_sensors(station_id)

        for sensor in sensors:
            if sensor["Wskaźnik - kod"] == pollutant:
                return sensor["Identyfikator stanowiska"]

        return None

    def compare_two_stations(self):

        station1_name = self.station_combo.get()
        station2_name = self.station2_combo.get()

        pollutant = "PM10" #self.pollutant_combo.get()

        if not station1_name or not station2_name:
            return

        station1_id = self.station_map[station1_name]
        station2_id = self.station_map[station2_name]

        sensor1 = self.find_sensor(
            station1_id,
            pollutant
        )

        sensor2 = self.find_sensor(
            station2_id,
            pollutant
        )

        if sensor1 is None or sensor2 is None:
            self.text.insert(
                tk.END,
                "\nNie znaleziona czujnikaPM10\n"
            )
            return
        
        df1 = get_measurements(sensor1)
        df2 = get_measurements(sensor2)

        if df1.empty or df2.empty:
            self.text.insert(
                tk.END,
                "\nBrak danych pomiarowych\n"
            )
            return

        compare_stations(
            df1,
            station1_name,
            df2,
            station2_name,
            pollutant
        )


    def calculate_statistics(self):
        station_name = self.station_combo.get()

        if not station_name:
            self.stats_text.insert(tk.END, "Najpierw wybierz stację\n")
            return
        
        station_id = self.station_map[station_name]

        sensors = get_sensors(station_id)

        pm10_sensor = None

        for sensor in sensors:
            if sensor["Wskaźnik - kod"] == "PM10":
                pm10_sensor = sensor["Identyfikator stanowiska"]
                break

        if pm10_sensor is None:
            self.stats_text.insert(tk.END, "\nBrak czujnika PM10\n")
            return

        df = get_measurements(pm10_sensor)

        if df.empty:
            self.stats_text.insert(
                tk.END,
                "\nBrak danych pomiarowych.\n"
            )
            return

        stats = calculate_stats(df)

        self.stats_text.insert(tk.END,"\n---Statystyki PM10 ---\n")

        for key,value in stats.items():
            self.stats_text.insert(
                tk.END,
                f"{key}:{value}\n"
            )

       #for sensor in sensors["Lista stanowisk pomiarowych"]:
          # self.text.insert(
         #      tk.END,
         #      f"{sensor['id']} - {sensor['param']['paramCode']}\n"
          # )

    def run(self):
        self.root.mainloop()
