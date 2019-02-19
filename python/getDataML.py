import numpy as np
import time
import getDataset as gds

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.linear_model import LinearRegression

###處理資料集
#將資料集設定成ndarray
dataset = gds.getdata()
dataset["data"] = np.array(dataset["data"])
dataset["target"] = np.array(dataset["target"])
dataset["feature_name"] = np.array(dataset["feature_name"])

###匯出資料集
np.set_printoptions(threshold=np.inf)
with open("dataset.txt", "w") as f:
     f.write(str(dataset))

###機器學習
#分割訓練集與測試集
X = dataset["data"]
y = dataset["target"]
X_train, X_test, y_train, y_test = \
         train_test_split(X, y, test_size=0.2, random_state=0)

#建立預測模型
print("開始建立預測模型...")
time.sleep(2)
reg = LinearRegression()
predicted = cross_val_predict(reg, X, y, cv=10)
reg.fit(X_train, y_train)
accuracy_train = reg.score(X_train, y_train)
accuracy_test = reg.score(X_test, y_test)
predict_y = reg.predict(X_test)
time.sleep(1)
print("建立完成")
print()
time.sleep(2)
print("訓練集預測分數為 %s" % (accuracy_train))
print("測試集預測分數為 %s" % (accuracy_test))

#畫出預測成果
plt.scatter(predicted,y,s=2)
plt.plot(predict_y, predict_y, 'ro')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.xlabel('Predicted')
plt.ylabel('Measured')
plt.show()

###定義機器學習執行函式
def ML(newData):
    newy = np.array(newData["data"])
    new_predict = reg.predict(newy.reshape(1, -1))
    newData["describe"] = "預測結果"
    newData["data"] = list(new_predict)
    return newData
