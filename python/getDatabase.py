import pymongo
import datetime

###設定日期與時間的輸出格式
updateDayFormat = "%Y%m%d"                           #設定日期格式
updateTimeFormat = "%H:%M"                           #設定時間格式

###連線mongodb
client = pymongo.MongoClient()                       #連線mondodb
db = client.pyServer                                 #選擇db:pyServer
collection = db.Data                                 #選擇collection:Data

###建立幫助函式
def help():
    print("此模組可用函式如下:\n")
    print("update(data_dict)")
    print("download([date = today]) ex:20180101")

###建立上傳函式
def update(data_dict):
    newDict = data_dict.copy()                       #製作副本以免輸入參數被更改
    if isinstance(newDict, dict):
        date = datetime.date.today().strftime(updateDayFormat)
        time = datetime.datetime.now().strftime(updateTimeFormat)
        newDict["date"] = date                       #設定上傳日期
        newDict["time"] = time                       #設定上傳時間
        collection.insert(newDict)
        print("上傳完成")
    else:
        print("輸入格式錯誤上傳失敗")
    
    
###建立下載函式        
def download(date = datetime.date.today().strftime(updateDayFormat)):
    print("\n搜尋日期:%s\n" % date)
    print("搜尋中...")
    newData = []
    for i in collection.find({"date":date}).sort("_id", pymongo.DESCENDING):
        del i['_id']
        del i['status']
        newData.append(i)
        
    print("下載完成")    
    return newData
