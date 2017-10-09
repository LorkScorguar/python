"""create an app here: https://dev.qivivo.com/register
and put following in Config.py file:
client_id=<generated client id>
secret_id=<generated secret>
token=""
refresh_token=""
thermostat_id=""
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

def ignoreCertificate():
    """Function to ignore ssl certificate error"""
    context = ssl.create_default_context()
    context.check_hostname=False
    context.verify_mode = ssl.CERT_NONE
    return context

def getToken():
    print(auth_url+"?response_type=code&scope=read_devices read_programmation update_programmation update_thermostat&client_id="+client_id+"&redirect_uri="+redirect_uri)
    code=input("Enter code:")
    url=access_token_url
    context=ignoreCertificate()
    req=urllib.request.Request(url+"?grant_type=authorization_code&code="+code+"&client_id="+client_id+"&client_secret="+secret_id+"&redirect_uri="+redirect_uri)
    req.get_method=lambda:'POST'
    resp=urllib.request.urlopen(req,context=context)
    jResp=json.loads(resp.read().decode('utf-8'))
    print(jResp)
    global token
    global refresh_token
    token=jResp['access_token']
    refresh_token=jResp['refresh_token']


def getDevices():
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
            global thermostat_id
            thermostat_id=device['uuid']
    print("Found "+str(len(jResp['devices']))+" devices")

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
    getPrograms()
