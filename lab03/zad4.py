import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

df = pd.read_csv("diagnosis.csv")

wawrtosci = df.iloc[:, 0:3].values
rezultat = df.iloc[:, 3].values

okno_wykresu = plt.figure(figsize=(10, 8))
wykres_3d = okno_wykresu.add_subplot(111, projection='3d')

zdrowi = df[df.iloc[:, 3] == 0]
chorzy = df[df.iloc[:, 3] == 1]

wykres_3d.scatter(zdrowi.iloc[:, 0], zdrowi.iloc[:, 1], zdrowi.iloc[:, 2], c='blue', label='Zdrowy (0)', alpha=0.6)
wykres_3d.scatter(chorzy.iloc[:, 0], chorzy.iloc[:, 1], chorzy.iloc[:, 2], c='red', label='Chory (1)', alpha=0.6)

wykres_3d.set_xlabel('Parametr 1')
wykres_3d.set_ylabel('Parametr 2')
wykres_3d.set_zlabel('Parametr 3')
wykres_3d.set_title('Diagnoza: Wizualizacja pacjentów 3D')
wykres_3d.legend()
plt.show()

pytania_trening, pytania_test, odpowiedzi_trening, odpowiedzi_test = train_test_split(wawrtosci, rezultat, test_size=0.3, random_state=13)

classifiers = {
    "Drzewo Decyzyjne": DecisionTreeClassifier(max_depth=4, random_state=301575),
    "3-NN": KNeighborsClassifier(n_neighbors=3),
    "5-NN": KNeighborsClassifier(n_neighbors=5),
    "11-NN": KNeighborsClassifier(n_neighbors=11),
    "Naive Bayes": GaussianNB(),
    "Sieć Neuronowa": MLPClassifier(max_iter=1000, random_state=301575) 
}

for name, klasyfikator in classifiers.items():
    klasyfikator.fit(pytania_trening, odpowiedzi_trening)
    y_pred = klasyfikator.predict(pytania_test)
    
    acc = accuracy_score(odpowiedzi_test, y_pred)
    prec = precision_score(odpowiedzi_test, y_pred, zero_division=0) 
    rec = recall_score(odpowiedzi_test, y_pred, zero_division=0)
    
    print(f"\n {name}")
    print(f"Accuracy: {acc:.2f}")
    print(f"Precision: {prec:.2f}")
    print(f"Sensitivity: {rec:.2f}")
    
    cm = confusion_matrix(odpowiedzi_test, y_pred)
    plt.figure(figsize=(4, 3))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', 
                xticklabels=['Zdrowy', 'Chory'], yticklabels=['Zdrowy', 'Chory'])
    plt.title(f'Macierz błędów: {name}')
    plt.ylabel('Prawdziwy Stan')
    plt.xlabel('Przewidywanie Modelu')
    plt.show()

#accuracy -> stosunek poprawnych diagnoz
#precision -> ilosc realnie chorych jednostek sposrod uznanych za chorych
#sensivity -> ilu z realnie chorych zostalo uznanych za chorych, NAJWAŻNIEJSZY

#nie, 100zdrowych i 1 chory, algorytm bedzie dawal wszystkim ze sa zdrowi