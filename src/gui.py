import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import pandas as pd

from api import get_stations
from api import get_sensors
from api import get_measurements
from analysis import calculate_stats
from analysis import compare_stations

class AirQualityApp:

    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Analiza jakości powietrza")
        self.root.geometry("1200x900")

        stations = get_stations()

        self.left_frame = tk.Frame(self.root)
        self.left_frame.grid(row=0, column = 0, padx=10, pady=10)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row=0, column = 1, padx=10, pady=10)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.grid(row=1, column = 0,columnspan=2, padx=10, pady=10)

        self.station_map = dict(
            zip(
                stations["Nazwa stacji"],
                stations["Identyfikator stacji"]
            )
        )

        tk.Label(
            self.left_frame,
            text = "Wybierz stację 1"
        ).pack()

        self.station_combo = ttk.Combobox(
            self.left_frame,
            values=list(self.station_map.keys()),
            width=60
        )

        self.station_combo.pack()

        tk.Label(
            self.right_frame,
            text = "Wybierz stację 2"
        ).pack()

        self.station2_combo = ttk.Combobox(
            self.right_frame,
            values=list(self.station_map.keys()),
            width=60
        )

        self.station2_combo.pack()

        tk.Label(
            self.bottom_frame,
            text = "Wybierz parametr do wykresu"
        ).pack()

        

        tk.Button(
            self.left_frame,
            text="Pobierz dane 1 stacji",
            command=self.download_station1
        ).pack(pady=5)

        tk.Button(
            self.right_frame,
            text="Pobierz dane 2 stacji",
            command=self.download_station2
        ).pack(pady=5)

        self.text = tk.Text(
            self.left_frame,
            height=10,
            width=50
        )
        self.text.pack()

        self.text2 = tk.Text(
            self.right_frame,
            height=10,
            width=50
        )
        self.text2.pack()

        #tk.Button(
         #   self.root,
          #  text="Oblicz statystyki",
           # command=self.calculate_statistics
        #).pack(pady=10)

        tk.Button(
            self.left_frame,
            text="Statystyki stacji 1",
            command=self.calculate_statistics_station1
        ).pack(pady=5)

        tk.Button(
            self.right_frame,
            text="statystyki stacji 2",
            command=self.calculate_statistics_station2
        ).pack(pady=5)

        self.stats_text = tk.Text(
            self.left_frame,
            height=10,
            width=50
        )
        self.stats_text.pack(pady=10)

        self.stats_text2 = tk.Text(
            self.right_frame,
            height=10,
            width=50
        )
        self.stats_text2.pack(pady=10)

        self.pollutant_combo =ttk.Combobox(
            self.bottom_frame,
            values = ["PM10","PM2.5","NO2","NO","NOx","O3","SO2","CO","C6H6","BaP(PM10)"],
            width=60
        )
        self.pollutant_combo.pack()

        tk.Button(
            self.bottom_frame,
            text="Porównaj wykresy",
            command= self.compare_two_stations
            #command= self.compare_statistics
        ).pack(pady=10)

        tk.Button(
            self.bottom_frame,
            text="Porównaj stacje",
           # command= self.compare_two_stations
            command= self.compare_statistics
        ).pack(pady=10)

        self.compare_text = tk.Text(
            self.bottom_frame, 
            width=80,
            height=8
        )
        self.compare_text.pack()

        tk.Button(
            self.left_frame,
            text="Wykres stacji 1",
            command=self.plot_station1
        ).pack(pady=5)

        tk.Button(
            self.right_frame,
            text="Wykres stacji 2",
            command=self.plot_station2
        ).pack(pady=5)

    def download_data(self, station_combo, textbox):

        textbox.delete("1.0", tk.END)

        station = station_combo.get()

        if station == "":
            textbox.insert(tk.END, "Nie wybrano stacji\n")
            return

        station_id = self.station_map[station]

        sensors = get_sensors(station_id)

        for sensor in sensors:

            sensor_id = sensor["Identyfikator stanowiska"]
            pollutant = sensor["Wskaźnik - kod"]

            df = get_measurements(sensor_id)

            textbox.insert(
                tk.END,
                f"\n===== {pollutant} =====\n"
            )

            if df.empty:
                textbox.insert(tk.END,"Brak danych\n")
            else:
                textbox.insert(tk.END,df.to_string(index=False))
                textbox.insert(tk.END,"\n")

    def find_sensor(self, station_id,pollutant):
        sensors = get_sensors(station_id)

        for sensor in sensors:
            if sensor["Wskaźnik - kod"] == pollutant:
                return sensor["Identyfikator stanowiska"]

        return None

    def compare_two_stations(self):

        station1_name = self.station_combo.get()
        station2_name = self.station2_combo.get()

        pollutant = self.pollutant_combo.get()

        if not station1_name or not station2_name or not pollutant:
            self.compare_text.delete("1.0", tk.END)
            self.compare_text.insert(
                tk.END,
                "Wybierz obie stacje oraz parametr."
            )
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


    def calculate_statistics(self, station_combo, textbox):
        station_name = station_combo.get()

        if not station_name:
            textbox.insert(tk.END, "Najpierw wybierz stację\n")
            return
        
        textbox.delete("1.0",tk.END)

        station_id = self.station_map[station_name]

        sensors = get_sensors(station_id)

        for sensor in sensors:

            pollutant = sensor["Wskaźnik - kod"]

            sensor_id = sensor["Identyfikator stanowiska"]

            df = get_measurements(sensor_id)

            if df.empty:
                continue

            stats = calculate_stats(df)

            textbox.insert(
                tk.END,
                f"\n====={pollutant}=====\n"
            )

            for key, value in stats.items():

                textbox.insert(
                    tk.END,
                    f"{key}:{value}\n"
                )

    def calculate_statistics_station1(self):
        self.calculate_statistics(
            self.station_combo,
            self.stats_text
        )

    def calculate_statistics_station2(self):
        self.calculate_statistics(
            self.station2_combo,
            self.stats_text2
        )

    def download_station1(self):
        self.download_data(
            self.station_combo,
            self.text
        )

    def download_station2(self):
        self.download_data(
            self.station2_combo,
            self.text2
        )

    def compare_statistics(self):

        self.compare_text.delete("1.0", tk.END)

        station1 = self.station_combo.get()
        station2 = self.station2_combo.get()

        if not station1 or not station2:
            self.compare_text.insert(
                tk.END,
                "Wybierz obie stacje.\n"
            )
            return

        station1_id = self.station_map[station1]
        station2_id = self.station_map[station2]

        sensors1 = get_sensors(station1_id)
        #sensors2 = get_sensors(station2_id)

        for sensor in sensors1:
            pollutant = sensor["Wskaźnik - kod"]
            sensor_id1 = sensor["Identyfikator stanowiska"]

            sensor_id2 = self.find_sensor(
                station2_id,
                pollutant
            )

            if sensor_id2 is None:
                continue
            
            df1 = get_measurements(sensor_id1)
            df2 = get_measurements(sensor_id2)

            if df1.empty or df2.empty:
                continue

            stats1 = calculate_stats(df1)
            stats2 = calculate_stats(df2)

            self.compare_text.insert(
                tk.END,
                f"\n====={pollutant}=====\n"
            )

            for key in stats1:
                self.compare_text.insert(
                    tk.END,
                    f"{key}:{stats1[key]} | {stats2[key]}\n"
                )

    def plot_station(self, station_combo, textbox):

        station_name = station_combo.get()
        pollutant = self.pollutant_combo.get()

        if not station_name or not pollutant:
            return

        station_id = self.station_map[station_name]

        sensor_id = self.find_sensor(
            station_id,
            pollutant
        )

        if sensor_id is None:
            textbox.insert(
                tk.END,
                "\nBrak takiego parametru w stacji\n"
            )
            return
        
        df = get_measurements(sensor_id)

        if df.empty:
            textbox.insert(
                tk.END,
                "\nBrak danych pomiarowych\n"
            )
            return

        df["Data"] = pd.to_datetime(df["Data"])

        plt.figure(figsize=(10,5))

        plt.plot(
            df["Data"],
            df["Wartość"],
            marker="o",
            label=station_name
        )

        plt.title(
            f"{station_name} - {pollutant}"
        )

        plt.legend()

        plt.xlabel("Data")
        plt.ylabel("µg/m³")

        plt.xticks(rotation=45)

        plt.grid()

        plt.tight_layout()

        plt.show()

    def plot_station1(self):
        self.plot_station(
            self.station_combo,
            self.text
        )

    def plot_station2(self):
        self.plot_station(
            self.station2_combo,
            self.text2
        )

    def run(self):
        self.root.mainloop()
