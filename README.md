# Analiza jakości powietrza z wykorzystaniem API GIOŚ

## Spis treści
### Opis projektu
### Funkcjonalności
### Wykorzystane biblioteki
### Struktura projektu
### Uruchamianie
### Źródło dancyh

## Opis projektu

Projekt został wykonany przy użyciu języka Python i umożliwia pobieranie oraz analize danych dotyczących
jakości powietrza z oficjalnego API Głównego Inspektoratu Ochrony Środowiska (GIOŚ).
Aplikacja posiada interfejs graficzny wykonany z wykorzystaniem biblioteki Tkinter.
Użytkownik może wybrać dwie stacje pomiarowe, pobrać dotyczące ich dane pomiarowe, obliczyć podstawowe 
statystyki, porównać ich wyniki oraz porównać wyniki i wykresy dla wybranych zanieczyszczeń.
Projekt wykonany w ramach zaliczenia zajęć zaawansowane programowanie w języku Python.

## Funkcjonalności

* Pobieranie listy stacji pomiarowych z API GIOŚ
* Pobieranie danych pomiarowych dal wybranej stacji.
* Wyświetlanie danych.
* Obliczanie podstawowych statystyk(średnia, minimum, maksimum, mediana, odchylenie std)
* Porównanie statystyk dla dwóch wybranych stacji.
* Tworzenie wykresu ze stężeniem danego zanieczyszczenia.
* Porównanie wykresów dwóch stacji.

## Wykorzystane biblioteki

* tkinter
* requests
* pandas
* numpy
* matplotlib

## Struktura projektu
├── README.md
├── requirements.txt
└── src
    ├── analysis.py
    ├── api.py
    ├── gui.py
    └── main.py

## Źródło danych

Projekt korzysta z API Głównego Inspektoratu Ochrony Środowiska(GIOŚ).
