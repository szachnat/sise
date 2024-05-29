import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert data to PyTorch tensors
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.long)
y_test_tensor = torch.tensor(y_test, dtype=torch.long)

# Define a simple feedforward neural network
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size):
        super(NeuralNet, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        
        # Lista modułów warstw ukrytych
        self.hidden_layers = nn.ModuleList()
        
        # Dodawanie warstw ukrytych
        for i, hidden_size in enumerate(hidden_sizes):
            if i == 0:
                self.hidden_layers.append(nn.Linear(input_size, hidden_size))
            else:
                self.hidden_layers.append(nn.Linear(hidden_sizes[i-1], hidden_size))
                self.hidden_layers.append(nn.ReLU())  # Dodanie nieliniowej funkcji aktywacji
        
        # Warstwa wyjściowa liniowa
        self.output_layer = nn.Linear(hidden_sizes[-1], output_size)
    
    def forward(self, x):
        # Przejście przez wszystkie warstwy ukryte
        for layer in self.hidden_layers:
            x = layer(x)
        
        # Warstwa wyjściowa liniowa
        x = self.output_layer(x)
        
        return x

# Parametry modelu
input_size = 4  # Liczba cech wejściowych
hidden_sizes = [10, 20]  # Lista zawierająca liczby neuronów w warstwach ukrytych
output_size = 3  # Liczba klas w problemie Iris

# Inicjalizacja modelu
model = NeuralNet(input_size, hidden_sizes, output_size)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Training loop
num_epochs = 100
train_losses = []
test_losses = []

for epoch in range(num_epochs):
    # Forward pass and loss calculation for training set
    model.train()
    outputs = model(X_train_tensor)
    loss_train = criterion(outputs, y_train_tensor)
    train_losses.append(loss_train.item())
    
    # Backward pass and optimize
    optimizer.zero_grad()
    loss_train.backward()
    optimizer.step()
    
    # Forward pass and loss calculation for test set
    model.eval()
    with torch.no_grad():
        outputs = model(X_test_tensor)
        loss_test = criterion(outputs, y_test_tensor)
        test_losses.append(loss_test.item())
    
    # Print progress (optional)
    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Train Loss: {loss_train.item():.4f}, Test Loss: {loss_test.item():.4f}')

# Plotting the loss curve
plt.figure(figsize=(10, 6))
plt.plot(train_losses, label='Train Loss')
plt.plot(test_losses, label='Test Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Test Loss over Epochs')
plt.legend()
plt.grid(True)
plt.show()

# Plotting the CDF of errors on test set
errors = torch.softmax(outputs, dim=1) - torch.eye(3)[y_test_tensor]
errors = errors.abs().sum(dim=1).numpy()

plt.figure(figsize=(8, 6))
plt.hist(errors, bins=20, density=True, cumulative=True, histtype='step', linewidth=1.5)
plt.xlabel('Error')
plt.ylabel('CDF')
plt.title('Cumulative Distribution Function of Errors on Test Set')
plt.grid(True)
plt.show()
