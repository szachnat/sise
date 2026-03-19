# 🧠 **SZTUCZNA INTELIGENCJA I SYSTEMY EKSPERTOWE – PROJEKTY**

Repozytorium zawiera rozwiązania dwóch zadań realizowanych w ramach kursu **Sztuczna inteligencja i systemy ekspertowe**.

## 📂 **STRUKTURA REPOZYTORIUM**

---
```text
.
├── zad1/ # Rozwiązywanie układanki "piętnastka"
├── zad2/ # Sieć neuronowa do korekcji lokalizacji robota
└── README.md
```
---


## 🔢 **ZADANIE 1 – PROBLEM „PIĘTNASTKI”**

### 📌 **OPIS**
Celem zadania było zaimplementowanie algorytmów przeszukiwania przestrzeni stanów w celu rozwiązania klasycznej układanki logicznej **15-puzzle**.

### ⚙️ **ZAIMPLEMENTOWANE ALGORYTMY**
- **BFS** (*Breadth-First Search* – przeszukiwanie wszerz)
- **DFS** (*Depth-First Search* – przeszukiwanie w głąb)
- **A\*** (*algorytm heurystyczny*)

### ⚙️ **TECHNOLOGIE**
- Python

### 🧪 **ZAKRES EKSPERYMENTÓW**
Przeprowadzono analizę porównawczą algorytmów pod względem:
- czasu znajdowania rozwiązania  
- długości rozwiązania  
- liczby odwiedzonych stanów  
- liczby przetworzonych stanów  
- maksymalnej głębokości rekursji  

### 📊 **WNIOSKI**
Algorytm **A\*** dzięki zastosowaniu heurystyki znacząco przewyższa BFS i DFS pod względem efektywności (czas oraz liczba stanów), zachowując jednocześnie optymalność rozwiązania.


## 🤖 **ZADANIE 2 – POPRAWA LOKALIZACJI ROBOTA (UWB)**

### 📌 **OPIS**
Zadanie polegało na stworzeniu **autorskiej implementacji sztucznej sieci neuronowej**, której celem była korekcja błędów pomiaru pozycji robota uzyskanych z systemu UWB.

### ⚙️ **TECHNOLOGIE**
- Python  
- implementacja sieci neuronowej **od podstaw** (bez bibliotek typu TensorFlow / PyTorch)

### 🧠 **ARCHITEKTURA SIECI**
Testowano różne warianty sieci:
- **1 warstwa ukryta** – 8 neuronów  
- **2 warstwy ukryte** – 10, 5 neuronów  
- **3 warstwy ukryte** – 8, 6, 4 neurony  

### 🔧 **SZCZEGÓŁY IMPLEMENTACYJNE**
- inicjalizacja wag: losowo z zakresu **[-0.5, 0.5]**  
- funkcja aktywacji: **ReLU**  
- uczenie: **backpropagation z momentum**  
- learning rate: **0.000001**  
- momentum: **0.9**  

**Warunek stopu:**
- maksymalna liczba epok lub  
- brak poprawy błędu MSE  

### 📊 **EWALUACJA**
Analiza obejmowała:
- przebieg błędu średniokwadratowego (**MSE**)  
- porównanie architektur  
- analizę błędów po korekcji  

### 📈 **WNIOSKI**
Zastosowanie sieci neuronowej pozwala istotnie poprawić dokładność pomiarów lokalizacji robota, a odpowiedni dobór architektury ma kluczowe znaczenie dla jakości wyników.

## ▶️ **JAK URUCHOMIĆ**

### **1. Sklonuj repozytorium:**
```bash
git clone <repo_url>
cd <repo_name>
```

Uruchom wybrane zadanie:

### **Zadanie 1:**

```bash
cd zad1
python main.py
```

### **Zadanie 2:**

```bash
cd zad2
python main.py
```

## 📌 **AUTORZY**

- Natalia Lewosińska

- Anna Chojnacka

## 📄 **LICENCJA**

[MIT Licence](LICENSE)
