import csv
import tensorflow as tf
import pandas as pd

from sklearn.model_selection import train_test_split

# Read data in from file
with open("banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row[:4]],
            "label": 1 if row[4] == "0" else 0
        })


# Dividir datos en entrenamiento y prueba
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Separate data into training and testing groups
evidence = [row["evidence"] for row in data]
labels = [row["label"] for row in data]
X_training, X_testing, y_training, y_testing = train_test_split(
    evidence, labels, test_size=0.4
)

# Create a neural network
model = tf.keras.models.Sequential()

# Add a hidden layer with 8 units, with ReLU activation
model.add(tf.keras.layers.Dense(8, input_shape=(4,), activation="tanh"))

# Add output layer with 1 unit, with sigmoid activation
model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

# Train neural network
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)
model.fit(X_training, y_training, epochs=20)

# Evaluate how well model performs
model.evaluate(X_testing, y_testing, verbose=2)


# Read data in from file
data_house = pd.read_excel('house_price_label.xlsx', sheet_name='house_price_lebel_raw')

data_house_list = []
for i, row in data_house.iterrows():
    data_dict = {
        "evidence": [row['bedroom'], row['bathroom'], row['built_in'], row['lot_size'], row['area'], row['price']],
        "label": row['is_single']
    }
    data_house_list.append(data_dict)


# Dividir datos en entrenamiento y prueba
train_data_h, test_data_h = train_test_split(data_house_list, test_size=0.2, random_state=42)


# Separate data into training and testing groups
evidence = [row["evidence"] for row in data_house_list]
labels = [row["label"] for row in data_house_list]
X_training_h, X_testing_h, y_training_h, y_testing_h = train_test_split(
    evidence, labels, test_size=0.4
)

model_h = tf.keras.models.Sequential([
    tf.keras.layers.Dense(10, activation = 'relu', input_shape=(6,)),
    tf.keras.layers.Dense(5,  activation = 'tanh'),
    tf.keras.layers.Dense(1,  activation = 'sigmoid')
])

# Train neural network
model_h.compile(
    optimizer = "sgd",
    loss      = "binary_crossentropy",
    metrics   = ["accuracy"]
)
model_h.fit(X_training_h, y_training_h, epochs=20)

# Evaluate how well model performs
model_h.evaluate(X_testing_h, y_testing_h, verbose=2)
