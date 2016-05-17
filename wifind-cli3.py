#!/usr/bin/env python
import subprocess as sub
import time
import socket
from netaddr import *

packetInfo = []
idNumber = 3
baseCounter = 0
p = sub.Popen(('sudo', 'tcpdump', '-i', 'mon0', '-l', '-e', '-s', '256', 'type', 'mgt', 'subtype', 'probe-req'), stdout=sub.PIPE, stderr=sub.PIPE)
#Starts tcpdump as a subprocess
for row in iter(p.stdout.readline, b''):
    #iterates through each line of sterr given from the tcpdump subprocess
    counter = 0
    packetNumber = baseCounter / 4
    print "Packet: ", packetNumber
    #Tells us which packet we are currently on (of each packet we save 4 pieces of data
    for entry in row.split():
        if counter == 0:
            #            time
            packetInfo.append(entry)
        elif counter == 5:
             #           freq
            packetInfo.append(entry)
        elif counter == 8:
            #            pwr
            packetInfo.append(entry)
        elif counter == 14:
            #            mac
            if entry != 'BSSID:Broadcast':
                if entry != 'Unknown)':
                    packetInfo.append(entry[3:])
                else:
                    packetInfo.append(entry[:-1])
            else:
                packetInfo.append('Unknown')
        else:
            pass
        counter = counter + 1
    macname = str(packetInfo[baseCounter+3])
    try:
        if str(packetInfo[baseCounter+3]) != 'Unknown':
            mac = EUI(macname)
            oui = mac.oui
            oui_out = oui.registration().org
        else:
            oui_out = 'Unknown'
    except(RuntimeError, TypeError, NameError, NotRegisteredError):
        oui_out = 'Unknown'
    if packetNumber != 0 and packetNumber != 1:
         send_info = str(idNumber) + ',' + str(packetInfo[baseCounter]) + ',' + str(packetInfo[baseCounter+2]) + ',' + str(packetInfo[baseCounter+1]) + ',' + str(packetInfo[baseCounter+3] + ',' + str(oui_out))
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         host = '169.254.210.168'
         port = 1234
         s.connect((host, port))
         s.sendall(send_info)
         print "Packet number: ", packetNumber, " sent"
         s.close()
    baseCounter = baseCounter + 4

