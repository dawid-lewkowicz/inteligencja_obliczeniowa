import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler

df = pd.read_csv("iris_big.csv", sep=",")

# Wybieramy dwie konkretne kolumny do porównania (zgodnie z instrukcją)
cols_to_scale = ['sepal length (cm)', 'sepal width (cm)']
data = df[cols_to_scale]

# 1. Normalizacja Min-Max (skaluje do zakresu [0, 1])
min_max_scaler = MinMaxScaler()
data_min_max = min_max_scaler.fit_transform(data)
df_min_max = pd.DataFrame(data_min_max, columns=cols_to_scale)
df_min_max['target_name'] = df['target_name'].values

# 2. Standaryzacja Z-Score (średnia=0, odchylenie std=1)
z_score_scaler = StandardScaler()
data_z_score = z_score_scaler.fit_transform(data)
df_z_score = pd.DataFrame(data_z_score, columns=cols_to_scale)
df_z_score['target_name'] = df['target_name'].values

# --- WIZUALIZACJA ---
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
colors = {'setosa': 'blue', 'versicolor': 'orange', 'virginica': 'green'}

def plot_data(ax, data_plot, title):
    for species, color in colors.items():
        subset = data_plot[data_plot['target_name'] == species]
        ax.scatter(subset[cols_to_scale[0]], subset[cols_to_scale[1]], 
                   c=color, label=species, alpha=0.5)
    ax.set_title(title)
    ax.set_xlabel(cols_to_scale[0])
    ax.set_ylabel(cols_to_scale[1])
    ax.legend()
    ax.grid(True)

# Rysowanie trzech wersji
plot_data(axes[0], df, "Oryginalne dane")
plot_data(axes[1], df_min_max, "Normalizacja Min-Max (0-1)")
plot_data(axes[2], df_z_score, "Skalowanie Z-Score (Mean=0, Std=1)")

plt.tight_layout()
plt.show()

# --- ANALIZA STATYSTYCZNA ---
print("Statystyki dla Min-Max:")
print(df_min_max[cols_to_scale].agg(['min', 'max', 'mean', 'std']))

print("\nStatystyki dla Z-Score:")
print(df_z_score[cols_to_scale].agg(['min', 'max', 'mean', 'std']).round(4))


################################################################################

#Stwórz wykresy z irysami jako punktami na wykresie, dla dwóch zmiennych: sepal length i sepal width. Klasy irysów
#oznaczone są w legendzie wykresu. Zrób wykres w trzech wersjach: dane oryginalne, znormalizowane min-max i
#zeskalowane z-scorem.