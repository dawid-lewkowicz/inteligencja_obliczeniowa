import datetime
import math

dzis = datetime.date.today()
imie = input("Podaj imię: ")
rok = int(input("Podaj rok urodzenia: "))
miesiąc = int(input("Podaj miesiąc urodzenia: "))
dzień = int(input("Podaj dzień urodzenia: "))
data_urodzenia = datetime.date(rok, miesiąc, dzień)
ilosc_dni = (dzis - data_urodzenia).days

fizyczna_fala = math.sin(((2*math.pi)/23)*ilosc_dni)
emocjonalna_fala = math.sin(((2*math.pi)/28)*ilosc_dni)
intelektualna_fala = math.sin(((2*math.pi)/33)*ilosc_dni)

if (fizyczna_fala < -0.5 and emocjonalna_fala < -0.5) or (fizyczna_fala <-0.5 and intelektualna_fala <-0.5) or (intelektualna_fala < -0.5 and emocjonalna_fala < -0.5):
    fizyczna_fala2 = math.sin(((2*math.pi)/23)*(ilosc_dni+1))
    emocjonalna_fala2 = math.sin(((2*math.pi)/28)*(ilosc_dni+1))
    intelektualna_fala2 = math.sin(((2*math.pi)/33)*(ilosc_dni+1))
    if (fizyczna_fala2 > 0.5 and emocjonalna_fala2 > 0.5) or (fizyczna_fala2 > 0.5 and intelektualna_fala2 > 0.5) or (intelektualna_fala2 > 0.5 and emocjonalna_fala2 > 0.5):
        print(f"{imie}, jest źle ale będzie dobrze")
    else: 
        print(f"{imie}, jest źle i nie będzie lepiej")
elif (fizyczna_fala > 0.5 and emocjonalna_fala > 0.5) or (fizyczna_fala > 0.5 and intelektualna_fala > 0.5) or (intelektualna_fala > 0.5 and emocjonalna_fala > 0.5):
    print(f"{imie}, masz świetny dzień")
else:
    print(f"{imie}, dziś masz umiarkowany dzień :)")

# <20 min