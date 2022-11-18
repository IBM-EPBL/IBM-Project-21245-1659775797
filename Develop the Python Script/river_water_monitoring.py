import time
import sys
import ibmiotf.application
import ibmiotf.device
import random

#Provide your IBM Watson Device Credentials
organization = "j9qiqy"
deviceType = "iot_device"
deviceId = "1234"
authMethod = "token"
authToken = "123456789"

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])
        status=cmd.data['command']
        if status=='lighton':
            print("LIGHT ON")
        else :
            print("LIGHT OFF")
                
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

deviceCli.connect()

while True:
        T=random.randint(0,100);
        H=random.randint(0,100);
        p=random.randint(1,14);
        #Send Temperature & Humidity to IBM Watson
        data = { 'Temperature' : T, 'Humidity': H,'pH':p }
        #print data
        def myOnPublishCallback():
            print ("Temperature = %s C" % T, "Humidity = %s %%" % H, " pH = %s  "% p)

        success = deviceCli.publishEvent("event", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
