import json
import time

###定義函數供其他程式使用
def help():
    print("此模組可用函式如下:\ngetdata(what=dataset)")

def getdata(what="dataset"): 
    if what == "dataset":
        return dataset
    elif what == "data":
        return data
    elif what == "count":
        return tmp
    else:
        print("error , wrong type or wrong value")
        return None

#直接讀取json檔
dataSrc = "FarmTransData.json"
with open(dataSrc, encoding = "utf-8") as f:
    dataJson = json.load(f)

#用於存放處理後資料
data_1 = []                                              #當日交易量
data_2 = []                                              #當日上價
data_3 = []                                              #當日中價
data_4 = []                                              #當日下價
data_5 = []                                              #當日平均價

#篩選資料
tmp = 0                                                  #計數器
count = len(dataJson)                                    #計算共有幾筆資料
for i in range(count, 0, -1):                            #過濾沒有交易的項目
    if dataJson[i-1]["交易量"] and dataJson[i-1]["上價"]\
    and dataJson[i-1]["中價"] and dataJson[i-1]["下價"]\
    and dataJson[i-1]["平均價"] != 0.0 and\
    "蘋果-" in dataJson[i-1]["作物名稱"]:
        data_1.append(dataJson[i-1]["交易量"])           #將目標資料存放到串列
        data_2.append(dataJson[i-1]["上價"])
        data_3.append(dataJson[i-1]["中價"])
        data_4.append(dataJson[i-1]["下價"])
        data_5.append(dataJson[i-1]["平均價"])
        tmp += 1                                         #計數器

#確認特徵資料蒐集正確
a = len(data_1)
b = len(data_2)
c = len(data_3)
d = len(data_4)
e = len(data_5)
if a == b == c == d == e:
    print("資料特徵蒐集成功")
    time.sleep(3)
else:
    print("警告，資料特徵蒐集失敗")


###整合各項特徵，製作資料集(用於機器學習)    
#把資料拆分後整合為"每筆資料多特徵"(原為"每個特徵多筆資料")

#定義資料集變數
dataset = {"data":None, "target":None, "feature_name":None, "doc":None}
data = [[0 for j in range(4)] for i in range(tmp)]
target = [0 for i in range(tmp)]

#整合各項特徵
for i in range (0, tmp):
    data[i][0] = data_1[i]                               #當日交易量
    data[i][1] = data_2[i]                               #當日上價
    data[i][2] = data_3[i]                               #當日中價
    data[i][3] = data_4[i]                               #當日下價
#預測目標
    target[i] = data_5[i] * data_1[i]                    #當日收入(平均價*交易量)

#特徵名稱
feature_name = ["當日交易量", "當日上價", "當日中價", "當日下價"]
        
#讀取說明資料
with open("doc.txt", "r") as doc:
    doc = doc.read()
    
#整合資料集
dataset["data"] = data
dataset["target"] = target
dataset["feature_name"] = feature_name
dataset["doc"] = doc
print("資料集處理完成")
