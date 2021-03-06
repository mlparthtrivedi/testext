# -*- coding: utf-8 -*-
#Import Necessary Libraries
import numpy as np
import pandas as pd

#visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

#ignore warnings
import warnings
warnings.filterwarnings('ignore')

#Read in and Explore the Data
data = pd.read_csv("new.csv")
train=data.sample(frac=0.8,random_state=200)
test=data.drop(train.index)

features_details = train.describe(include = "all");
nan_value_detail = pd.isnull(train).sum();

#Data Visualization

#draw a bar plot of output by pregnant_count
sns.barplot(x="pregnant_count", y="output", data=train)
for i in range(1,16):
  print("Percentage of pregnant_count who has ",i," output:", train["output"][train["pregnant_count"] == i].value_counts(normalize = True)[1]*100)

#draw a bar plot of output byPlasma glucose concentration
sns.factorplot(x="output", y="Plasma glucose concentration", data=train)
sns.FacetGrid(train, col="output").map(sns.distplot, "Plasma glucose concentration")

#draw a bar plot of output BP
sns.factorplot(x="output", y="BP", data=train)
sns.FacetGrid(train, col="output").map(sns.distplot, "BP")

#draw a bar plot of output Triceps skinfold thickness
sns.factorplot(x="output", y="Triceps skinfold thickness", data=train)
sns.FacetGrid(train, col="output").map(sns.distplot, "Triceps skinfold thickness")

#2-Hour serum insulin
#draw a bar plot of output Triceps skinfold thickness
sns.factorplot(x="output", y="2-Hour serum insulin", data=train)
sns.FacetGrid(train, col="output").map(sns.distplot, "2-Hour serum insulin")

#draw a bar plot of output BMI
sns.factorplot(x="output", y="BMI", data=train)
sns.FacetGrid(train, col="output").map(sns.distplot, "BMI")

#draw a bar plot of output Diabetes pedigree function
sns.factorplot(x="output", y="Diabetes pedigree function", data=train)
sns.FacetGrid(train, col="output").set(xticks=[0,0.2,0.4,0.6,0.8,1], yticks=[0,1]).map(sns.distplot, "Diabetes pedigree function")

#draw a bar plot of output BMI
sns.factorplot(x="output", y="Age", data=train)
sns.FacetGrid(train, col="output").map(sns.distplot, "Age")
#sort the ages into logical categories
train["Age"] = train["Age"].fillna(-0.5)
test["Age"] = test["Age"].fillna(-0.5)
bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
labels = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior']
train['AgeGroup'] = pd.cut(train["Age"], bins, labels = labels)
test['AgeGroup'] = pd.cut(test["Age"], bins, labels = labels)
#draw a bar plot of Age vs. survival
sns.barplot(x="AgeGroup", y="output", data=train)
plt.show()


#data cleaning
#map each Age value to a numerical value
age_mapping = {'Baby': 1, 'Child': 2, 'Teenager': 3, 'Student': 4, 'Young Adult': 5, 'Adult': 6, 'Senior': 7}
train['AgeGroup'] = train['AgeGroup'].map(age_mapping)
test['AgeGroup'] = test['AgeGroup'].map(age_mapping)
#dropping the Age feature for now, might change
train = train.drop(['Age'], axis = 1)
test = test.drop(['Age'], axis = 1)


#choose model
from sklearn.model_selection import train_test_split
x = train.drop(['output'], axis=1)
y = train["output"]
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size = 0.22, random_state = 0)

    
# Gaussian Naive Bayes
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
gaussian = GaussianNB()
gaussian.fit(x_train, y_train)
y_pred = gaussian.predict(x_val)
acc_gaussian = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_gaussian)
    
# Logistic Regression
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
logreg.fit(x_train, y_train)
y_pred = logreg.predict(x_val)
acc_logreg = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_logreg)

# Support Vector Machines
from sklearn.svm import SVC
svc = SVC()
svc.fit(x_train, y_train)
y_pred = svc.predict(x_val)
acc_svc = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_svc)

#Decision Tree
from sklearn.tree import DecisionTreeClassifier
decisiontree = DecisionTreeClassifier()
decisiontree.fit(x_train, y_train)
y_pred = decisiontree.predict(x_val)
acc_decisiontree = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_decisiontree)

# Random Forest
from sklearn.ensemble import RandomForestClassifier
randomforest = RandomForestClassifier()
randomforest.fit(x_train, y_train)
y_pred = randomforest.predict(x_val)
acc_randomforest = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_randomforest)

# KNN or k-Nearest Neighbors
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(x_train, y_train)
y_pred = knn.predict(x_val)
acc_knn = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_knn)


# Stochastic Gradient Descent
from sklearn.linear_model import SGDClassifier
sgd = SGDClassifier()
sgd.fit(x_train, y_train)
y_pred = sgd.predict(x_val)
acc_sgd = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_sgd)

# Gradient Boosting Classifier
from sklearn.ensemble import GradientBoostingClassifier
gbk = GradientBoostingClassifier()
gbk.fit(x_train, y_train)
y_pred = gbk.predict(x_val)
acc_gbk = round(accuracy_score(y_pred, y_val) * 100, 2)
print(acc_gbk)

models = pd.DataFrame({
    'Model': ['Support Vector Machines', 'KNN', 'Logistic Regression', 
              'Random Forest', 'Naive Bayes', 
              'Decision Tree', 'Stochastic Gradient Descent', 'Gradient Boosting Classifier'],
    'Score': [acc_svc, acc_knn, acc_logreg, 
              acc_randomforest, acc_gaussian, acc_decisiontree,
              acc_sgd, acc_gbk]})
models.sort_values(by='Score', ascending=False)


#kfold cross validation
from sklearn.model_selection import cross_val_score
rf = RandomForestClassifier(n_estimators=100)
scores = cross_val_score(rf, x_train, y_train, cv=10, scoring = "accuracy")
print("Scores:", scores)
print("Mean:", scores.mean())
print("Standard Deviation:", scores.std())


#features minify
importances = pd.DataFrame({'feature':x_train.columns,'importance':np.round(randomforest.feature_importances_,3)})
importances = importances.sort_values('importance',ascending=False).set_index('feature')
importances.head(15)
importances.plot.bar()

#saleprice correlation matrix
k = 10 #number of variables for heatmap
corrmat = data.corr()
cols = corrmat.nlargest(k, 'output')['output'].index
cm = np.corrcoef(data[cols].values.T)
sns.set(font_scale=1.25)
hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
plt.show()


#obb score (out of bag score)
#print("oob score:", round(random_forest.oob_score_, 4)*100, "%")


#confusion metrix
'''from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
predictions = cross_val_predict(random_forest, x_train_def, y_train_def, cv=3)
CM = confusion_matrix(y_train_def, predictions)
#precision and recall
from sklearn.metrics import precision_score, recall_score
print("Precision:", precision_score(y_train_def, predictions))
print("Recall:",recall_score(y_train_def, predictions))
#f1 score
from sklearn.metrics import f1_score
f1_score(y_train_def, predictions)'''