from netmiko import ConnectHandler
import socket
import os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
for n in range(1, 5):
    server_ip="192.168.20.{0}".format(n)
    rep = os.system('ping ' + server_ip)
    if rep == 0:
        print ("server is up" ,server_ip)
    else:
        print ("server is down" ,server_ip)
template="""logging host 192.168.20.5 transport tcp port 514
logging trap 6
interface loopback 30
description "{rtr} loopback interface\""""

username = 'test'
password="test"

#step 1
#fetch the hostname of the router for the template
for n in range(1, 5):
ip="192.168.20.{0}".format(n)
device = ConnectHandler(device_type='cisco_ios', ip=ip, username='test', password='test')
output = device.send_command("show run | in hostname")
output=output.split(" ")
hostname=output[1]
generatedconfig=template.replace("{rtr}",hostname)

#step 2
#push the generated config on router
#create a list for generateconfig
generatedconfig=generatedconfig.split("\n")
device.send_config_set(generatedconfig)

#step 3:
#perform validations
print ("********")
print ("Performing validation for :",hostname+"\n")
output=device.send_command("show logging")
if ("encryption disabled, link up"):
print ("Syslog is configured and reachable")
else:
print ("Syslog is NOT configured and NOT reachable")
if ("Trap logging: level informational" in output):
print ("Logging set for informational logs")
else:
print ("Logging not set for informational logs")

print ("\nLoopback interface status:")
output=device.send_command("show interfaces description | in loopback interface")
print (output)
print ("************\n")

from netmiko import ConnectHandler
import os
template="""logging host 192.168.20.5 transport tcp port 514
logging trap 6
interface loopback 30
description "{rtr} loopback interface\""""

username = 'test'
password="test"

#step 1
#fetch the hostname of the router for the template
for n in range(1, 5):
ip="192.168.20.{0}".format(n)
device = ConnectHandler(device_type='cisco_ios', ip=ip, username='test', password='test')
output = device.send_command("show run | in hostname")
output=output.split(" ")
hostname=output[1]
generatedconfig=template.replace("{rtr}",hostname)

#step 2
#create different config files for each router ready to be pushed on routers.
configfile=open(hostname+"_syslog_config.txt","w")
configfile.write(generatedconfig)
configfile.close()

#step3 (Validation)
#read files for each of the router (created as routername_syslog_config.txt)
print ("Showing contents for generated config files....")
for file in os.listdir('./'):
if file.endswith(".txt"):
if ("syslog_config" in file):
hostname=file.split("_")[0]
fileconfig=open(file)
print ("\nShowing contents of "+hostname)
print (fileconfig.read())
fileconfig.close()

#snmp_python.py
from pysnmp.hlapi import *
for n in range(1, 3):
server_ip="192.168.20.{0}".format(n)
errorIndication, errorStatus, errorIndex, varBinds = next(
getCmd(SnmpEngine(),
CommunityData('mytest', mpModel=0),
UdpTransportTarget((server_ip, 161)),
ContextData(),
ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
)
print ("\nFetching stats for...", server_ip)
for varBind in varBinds:
print (varBind[1])


#snmp_python_interfacestats.py
from pysnmp.entity.rfc3413.oneliner import cmdgen
cmdGen = cmdgen.CommandGenerator()

for n in range(1, 3):
server_ip="192.168.20.{0}".format(n)
print ("\nFetching stats for...", server_ip)
errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
cmdgen.CommunityData('mytest'),
cmdgen.UdpTransportTarget((server_ip, 161)),
0,25,
'1.3.6.1.2.1.2.2.1.2'
)

for varBindTableRow in varBindTable:
for name, val in varBindTableRow:
print('%s = Interface Name: %s' % (name.prettyPrint(), val.prettyPrint()))


#parallel_query.py
from netmiko import ConnectHandler
from datetime import datetime
from threading import Thread
startTime = datetime.now()

threads = []
def checkparallel(ip):
device = ConnectHandler(device_type='cisco_ios', ip=ip, username='test', password='test')
output = device.send_command("show run | in hostname")
output=output.split(" ")
hostname=output[1]
print ("\nHostname for IP %s is %s" % (ip,hostname))

for n in range(1, 5):
ip="192.168.20.{0}".format(n)
t = Thread(target=checkparallel, args= (ip,))
t.start()
threads.append(t)

#wait for all threads to completed
for t in threads:
t.join()

print ("\nTotal execution time:")
print(datetime.now() - startTime)
