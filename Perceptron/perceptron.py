import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Compuerta AND
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
# and
# y = np.array([0, 0, 0, 1])
# or
y = np.array([0, 1, 1, 1])

# Inicialización de los parámetros
w = np.zeros(X.shape[1])
b = 0
lr = 0.1
epochs = 500

# Función de activación escalón  # funciona para or y and
def step(x): 
    return 1 if x >= 0 else 0

# relu # funciona para or y and
def relu(x):
    return np.maximum(0,x)

# sigmoid # funciona para or
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# tanh # funciona para or
def tanh(x):
    return np.tanh(x)

# Algoritmo Perceptrón
fig, ax = plt.subplots()
ax.scatter(X[:,0], X[:,1], c=y)
line, = ax.plot([], [], 'k')
text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

def animate(i):
    global w, b, lr
    for j in range(X.shape[0]):
        #y_pred = step(np.dot(X[j], w) + b)
        #y_pred = relu(np.dot(X[j], w) + b)
        #y_pred = sigmoid(np.dot(X[j], w) + b)
        y_pred = tanh(np.dot(X[j], w) + b)
        w += lr * (y[j] - y_pred) * X[j]
        b += lr * (y[j] - y_pred)

    x_vals = np.array(ax.get_xlim())
    y_vals = (-b - w[0]*x_vals) / w[1]
    line.set_data(x_vals, y_vals)
    text.set_text("Epochs: {}\nWeight: {}\nBias: {}\n\n".format(i+1, w, b))
    return line, text

anim = FuncAnimation(fig, animate, frames=epochs, interval=1, repeat=False)
plt.scatter(X[y==0, 0], X[y==0, 1], c='blue', label='Class 0')
plt.scatter(X[y==1, 0], X[y==1, 1], c='red', label='Class 1')
plt.legend()

plt.show()