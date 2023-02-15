import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.tree import DecisionTreeClassifier

# Cargar los datos
data = pd.read_csv("simpsons.csv",sep=";")

# Crear el modelo de árbol de decisión
X = data[['Hair Length', 'Weight', 'Age']]
data.head()
y = data['Class']
dtc = DecisionTreeClassifier(criterion="entropy",min_samples_split=4, )
dtc.fit(X, y)

# Predecir la clase de 'Comic'
comic = pd.DataFrame({"Hair Length":[8],"Weight":[290],"Age":[38]})
prediction = dtc.predict(comic)
print("Comic es de género: ", prediction)

plt.figure(figsize=(10,8))
plot_tree(dtc, feature_names=['Hair Length', 'Weight', 'Age'], class_names=dtc.classes_, filled=True)
plt.show()