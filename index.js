var express = require('express');
var app = express();

app.set('view engine', 'ejs');
app.use('/public', express.static(__dirname + '/public'));

app.get('/', function (req, res) {
	res.render('index.ejs');
});

app.get('/revenue', function (req, res) {
	res.render('revenue.ejs');
});

app.use(function (err, req, res, next) {
	console.error(err.stack);
	res.status(500).send('something broke !')
});
app.use(function (req, res, next) {
	res.status(404).send('sorry cant find that !')
});

app.listen(3000);

require('./public/revenue/db.js');