"""create an app here: https://dev.qivivo.com/register
and put following in Config.py file:
client_id=<generated client id>
secret_id=<generated secret>
token=""
refresh_token=""
thermostat_id=""

Can:
- set temperature
- get temperature
- get humidity
- get current program
- set program
- check if heating is running
"""
import json
import ssl
import urllib.request
import Config

client_id=Config.client_id
secret_id=Config.secret_id
redirect_uri="https://qivivo.com/authorize"
auth_url="https://account.qivivo.com/"
access_token_url="https://account.qivivo.com/oauth/token"
token=Config.token
refresh_token=Config.refresh_token
thermostat_id=Config.thermostat_id

def updateConfig(param,value):
    #save configuration
    save = {}
    cfg = open("Config.py","r")
    for line in cfg:
        parm = line.strip().split("=")[0]
        val = line.strip().split("=")[1]
        save[parm] = val
    cfg.close()
    #do the change and write file
    save[param] = '"'+value+'"'
    cfg = open("Config.py","w")
    for k,v in save.items():
        cfg.write(str(k)+"="+str(v)+"\n")
    cfg.close()

def ignoreCertificate():
    """Function to ignore ssl certificate error"""
    context = ssl.create_default_context()
    context.check_hostname=False
    context.verify_mode = ssl.CERT_NONE
    return context

def getToken():
    global token
    global refresh_token
    print(auth_url+"?response_type=code&scope=read_devices read_programmation update_programmation read_thermostats read_wireless_modules&client_id="+client_id+"&redirect_uri="+redirect_uri)
    code=input("Enter code:")
    url=access_token_url
    context=ignoreCertificate()
    req=urllib.request.Request(url+"?grant_type=authorization_code&code="+code+"&client_id="+client_id+"&client_secret="+secret_id+"&redirect_uri="+redirect_uri)
    req.get_method=lambda:'POST'
    resp=urllib.request.urlopen(req,context=context)
    jResp=json.loads(resp.read().decode('utf-8'))
    print(jResp)
    token=jResp['access_token']
    refresh_token=jResp['refresh_token']

def refreshToken():
    global token
    global refresh_token
    url=access_token_url
    context=ignoreCertificate()
    req=urllib.request.Request(url+"?grant_type=refresh_token&client_id="+client_id+"&client_secret="+secret_id+"&redirect_uri="+redirect_uri+"&refresh_token="+refresh_token)
    req.get_method=lambda:'POST'
    resp=urllib.request.urlopen(req,context=context)
    jResp=json.loads(resp.read().decode('utf-8'))
    #print(jResp)
    token=jResp['access_token']
    refresh_token=jResp['refresh_token']
    updateConfig("token",token)
    updateConfig("refresh_token",refresh_token)

def getDevices():
    global thermostat_id
    url = "https://data.qivivo.com/api/v2/devices"
    context=ignoreCertificate()
    req=urllib.request.Request(url)
    req.add_header("content-type", "application/json")
    req.add_header("authorization", "Bearer "+token)
    req.get_method=lambda:'GET'
    resp=urllib.request.urlopen(req,context=context)
    jResp=json.loads(resp.read().decode('utf-8'))
    for device in jResp['devices']:
            if device['type']=='thermostat':
                thermostat_id=device['uuid']
    return jResp['devices']

def getPrograms():
    dprog = {}
    url = "https://data.qivivo.com/api/v2/devices/thermostats/"+thermostat_id+"/programs"
    context=ignoreCertificate()
    req=urllib.request.Request(url)
    req.add_header("content-type", "application/json")
    req.add_header("authorization", "Bearer "+token)
    req.get_method=lambda:'GET'
    resp=urllib.request.urlopen(req,context=context)
    jResp=json.loads(resp.read().decode('utf-8'))
    prog_id=jResp['user_active_program_id']
    print("Currently using "+str(jResp['user_programs'][prog_id-1]['name']))
    for prog in jResp['user_programs']:
        dprog[prog['name']]=prog['id']
    return dprog

def changeProgram(prog_name):
    dprog = getPrograms()
    url = "https://data.qivivo.com/api/v2/devices/thermostats/"+thermostat_id+"/programs/"+dprog[prog_name]+"/active"
    context=ignoreCertificate()
    req=urllib.request.Request(url)
    req.add_header("content-type", "application/json")
    req.add_header("authorization", "Bearer "+token)
    req.get_method=lambda:'PUT'
    resp=urllib.request.urlopen(req,context=context)
    getPrograms()

def getTemp(deviceid):
    url = "https://data.qivivo.com/api/v2/devices/thermostats/"+deviceid+"/temperature"
    context=ignoreCertificate()
    req=urllib.request.Request(url)
    req.add_header("content-type", "application/json")
    req.add_header("authorization", "Bearer "+token)
    req.get_method=lambda:'GET'
    resp=urllib.request.urlopen(req,context=context)
    jResp=json.loads(resp.read().decode('utf-8'))
    return jResp['temperature']

def getHumidity(deviceid):
    url = "https://data.qivivo.com/api/v2/devices/thermostats/"+deviceid+"/humidity"
    context=ignoreCertificate()
    req=urllib.request.Request(url)
    req.add_header("content-type", "application/json")
    req.add_header("authorization", "Bearer "+token)
    req.get_method=lambda:'GET'
    resp=urllib.request.urlopen(req,context=context)
    jResp=json.loads(resp.read().decode('utf-8'))
    return jResp['humidity']

#can't work as update_thermostat scope is invalid
def setTemp(temp,duration):
    data={"temperature":temp,"duration":duration}
    url = "https://data.qivivo.com/api/v2/devices/thermostats/"+thermostat_id+"/temperature/temporary-instruction"
    context=ignoreCertificate()
    req=urllib.request.Request(url)
    req.add_header("content-type", "application/json")
    req.add_header("authorization", "Bearer "+token)
    req.get_method=lambda:'POST'
    resp=urllib.request.urlopen(req,json.dumps(data).encode('utf-8'),context=context)

try:
    _=getDevices()
    t=getTemp(thermostat_id)
    print(thermostat_id+":"+str(t))
except:
    refreshToken()
    _=getDevices()
    t=getTemp(thermostat_id)
    print(thermostat_id+":"+str(t))
