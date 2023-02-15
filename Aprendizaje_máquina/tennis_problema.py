import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("tennis.csv",sep=";")
df

#se cambian las variables a numeros
from sklearn import preprocessing
string_to_int= preprocessing.LabelEncoder()                     #encode your data
df=df.apply(string_to_int.fit_transform) #fit and transform it
df

X = df.drop(["Day","PlayTennis"],axis = 1)
X
y = df["PlayTennis"]
y.head()

# perform training 
from sklearn.tree import DecisionTreeClassifier                             
classifier = DecisionTreeClassifier(criterion="entropy", random_state=100)     
classifier.fit(X, y)                                              

D15 = pd.DataFrame({"Outlook":[1],"Humidity":[0],"Wind":[1]})
y_pred = classifier.predict(D15)
print("En el día D15 se jugará tenis?", y_pred)

from sklearn import tree
tree.plot_tree(classifier)
plt.show()