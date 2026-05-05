import pandas as pd
from sklearn import tree
import pydot
import io
import os

os.chdir("C:\\Users\\ADMIN\\Desktop\\Trainings\\AI Batch_March\\3. ML\\data_source")
#creation of data frames from csv
titanic_train = pd.read_csv('train.csv')
print(titanic_train.info())

#want to build model on only selected features.
features = ['Pclass', 'Parch' , 'SibSp']

X_train = titanic_train[['Pclass', 'Parch' , 'SibSp']]
y_train = titanic_train['Survived']


#create an instance of decision tree classifier type
classifer = tree.DecisionTreeClassifier()

print(type(classifer))

#learn the pattern automatically
classifer.fit(X_train, y_train)


#get the logic or model learned by Algorithm
#issue: not readable
print(classifer.tree_)

os.chdir("C:\\Users\\ADMIN\\Desktop\\Trainings\\AI Batch_March\\3. ML\\data_source\\submissions")
#get the readable tree structure from tree_ object
#visualize the deciion tree
dot_data = io.StringIO() 
tree.export_graphviz(classifer, out_file = dot_data, feature_names = X_train.columns)
graph = pydot.graph_from_dot_data(dot_data.getvalue())[0] 
graph.write_pdf("tree_011.pdf")


#read test data
os.chdir("C:\\Users\\ADMIN\\Desktop\\Trainings\\AI Batch_March\\3. ML\\data_source")
titanic_test = pd.read_csv("test.csv")
print(titanic_test.info())
features = ['Pclass', 'Parch' , 'SibSp']
X_test = titanic_test[features]
titanic_test['Survived'] = classifer.predict(X_test)

os.chdir("C:\\Users\\ADMIN\\Desktop\\Trainings\\AI Batch_March\\3. ML\\data_source\\submissions")
titanic_test.to_csv("submission_tree_ml_011.csv", columns=["PassengerId", "Survived"], index=False)



