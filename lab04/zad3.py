import torch
import torch.nn as nn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, precision_score

df = pd.read_csv("diagnosis.csv")

X = torch.tensor(df.drop("diagnosis", axis=1).values, dtype=torch.float32)
y = torch.tensor(df["diagnosis"].values, dtype=torch.long)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=301575)

model = nn.Sequential(
    nn.Linear(3, 8), 
    nn.ReLU(), 
    nn.Linear(8, 4), 
    nn.ReLU(), 
    nn.Linear(4, 2)
)

optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()

train_losses, val_losses, train_accs, val_accs = [], [], [], []

for tura in range(100):
    model.train()
    optimizer.zero_grad()
    
    out = model(X_train)
    loss = criterion(out, y_train)
    loss.backward()
    optimizer.step()
    
    train_losses.append(loss.item())
    acc_t = (out.argmax(1) == y_train).float().mean().item()
    train_accs.append(acc_t)

    model.eval()
    with torch.no_grad():
        out_v = model(X_val)
        val_loss = criterion(out_v, y_val)
        val_losses.append(val_loss.item())
        acc_v = (out_v.argmax(1) == y_val).float().mean().item()
        val_accs.append(acc_v)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.plot(train_losses, label="Trening"); ax1.plot(val_losses, label="Walidacja")
ax1.set_title("Loss (Błąd)"); ax1.legend()
ax2.plot(train_accs, label="Trening"); ax2.plot(val_accs, label="Walidacja")
ax2.set_title("Accuracy (Celność)"); ax2.legend()
plt.tight_layout()
plt.show()

model.eval()
with torch.no_grad():
    logits = model(X_val)
    probs = torch.softmax(logits, dim=1)
    
    preds = logits.argmax(1)

print(f"Accuracy: {accuracy_score(y_val, preds)}")
print(f"Precision: {precision_score(y_val, preds)}")
print(f"Recall: {recall_score(y_val, preds)}")

print("\nConfusion Matrix:")
cm_df = pd.DataFrame(
    confusion_matrix(y_val, preds), 
    index=["Faktycznie Zdrowy", "Faktycznie Chory"], 
    columns=["Pred: Zdrowy", "Pred: Chory"]
)
print(cm_df)

custom_threshold = 0.2
preds_safe = (probs[:, 1] > custom_threshold).long()

print(f"\nRecall przy progu {custom_threshold}: {recall_score(y_val, preds_safe)}")