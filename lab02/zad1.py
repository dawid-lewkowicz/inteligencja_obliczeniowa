import pandas as pd

df = pd.read_csv("iris_big.csv", sep=",")
print(df.columns)

print(df.isna().sum())

print(f"suma niepełnych rekordów: {df.isna().sum().sum()}")

#mediana_sepal_length = df["sepal length (cm)"].median()

#print(mediana_sepal_length)

is_in_range = (df > 0 ) & (df < 15)
print(is_in_range.all().all())