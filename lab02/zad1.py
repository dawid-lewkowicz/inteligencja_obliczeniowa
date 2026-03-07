import pandas as pd

df = pd.read_csv("iris_big_with_errors.csv", sep=",")

df.columns = df.columns.str.strip().str.replace('"', '')
df['target_name'] = df['target_name'].str.strip().str.replace('"', '')
print(df.columns)



print(df.isna().sum())
print(f"suma niepełnych rekordów: {df.isna().sum().sum()}")



numerical_columns = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
for column in numerical_columns:
    df[column] = pd.to_numeric(df[column], errors='coerce') #nieliczbowe dane zmieniane sa na NaN

for column in numerical_columns:
    mediana = df[column].median()
    df.loc[(df[column] <= 0) | (df[column] >= 15) | (df[column].isna()), column] = mediana #podstawianie mediany



df['target_name'] = df['target_name'].str.lower().str.strip().str.replace('"', '')

def fix_name(name):
    if pd.isna(name): return df['target_name'].mode()[0] # mode() daje dominantę
    if 'seto' in name: return 'setosa'
    if 'versi' in name: return 'versicolor'
    if 'virgi' in name: return 'virginica'
    return df['target_name'].mode()[0]

df['target_name'] = df['target_name'].apply(fix_name)