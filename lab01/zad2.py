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

while not trafiony:
    proby += 1
    try:
        kat_stopnie = float(input("\nPodaj kąt: "))
    except ValueError:
        print("To nie jest prawidłowa liczba")
        continue
    
    kat_rad = math.radians(kat_stopnie)
    
    # odległość ze wzoru
    czesc1 = v0 * math.sin(kat_rad)
    czesc2 = math.sqrt((v0**2) * (math.sin(kat_rad)**2) + 2 * g * h)
    czesc3 = (v0 * math.cos(kat_rad)) / g
    
    odleglosc = (czesc1 + czesc2) * czesc3
    
    print(f"Pocisk poleciał na odległość {odleglosc:.2f}")
    
    if abs(odleglosc - cel) <= 5:
        print(f"\nCel trafiony w {proby} próbach")
        trafiony = True
    else:
        print("Pudło")

print("\nGeneruję trajektorię lotu zwycięskiego pocisku...")

x_punkty = []
y_punkty = []
x = 0
y = h

# Obliczamy pozycję (x, y) lecącego pocisku co 1 metr, aż do uderzenia w ziemię
krok = 1.0
while y >= 0:
    x_punkty.append(x)
    y_punkty.append(y)
    x += krok
    
    # Wzór na trajektorię y(x)
    # y = -(g / (2 * v0^2 * cos^2(a))) * x^2 + (sin(a)/cos(a))*x + h
    czlon1 = -(g / (2 * (v0**2) * (math.cos(kat_rad)**2))) * (x**2)
    czlon2 = math.tan(kat_rad) * x
    y = czlon1 + czlon2 + h

# Dodajemy punkt końcowy uderzenia
x_punkty.append(odleglosc)
y_punkty.append(0)

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