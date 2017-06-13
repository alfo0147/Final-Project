import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.externals.six import StringIO
from sklearn import tree
import pydotplus
from IPython.display import Image
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

data = pd.read_csv(r'C:\Users\User\Desktop\moviedata\yujindata.csv', encoding = 'CP949')
data = data.drop(['영화명', '최종관객수'],1) # 필요없는 data 삭제

X = np.array(data.iloc[:,1:]) # input
y = np.array(data['Target']) # output

# SVM parameter setting
# 5-fold CV
C = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 1, 10, 100]
g = [0.01,0.1,1]
sk_fold = StratifiedKFold(n_splits=5, shuffle=True)
for param_c in C:
    for param_g in g:
        clf_svm = SVC(kernel='rbf', C=param_c, gamma=param_g)
        tmp = []
        for tr, te in sk_fold.split(X,y):
            clf_svm.fit(X[tr], y[tr])
            acc = clf_svm.score(X[te], y[te])
            tmp.append(acc)
            avg_acc = np.mean(np.array(acc))

# SVM modeling (C=10, gamma=0.01)
X_tr, X_te, Y_tr, Y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=100)

clf_svm = SVC(kernel='rbf', C=10, gamma=0.01)
clf_svm.fit(X_tr, Y_tr)
SVC_pred = clf_svm.predict(X_te)
confusion_matrix(Y_te, SVC_pred)
clf_svm.score(X_te, Y_te)
print(classification_report(Y_te, SVC_pred))


# Logistic Regression parameter setting
# 5-fold CV
sk_fold=StratifiedKFold(n_splits=5)

C=[0.01,0.1,1,10,100,1000]
acc=[]
for param_c in C:
    clf_lr=LogisticRegression(multi_class='multinomial',solver='lbfgs', C=param_c)
    temp=[]
    for tr, te in sk_fold.split(X,y):
        clf_lr.fit(X[tr], y[tr])
        acc = clf_lr.score(X[te], y[te])
        tmp.append(acc)
        avg_acc = np.mean(np.array(acc))

# logistic Regression modeling (C=10)
X_tr, X_te, Y_tr, Y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=100)

clf_lr = LogisticRegression(multi_class='multinomial',solver='lbfgs', C=10)
clf_lr.fit(X_tr, Y_tr)
LR_pred = clf_lr.predict(X_te)
confusion_matrix(Y_te, LR_pred)
clf_lr.score(X_te, Y_te)
print(classification_report(Y_te, LR_pred))


# DT parameter setting
# 5-fold CV
max_depth=[5, 10]
min_samples_split=[10, 20, 50]
min_samples_leaf=[50, 100]

acc=[]
for depth in max_depth:
    for split in min_samples_split:
        for leaf in min_samples_leaf:
            clf_tree=DecisionTreeClassifier(max_depth=depth, min_samples_split=split, min_samples_leaf=leaf)
            temp = []
            for tr, te in sk_fold.split(X,y):
                clf_tree.fit(X[tr], y[tr])
                acc = clf_tree.score(X[te], y[te])
                tmp.append(acc)
                avg_acc = np.mean(np.array(acc))

# DT modeling (max_depth=10, min_samples_split=50, min_samples_leaf=50)
clf_tree=DecisionTreeClassifier(max_depth=10, min_samples_split=50, min_samples_leaf=50)
clf_tree.fit(X_tr, Y_tr)
DT_pred = clf_tree.predict(X_te)
confusion_matrix(Y_te, DT_pred)
clf_tree.score(X_te, Y_te)
print(classification_report(Y_te, DT_pred))

# DT plot
dot_file=StringIO()
tree.export_graphviz(clf_tree, out_file=dot_file)
tree.export_graphviz(clf_tree, out_file=dot_file, filled=True)

dot_file.getvalue()

graph=pydotplus.graph_from_dot_data(dot_file.getvalue())
graph[-1].write_pdf(r'C:\Users\User\Desktop\moviedata\tree.pdf')
Image(graph[1].create_png())
