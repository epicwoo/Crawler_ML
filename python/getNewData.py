import requests
import json
import time, datetime
import schedule
import getDatabase as gdb
import getDataML as gdml
time.sleep(2)

#定義抓取資料及處理資料的函數
def getNewData():
    
#抓取新資料，更新時間為每日上午6時、9時、10時、11時
    src = "http://data.coa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx"
    headers = {"user-agent": "Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"}
    dataSrc = requests.get(src, headers = headers).text
    dataSrc = json.loads(dataSrc)

#設定時間格式
    updateTimeFormat = "%Y/%m/%d %H:%M"
    moment = datetime.datetime.now().strftime(updateTimeFormat)

#篩選資料，只留下台北的香蕉交易資料
    count = len(dataSrc)
    for i in range(count,0,-1):
        if "蘋果-" not in dataSrc[i-1]["作物名稱"] or "台北" not in dataSrc[i-1]["市場名稱"]:
            del dataSrc[i-1]

#將當日資料加總平均
    count = len(dataSrc)
    if count != 0:
        a = []
        b = []
        c = []
        d = []
        for i in range(count):
            a.append(dataSrc[i]["交易量"])
            b.append(dataSrc[i]["上價"])
            c.append(dataSrc[i]["中價"])
            d.append(dataSrc[i]["下價"])
            
        print()
        print("開始抓取最新資料")
        print("執行時間 %s" % moment)
        time.sleep(1)
        print()
        print("本日台北各市場交易量", a)
        print("本日台北各市場上價", b)
        print("本日台北各市場中價", c)
        print("本日台北各市場下價", d)
        time.sleep(1)
        
        if len(a) == len(b) == len(c) == len(d):
            item_a = round(sum(a)/count, 2)
            item_b = round(sum(b)/count, 2)
            item_c = round(sum(c)/count, 2)
            item_d = round(sum(d)/count, 2)
    
        print()
        print("本日台北各市場平均交易量", item_a)
        print("本日台北各市場平均上價", item_b)
        print("本日台北各市場平均中價", item_c)
        print("本日台北各市場平均下價", item_d)
        print()
        
        newData = {"describe":"特徵資料","data":[item_a, item_b, item_c, item_d]}
        return newData
    else:
        print("無交易資料")
        return None

#定義執行函式
def daily():
    data = getNewData()
    time.sleep(5)
    if data != None:
        print("上傳特徵資料...")
        time.sleep(3)
        gdb.update(data)
        time.sleep(3)
        print()
        newData = gdml.ML(data)
        print("上傳預測結果...")
        time.sleep(3)
        newData["data"][0] = int(newData["data"][0])
        gdb.update(newData)
daily()
#排程每日執行
schedule.every().day.at("13:57").do(daily)

while True:
    schedule.run_pending()
    time.sleep(1)
