import math
import random
import matplotlib.pyplot as plt

h = 100.0  
v0 = 50.0  
g = 9.81   

cel = random.randint(50, 340)
print(f"Cel znajduje się w odległości {cel} metrów")

trafiony = False
proby = 0
odleglosc = 0
kat_rad = 0
cos_a = 0  # Zmienna do przechowania cosinusa dla wykresu

while not trafiony:
    proby += 1
    try:
        kat_stopnie = float(input("\nPodaj kąt (0-89): "))
        # Zabezpieczenie przed dzieleniem przez zero (cos(90) = 0) oraz kątami ujemnymi
        if kat_stopnie < 0 or kat_stopnie >= 90:
            print("Kąt strzału musi być z przedziału od 0 do 89 stopni.")
            continue
    except ValueError:
        print("To nie jest prawidłowa liczba")
        continue
    
    kat_rad = math.radians(kat_stopnie)
    
    # OPTYMALIZACJA 1: Liczymy sinus i cosinus tylko raz dla danej próby
    sin_a = math.sin(kat_rad)
    cos_a = math.cos(kat_rad)
    
    # Odległość ze wzoru
    czesc1 = v0 * sin_a
    czesc2 = math.sqrt((v0**2) * (sin_a**2) + 2 * g * h)
    czesc3 = (v0 * cos_a) / g
    
    odleglosc = (czesc1 + czesc2) * czesc3
    
    print(f"Pocisk poleciał na odległość {odleglosc:.2f} m")
    
    if abs(odleglosc - cel) <= 5:
        print(f"\nCel trafiony w {proby} próbach!")
        trafiony = True
    else:
        print("Pudło.")

print("\nGeneruję trajektorię lotu zwycięskiego pocisku...")

x_punkty = []
y_punkty = []
x = 0.0
y = h

# OPTYMALIZACJA 2: Wyciągnięcie stałych współczynników równania paraboli przed pętlę while.
# Dzięki temu skomplikowane dzielenie, potęgowanie i funkcje trygonometryczne wykonają się tylko 1 raz!
wspolczynnik_a = -(g / (2 * (v0**2) * (cos_a**2)))
wspolczynnik_b = math.tan(kat_rad)

# Obliczamy pozycję (x, y) lecącego pocisku co 1 metr, aż do uderzenia w ziemię
krok = 1.0
while y >= 0:
    x_punkty.append(x)
    y_punkty.append(y)
    x += krok
    
    # Zoptymalizowane obliczanie y - to teraz proste równanie kwadratowe y = ax^2 + bx + c
    y = wspolczynnik_a * (x**2) + wspolczynnik_b * x + h

# Dodajemy dokładny punkt końcowy uderzenia
x_punkty.append(odleglosc)
y_punkty.append(0.0)

# Ustawienia wykresu matplotlib
plt.figure(figsize=(10, 5))
plt.plot(x_punkty, y_punkty, color="blue")
plt.axhline(0, color='black') # Linia ziemi
plt.grid(True)
plt.title("Trajektoria zwycięskiego strzału z trebusza")
plt.xlabel("Odległość (m)")
plt.ylabel("Wysokość (m)")

plt.savefig("trajektoria.png")
print("Wykres został zapisany jako plik: trajektoria.png")