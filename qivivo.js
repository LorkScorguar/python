// create an app here: https://dev.qivivo.com/register
// get a token and complete token and thermostat_id vars
//
// Can:
// - get temperature

const https = require('https');
const http = require('http');
const parsedJSON = require('./Config.json')

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";//to avoid certificate problem

var token=parsedJSON['token'];
var thermostat_id=parsedJSON['thermostat_id'];
const proxy=parsedJSON['proxy']


function getTemp(callback){
  var connectReq = http.request({
    host: proxy,
    port: 8000,
    method: 'CONNECT',
    path: 'data.qivivo.com',
  }).on('connect', function(res, socket, head) {
    var req = https.get({
      host: 'data.qivivo.com',
      path: '/api/v2/devices/thermostats/'+thermostat_id+'/temperature',
      socket: socket, // using a tunnel
      agent: false,    // cannot use a default agent
      headers: {
        'content-type': 'application/json',
        'authorization': 'Bearer '+token,
      }
    }, function(res) {
      res.setEncoding('utf8');
      res.on('data', (data) => {
        jResp = JSON.parse(data);
      });
      res.on('end', (data) => {
        callback(jResp['temperature']);
      });
    });
  }).end();
}


getTemp(function(res){
  console.log("La température est de "+res)
});
