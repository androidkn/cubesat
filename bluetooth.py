#!/usr/bin/python3

import bluetooth  
import lightblue  

target_name = "XXX"  #name of the device we are using 
file_to_send = "/home/asanka/Downloads/20130621_151742.jpg" #file we will be sending 

obex_port = None                 
target_address = "XX" #adress of our device  

print ("searching for nearby devices...")
nearby_devices = bluetooth.discover_devices()  
  
for bdaddr in nearby_devices:  
  print(bluetooth.lookup_name( bdaddr ))
  if target_name == bluetooth.lookup_name( bdaddr ): 
    print("found the target device!")
    target_address = bdaddr  
    break  
    
print ("searching for the object push service...")
services = lightblue.findservices(target_address)
for service in services:  
  if service[2] == "OBEX Object Push":  
    obex_port = service[1]       
    print ("OK, service '", service[2], "' is in port", service[1], "!") 
    break  
    
print ("sending a file...")
try:  
  lightblue.obex.sendfile( target_address, service[1], file_to_send )  
  print ("completed!\n")
except:  
  print ("an error occurred while sending file\n" )

#http://recolog.blogspot.com/2013/07/transferring-files-via-bluetooth-using.html

