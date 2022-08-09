import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score

df = pd.read_csv('dataset.csv')

# Undersample the overrepresented class
# print(df['label'].value_counts())
n = min(df.label.value_counts())
msk = df.groupby('label')['label'].transform('size') >= n
df = pd.concat((df[msk].groupby('label').sample(
    n=n), df[~msk]), ignore_index=True)
print(df['label'].value_counts())


# Split into train and test sets
X = df.drop(columns='label')
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


with open('train.log', 'w+') as log:
    clf = None

    # SVC classifier and confusion matrix validation
    kernels = ['linear', 'rbf', 'sigmoid']
    log.write('{:-^50}'.format(' SVC ') + '\n')
    for deg in range(2, 5):
        clf = SVC(kernel='poly', degree=deg, gamma='auto')
        log.write(
            f'Cross Validation Score: {np.mean(cross_val_score(clf, X, y, cv=5))}\n')
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        pickle.dump(clf, open(os.path.join(
            './models/', f'svc_poly{deg}.sav'), 'wb'))
        log.write(f'Polynomial Degree {deg} \nConfusion: \n{cm}\n')
        log.write(f'Accuracy: {clf.score(X_test, y_test)}\n')

    for k in kernels:
        clf = SVC(kernel=k, gamma='auto')
        log.write(
            f'Cross Validation Score: {np.mean(cross_val_score(clf, X, y, cv=5))}\n')
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        pickle.dump(clf, open(os.path.join(
            './models/', f'svc_{k}.sav'), 'wb'))
        log.write(f'Kernel: {k} \nConfusion: \n{cm}\n')
        log.write(f'Accuracy: {clf.score(X_test, y_test)}\n')

    # Random Forest classifier and confusion matrix validation
    n_estimators = [10, 50, 100, 200, 500]
    log.write('{:-^50}'.format(' Random Forest ') + '\n')
    for n in n_estimators:
        clf = RandomForestClassifier(n_estimators=n)
        log.write(
            f'Cross Validation Score: {np.mean(cross_val_score(clf, X, y, cv=5))}\n')
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        pickle.dump(clf, open(os.path.join(
            'models/', f'rf_n{n}.sav'), 'wb'))
        log.write(f'N_estimators: {n} \nConfusion: \n{cm}\n')
        log.write(f'Accuracy: {clf.score(X_test, y_test)}\n')

    # Decision Tree classifier and confusion matrix validation
    max_depth = [2, 5, 10, 20, 50, 100]
    log.write('{:-^50}'.format(' Decision Tree ') + '\n')
    for d in max_depth:
        clf = DecisionTreeClassifier(max_depth=d)
        log.write(
            f'Cross Validation Score: {np.mean(cross_val_score(clf, X, y, cv=5))}\n')
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        pickle.dump(clf, open(os.path.join(
            './models/', f'dt_depth{d}.sav'), 'wb'))
        log.write(f'Max_depth: {d} \nConfusion: \n{cm}\n')
        log.write(f'Accuracy: {clf.score(X_test, y_test)}\n')

    # Logistic Regression classifier and confusion matrix validation
    log.write('{:-^50}'.format(' Logistic Regression ') + '\n')
    clf = LogisticRegression(max_iter=1000)
    log.write(
        f'Cross Validation Score: {np.mean(cross_val_score(clf, X, y, cv=5))}\n')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    pickle.dump(clf, open(os.path.join(
        './models/', 'lr.sav'), 'wb'))
    log.write(f'Confusion: \n{cm}\n')
    log.write(f'Accuracy: {clf.score(X_test, y_test)}\n')

    # KNN classifier and confusion matrix validation
    log.write('{:-^50}'.format(' KNN ') + '\n')
    clf = KNeighborsClassifier()
    log.write(
        f'Cross Validation Score: {np.mean(cross_val_score(clf, X, y, cv=5))}\n')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    pickle.dump(clf, open(os.path.join(
        './models/', 'knn.sav'), 'wb'))
    log.write(f'Confusion: \n{cm}\n')
    log.write(f'Accuracy: {clf.score(X_test, y_test)}\n')

    # Naive Bayes classifier and confusion matrix validation
    log.write('{:-^50}'.format(' Naive Bayes ') + '\n')
    clf = GaussianNB()
    log.write(
        f'Cross Validation Score: {np.mean(cross_val_score(clf, X, y, cv=5))}\n')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    pickle.dump(clf, open(os.path.join(
        './models/', 'nb.sav'), 'wb'))
    log.write(f'Confusion: \n{cm}\n')
    log.write(f'Accuracy: {clf.score(X_test, y_test)}\n')
