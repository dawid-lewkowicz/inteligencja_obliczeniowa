import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

df = pd.read_csv("iris_big.csv", sep=",")

numerical_columns = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
korelacja = df[numerical_columns].corr()

print(korelacja) #wyniki bliskie 1 i -1 to silna kierlacja, 0 brak korelacji

pca = PCA(n_components=2)
iris_pca = pca.fit_transform(df[numerical_columns])

df_pca = pd.DataFrame(data=iris_pca, columns=['PC1', 'PC2'])
df_pca['target_name'] = df['target_name']

comp_df = pd.DataFrame(
    pca.components_, 
    columns=numerical_columns, 
    index=['PC1', 'PC2']
)

print("Wpływ poszczególnych cech:")
print(comp_df)

print("Wariancja wyjaśniona przez składowe:", pca.explained_variance_ratio_)

plt.figure(figsize=(8, 6))
colors = {'setosa': 'red', 'versicolor': 'blue', 'virginica': 'green'}

for species, color in colors.items():
    subset = df_pca[df_pca['target_name'] == species]
    plt.scatter(subset['PC1'], subset['PC2'], c=color, label=species, alpha=0.5)

plt.title("Wizualizacja PCA")
plt.xlabel("Petal length")
plt.ylabel("Sepal length")
plt.legend()
plt.grid(True)
plt.show()