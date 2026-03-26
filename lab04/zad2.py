import torch
import torch.nn as nn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

df = pd.read_csv("iris_big.csv")

labels = LabelEncoder().fit_transform(df["target_name"]) 

X = torch.tensor(df.drop("target_name", axis=1).values, dtype=torch.float32)
y = torch.tensor(labels, dtype=torch.long)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=301575)

srednia = X_train.mean(dim=0)
odchylenie_standardowe = X_train.std(dim=0)
X_train = (X_train - srednia) / odchylenie_standardowe
X_val = (X_val - srednia) / odchylenie_standardowe

model = nn.Sequential(
    nn.Linear(4, 12), 
    nn.ReLU(), 
    nn.Linear(12, 6), 
    nn.ReLU(), 
    nn.Linear(6, 3)
)

optimizer = torch.optim.Adam(model.parameters(), lr=0.01) # sprawdzaie wyników
criterion = nn.CrossEntropyLoss()

train_losses, val_losses, train_accs, val_accs = [], [], [], []

for epoch in range(100):
    model.train()
    optimizer.zero_grad()

    przepuszczone_dane = model(X_train)
    wynik_porównania = criterion(przepuszczone_dane, y_train)

    wynik_porównania.backward()
    optimizer.step() #aktualizajca wag
    
    train_losses.append(wynik_porównania.item())
    
    prediction_train = przepuszczone_dane.argmax(dim=1)
    accuracy_train = (prediction_train == y_train).float().mean().item()
    train_accs.append(accuracy_train)

    model.eval() #zakaz wprowadzania zmian w wagach
    with torch.no_grad():
        out_val = model(X_val)
        val_loss = criterion(out_val, y_val)
        
        val_losses.append(val_loss.item())

        preds_val = out_val.argmax(dim=1)
        acc_val = (preds_val == y_val).float().mean().item()
        val_accs.append(acc_val)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.plot(train_losses, label="Trening")
ax1.plot(val_losses, label="Walidacja")
ax1.set_title("Funkcja Straty (Loss)")
ax1.legend()

ax2.plot(train_accs, label="Trening")
ax2.plot(val_accs, label="Walidacja")
ax2.set_title("Dokładność (Accuracy)")
ax2.legend()
plt.tight_layout()
plt.savefig("krzywe.png")
plt.show()

model.eval()
with torch.no_grad():
    final_out = model(X_val)
    final_preds = final_out.argmax(dim=1)

final_acc = (final_preds == y_val).float().mean().item()
print(f"Accuracy: {final_acc}")

classes = ["setosa", "versicolor", "virginica"]
print("\nConfusion Matrix:")
print(pd.DataFrame(confusion_matrix(y_val.numpy(), final_preds.numpy()), index=classes, columns=classes))