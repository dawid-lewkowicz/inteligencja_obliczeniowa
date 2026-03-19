import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

df = pd.read_csv("iris_big.csv")
wartosci = df.iloc[:, 0:4].values
nazwa = df.iloc[:, 4].values

pytanie_treningowe, pytanie_test, odpowiedz_treningowa, odpowiedz_test = train_test_split(wartosci, nazwa, test_size=0.3, random_state=301575)

classifiers = {
    "Drzewo Decyzyjne": DecisionTreeClassifier(max_depth=4, random_state=301575),
    "k-NN (k=3)": KNeighborsClassifier(n_neighbors=3),
    "k-NN (k=5)": KNeighborsClassifier(n_neighbors=5),
    "k-NN (k=11)": KNeighborsClassifier(n_neighbors=11),
    "Naive Bayes": GaussianNB(),
    "Sieć Neuronowa": MLPClassifier(max_iter=1000, random_state=301575) 
}

results = {}

for name, classifier in classifiers.items():
    classifier.fit(pytanie_treningowe, odpowiedz_treningowa)
    
    odpowiedz_predykcyjna = classifier.predict(pytanie_test)
    
    acc = accuracy_score(odpowiedz_test, odpowiedz_predykcyjna)
    results[name] = acc
    
    cm = confusion_matrix(odpowiedz_test, odpowiedz_predykcyjna)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Purples',
                xticklabels=classifier.classes_, yticklabels=classifier.classes_)
    plt.title(f"Macierz Błędów: {name}")
    plt.xlabel("Przewidziany Gatunek")
    plt.ylabel("Rzeczywisty Gatunek")
    plt.show()

print("Dokładność klasyfikatorów")
for name, acc in results.items():
    print(f"{name}: {acc * 100:.2f}%")