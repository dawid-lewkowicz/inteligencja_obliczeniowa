import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

df = pd.read_csv("iris_big.csv")

wartosci = df.iloc[:, 0:4].values
nazwa = df.iloc[:, 4].values

pytanie_treningowe, pytanie_test, odpowiedz_treningowa, odpowiedz_test = train_test_split(wartosci, nazwa, test_size=0.3, random_state=301575)

#print("Treningowy :\n", pytanie_treningowe)
#print("Testowy :\n", pytanie_test)

drzewo = DecisionTreeClassifier(max_depth=4, random_state=301575)

drzewo.fit(pytanie_treningowe, odpowiedz_treningowa)

odpowiedz_predykcyjna = drzewo.predict(pytanie_test)

accuracy = accuracy_score(odpowiedz_test, odpowiedz_predykcyjna)
print(f"Accuracy: {accuracy * 100:.2f}%")

cm = confusion_matrix(odpowiedz_test, odpowiedz_predykcyjna)

plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', 
            xticklabels=drzewo.classes_, yticklabels=drzewo.classes_)
plt.title("Macierz Błędów - Drzewo Decyzyjne")
plt.xlabel("Przewidziany Gatunek")
plt.ylabel("Rzeczywisty Gatunek")
plt.show()