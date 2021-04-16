import requests
import json
import argparse
import time
import sys

#Capture command line arguments
arguments = sys.argv



#Capture command line arguments
arg_options = argparse.ArgumentParser(description="Control containers for the project")
arg_options.add_argument('--application', required=True, type=str)
arg_options.add_argument('--imagename', type=str)
arg_options.add_argument('--tag', type=str)
arg_options.add_argument('--url', type=str)



args = arg_options.parse_args()

application = ""
imagename = ""
tag = ""
url = ""

if args.application is not None:
    application = args.application
    
if args.imagename is not None:
    imagename = args.imagename
    
if args.tag is not None:
    tag = args.tag
    
if args.url is not None:
    url = args.url
    
s = requests.Session()


s.headers.update({
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Authorization': "Bearer c64Ca28whEAIkFYlzO8clRutrlwVws2pFRwEz09Pm9I"
    })



#Build API URL
host = "https://uleska-live-one.uleska.com/"

#payload = '{ "settingsName": "' + wi_settings_name + '", "overrides": { "startUrls": ["' + app_start_url + '"],  "networkAuthenticationMode": "basic", "networkCredentials": ["' + app_username + '","' + app_password + '"] }'
payload = '{"name":"' + imagename + '-' + tag + '","forceCookies":false,"roles":[],"webPageList":[],"tools":[],"reports":[],"actions":[],"scmConfiguration":{"useUpload":false,"authenticationType":"UNAUTHENTICATED","address":"' + url + '"}}'

##### 
AddVersion = host + "SecureDesigner/api/v1/applications/" + application + "/versions"


#print ("AddVersion: " + AddVersion)

#print ("\n\n")

#print ("Payload: " + payload)

#print ("\n\n")


print ("Ensuring container " + imagename + "-" + tag + " associated with this project\n")
       
try:
    StatusResponse = s.request("POST", AddVersion, data=payload)
except requests.exceptions.RequestException as err:
    print ("Exception occured adding container\n" + str(err))
    sys.exit()
    
if StatusResponse.status_code != 201:
    #Something went wrong, maybe server not up, maybe auth wrong
    print("Non 201 (Created) status code returned when adding container.  Code [" + str(StatusResponse.status_code) + "]")
    sys.exit()
    

version_info = ""

try:
    version_info = json.loads(StatusResponse.text)
except json.JSONDecodeError as jex:
    print ("Invalid JSON when checking for version information.  Exception: [" + str(jex) + "]")
    sys.exit()
    

version_id = ""

if 'id' in version_info:
    version_id = version_info['id']
    

print ("New version for " + imagename + "-" + tag + " successfully created (" + version_id + "\n")





# Now we have the ID of the new version added, get the Clair tool added

AddTool = host + "SecureDesigner/api/v1/applications/" + application + "/versions/" + version_id 

toolpayload = '{"id":"' + version_id + '","createdDate":"2021-04-14T14:18:32.518+0000","name":"' + imagename + '-' + tag + '","webPageList":[],"roles":[],"tools":[{"toolName":"CLAIR"}],"reports":[],"scmConfiguration":{"useUpload":false,"address":"' + url + '","authenticationType":"UNAUTHENTICATED"}}'
 
 
#print ("Adding Clair tool for this new pipeline\n")

#print ("AddTool: " + AddTool)

#print ("\n\n")

#print ("toolpayload: " + toolpayload)

#print ("\n\n")


      
try:
    StatusResponse = s.request("PUT", AddTool, data=toolpayload)
except requests.exceptions.RequestException as err:
    print ("Exception occured adding tool\n" + str(err))
    sys.exit()
    
if StatusResponse.status_code != 200:
    #Something went wrong, maybe server not up, maybe auth wrong
    print("Non 200 (OK) status code returned when adding tool.  Code [" + str(StatusResponse.status_code) + "]")
    sys.exit()


print ("Version and container analysis tool successfully setup, initiating testing ...\n")



##### Kick off a scan
ScanURL = host + "SecureDesigner/api/v1/applications/" + application + "/versions/" + version_id + "/scan"

#Check for running scans
try:
    StatusResponse = s.request("Get", ScanURL)
except requests.exceptions.RequestException as err:
    print ("Exception running scan\n" + str(err))
    sys.exit()
    
if StatusResponse.status_code != 200:
    #Something went wrong, maybe server not up, maybe auth wrong
    print("Non 200 status code returned when running scan.  Code [" + str(StatusResponse.status_code) + "]")
    sys.exit()


print("ScanId " + json_data.get("ScanId") + " is now running")

