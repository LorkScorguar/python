// create an app here: https://dev.qivivo.com/register
// get a token and complete token and thermostat_id vars
//
// Can:
// - get temperature

const https = require('https');
const http = require('http');

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";//to avoid certificate problem

const token='';
const thermostat_id="";


function getTemp(){
  var connectReq = http.request({ // establishing a tunnel
    host: 'proxy.com',
    port: 8000,
    method: 'CONNECT',
    path: 'data.qivivo.com',
  }).on('connect', function(res, socket, head) {
    // should check res.statusCode here
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
        jResp = JSON.parse(data)
        console.log(jResp['temperature']);
      });
    });
  }).end();
}


getTemp();
