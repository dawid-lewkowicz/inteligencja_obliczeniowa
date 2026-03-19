import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("iris_big.csv")

(train_set, test_set) = train_test_split(df.values, train_size=0.7, random_state=301575)

def classify_iris(sepal_length, sepal_width, petal_length, petal_width):
    if petal_length < 2.5:
        return "setosa"
    elif petal_length < 4.8:
        return "versicolor"
    else:
        return "virginica"

good_predictions = 0

ilosc_testowa = test_set.shape[0] #liczba rekordów w zbiorze testowym

for i in range(ilosc_testowa):
    if classify_iris(test_set[i, 0], test_set[i, 1], test_set[i, 2], test_set[i, 3]) == test_set[i, 4]:
        good_predictions = good_predictions + 1 

print("Zgadnięte irysy:", good_predictions)
print("Accuracy:", (good_predictions / ilosc_testowa) * 100, "%")