var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost/";
var fs = require('fs');
var schedule = require('node-schedule');

MongoClient.connect(url, {useNewUrlParser: true}, function (err, db) {
    if (err) throw err;

    var mydb = db.db("pyServer");
    var mysort = {
        "date": -1,
        "time": -1
    }

    schedule.scheduleJob('1,31 * * * * *', function () {
            mydb.collection("Data").find({
                describe: '特徵資料'
            }).sort(mysort).limit(1).toArray(function (err, result) {
                if (err) throw err;
                //console.log(result);
                fs.writeFile('./public/revenue/features.json', JSON.stringify(result), function (err) {
                    if (err) throw err;
                });
                //db.close();
            });
        })

    schedule.scheduleJob('21,51 * * * * *', function () {
            mydb.collection("Data").find({
                describe: '預測結果'
            }).sort(mysort).limit(1).toArray(function (err, result) {
                if (err) throw err;
                //console.log(result);
                fs.writeFile('./public/revenue/predict.json', JSON.stringify(result), function (err) {
                    if (err) throw err;
                });
                //db.close();
            });
        })
    });


// schedule時間設定格式

// *  *  *  *  *  *
// ┬ ┬ ┬ ┬ ┬ ┬
// │ │ │ │ │  |
// │ │ │ │ │ └ day of week (0 - 7) (0 or 7 is Sun)
// │ │ │ │ └───── month (1 - 12)
// │ │ │ └────────── day of month (1 - 31)
// │ │ └─────────────── hour (0 - 23)
// │ └──────────────────── minute (0 - 59)
// └───────────────────────── second (0 - 59, OPTIONAL)