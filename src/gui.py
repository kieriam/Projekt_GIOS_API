import tkinter as tk
from tkinter import ttk

from api import get_stations
from api import get_sensors

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
            text = "Wybierz stację"
        ).pack(pady=10)

        self.station_combo = ttk.Combobox(
            self.root,
            values=list(self.station_map.keys()),
            width=60
        )

        self.station_combo.pack()

        tk.Button(
            self.root,
            text="Pobierz dane",
            command=self.download_data
        ).pack(pady=10)

        self.text = tk.Text(
            self.root,
            height=20,
            width=100
        )
        self.text.pack()


    def download_data(self):
        station_name = self.station_combo.get()

        if not station_name:
            print("Nie wybrano stacji")
            return
        
        station_id = self.station_map[station_name]

        sensors = get_sensors(station_id)
       #print(type(sensors))
       #print(sensors)
       #self.text.delete("1.0",tk.END)

        sensors = get_sensors(station_id)

        for sensor in sensors:
            self.text.insert(
                tk.END,
                f"{sensor['Wskaźnik - kod']}"
                f"(ID:{sensor['Identyfikator stanowiska']})\n"
            )
        
       #for sensor in sensors["Lista stanowisk pomiarowych"]:
          # self.text.insert(
         #      tk.END,
         #      f"{sensor['id']} - {sensor['param']['paramCode']}\n"
          # )

    def run(self):
        self.root.mainloop()
