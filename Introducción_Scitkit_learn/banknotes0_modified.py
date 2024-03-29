import csv
import random
from sklearn import metrics
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_auc_score, roc_curve
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score

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

#5-fold cross validation
accuracies = cross_val_score(model, X_training, y_training, cv=5)

print(f"Accuracy for each fold: {accuracies}")
print(f"Average accuracy: {accuracies.mean()}")

# matriz de confusion
cm = confusion_matrix(y_testing, predictions, labels=model.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)

disp.plot()
plt.show()

# roc and auc
fpr, tpr, thresholds = roc_curve(y_testing, model.predict_proba(X_testing)[:, 1], pos_label="Authentic")

roc_auc = roc_auc_score(y_testing, model.predict_proba(X_testing)[:, 1], labels="Authentic")
print(f"AUC: {roc_auc:.2f}")

plt.plot(fpr, tpr, color='darkorange', label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.ylabel('1-Specificity')
plt.xlabel('1-Sensitivity')
plt.title(f'ROC Curve of Model {type(model).__name__}')
plt.legend(loc="lower right")
plt.show()