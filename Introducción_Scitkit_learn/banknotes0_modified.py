import csv
import random
from sklearn import metrics
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
import matplotlib.pyplot as plt

# model = Perceptron()
# model = svm.SVC()
# model = KNeighborsClassifier(n_neighbors=1)
model = GaussianNB()

# Read data in from file
with open("banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row[:4]],
            "label": "Authentic" if row[4] == "0" else "Counterfeit"
        })

# Separate data into training and testing groups
holdout = int(0.40 * len(data))
random.shuffle(data)
testing = data[:holdout]
training = data[holdout:]

# Train model on training set
X_training = [row["evidence"] for row in training]
y_training = [row["label"] for row in training]
model.fit(X_training, y_training)

# Make predictions on the testing set
X_testing = [row["evidence"] for row in testing]
y_testing = [row["label"] for row in testing]
predictions = model.predict(X_testing)

# Compute performance metrics
correct = 0
incorrect = 0
total = 0
for actual, predicted in zip(y_testing, predictions):
    total += 1
    if actual == predicted:
        correct += 1
    else:
        incorrect += 1

accuracy = metrics.accuracy_score(y_testing, predictions)
precision = metrics.precision_score(y_testing, predictions, pos_label='Authentic')
negative_predictive_value = metrics.recall_score(y_testing, predictions, pos_label='Counterfeit')
recall = metrics.recall_score(y_testing, predictions, pos_label='Authentic')
specificity = metrics.recall_score(y_testing, predictions, pos_label='Counterfeit')

# Print results
print(f"Results for model {type(model).__name__}")
print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Negative Predictive Value: {negative_predictive_value:.2f}")
print(f"Sensitivity (Recall): {recall:.2f}")
print(f"Specificity: {specificity:.2f}")

cm = confusion_matrix(y_testing, predictions)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)

disp.plot()
plt.show()

