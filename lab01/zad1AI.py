import datetime
import math

# Funkcja pomocnicza do liczenia biorytmu
def licz_fale(dni, cykl):
    return math.sin((2 * math.pi / cykl) * dni)

# Dane wejściowe
imie = input("Podaj imię: ")
rok = int(input("Podaj rok urodzenia: "))
miesiac = int(input("Podaj miesiąc urodzenia: "))
dzien = int(input("Podaj dzień urodzenia: "))

data_urodzenia = datetime.date(rok, miesiac, dzien)
dni_zycia = (datetime.date.today() - data_urodzenia).days

# Obliczamy fale dla dzisiaj i dla jutra (dni_zycia + 1)
cykle = {"fizyczna": 23, "emocjonalna": 28, "intelektualna": 33}

dzis_fale = {nazwa: licz_fale(dni_zycia, c) for nazwa, c in cykle.items()}
# dzis_fale = {}
# for nazwa, c in cykle.items():
#     wynik = licz_fale(dni_zycia, c)
#     dzis_fale[nazwa] = wynik
jutro_fale = {nazwa: licz_fale(dni_zycia + 1, c) for nazwa, c in cykle.items()}

zle_dzis = sum(1 for v in dzis_fale.values() if v < -0.5)
dobre_jutro = sum(1 for v in jutro_fale.values() if v > 0.5)

print(f"\nWitaj {imie}!")

if zle_dzis >= 2:
    if dobre_jutro >= 2:
        print("Nie martw się – jest źle, ale jutro będzie dobrze!")
    else:
        print("Dzisiaj masz gorszy dzień, oszczędzaj siły.")
else:
    print("Masz świetny dzień! Korzystaj z energii.")

# Opcjonalnie: wypisz wartości
for nazwa, wartosc in dzis_fale.items():
    print(f"Fala {nazwa}: {wartosc:.2f}")

######################################################3
#############################################################33
#################################################################3

import math
from datetime import date

def oblicz_biorytm(dni, cykl):
    return math.sin((2 * math.pi / cykl) * dni)

def ocen_dzien(dni):
    wyniki = {
        "fizyczny": oblicz_biorytm(dni, 23),
        "emocjonalny": oblicz_biorytm(dni, 28),
        "intelektualny": oblicz_biorytm(dni, 33)
    }
    
    pozytywne = sum(1 for v in wyniki.values() if v > 0.5)
    negatywne = sum(1 for v in wyniki.values() if v < -0.5)
    
    return pozytywne, negatywne, wyniki

# Pobieranie danych od użytkownika
print("--- Kalkulator Biorytmu ---")
imie = input("Jak masz na imię? ")
rok = int(input("Rok urodzenia: "))
miesiac = int(input("Miesiąc urodzenia (1-12): "))
dzien = int(input("Dzień urodzenia: "))

data_urodzenia = date(rok, miesiac, dzien)
dzisiaj = date.today()
dni_zycia = (dzisiaj - data_urodzenia).days

# Analiza dzisiejszego dnia
poz, neg, wartosci = ocen_dzien(dni_zycia)

print(f"\nWitaj {imie}!")
print(f"Dzisiaj mija Twój {dni_zycia} dzień życia.")

if poz >= 2:
    print("Masz SUPER DZIEŃ! Przynajmniej dwa Twoje cykle są w szczytowej formie.")
elif neg >= 2:
    print("Dzisiaj masz słabszy dzień (minimum dwa cykle poniżej -0.5).")
    
    # Sprawdzamy jutro
    poz_jutro, neg_jutro, _ = ocen_dzien(dni_zycia + 1)
    if poz_jutro >= 2 or neg_jutro < 2:
        print("Głowa do góry! Jutro będzie lepiej.")
    else:
        print("Jutro też zapowiada się wymagająco, oszczędzaj siły.")
else:
    print("To jest przeciętny dzień – stabilizacja to też dobra rzecz.")

# Wyświetlenie szczegółów dla ciekawskich
print("\nSzczegółowe wyniki (od -1 do 1):")
for cykl, wynik in wartosci.items():
    print(f"- {cykl.capitalize()}: {wynik:.2f}")

# 2.5 min