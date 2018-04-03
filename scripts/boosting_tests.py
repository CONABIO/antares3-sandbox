from lightgbm import LGBMClassifier
from xgboost.sklearn import XGBClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

X, y = make_classification(n_samples=10000, n_features=10,
                           n_classes=5, n_informative=6)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)


## Lightgbm
lgb = LGBMClassifier(n_estimators=50,
                     max_depth=30,
                     learning_rate=0.1,
                     reg_alpha=0,
                     reg_lambda=0,
                     # objective='binary',
                     n_jobs=-1)

lgb.fit(X_train, y_train)
y_pred = lgb.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print('Lightboost:')
print(y_pred)
print(acc)


## Xgboost
xgb = XGBClassifier(n_estimators=50,
                     max_depth=30,
                     learning_rate=0.1,
                     reg_alpha=0,
                     reg_lambda=1,
                     objective='multi:softmax',
                     # objective='binary:logistic',
                     n_jobs=-1)

xgb.fit(X_train, y_train)
y_pred = xgb.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print('xgboost:')
print(y_pred)
print(acc)
