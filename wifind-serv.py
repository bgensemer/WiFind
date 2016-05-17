#!/usr/bin/env python
import socket
import threading
import SocketServer
import time
from time import sleep

#########################################################
#              Global Variables                         #
#########################################################
lock = threading.Lock()
dataList = []
macList = []
macList2 = []
macList3 = []
matchingMacs = []

#########################################################
#              Classes                                  #
#########################################################

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):

        data = self.request.recv(1024)
        with lock:
            recieve_information(data)
        #print data

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

#class update_list():
#___________________PSEUDO BEGIN_______________________________________________________________
#       iterate list, 
#       for each (capTime) take (capTime) - (currentTime)
#       if capTime - currentTime > 30s, then decayItem = capTime
#       delete_item(decayItem)
#___________________PSEUDO END_________________________________________________________________
#    def check_item(self):
#        pass
#
#
#    def delete_item(self, decayItem):
#            #lock dataList or enter queue
#        try:
#            dataList = [dataItem for dataItem in dataList if dataItem != decayItem]
#        except(ValueError):
#            print 'ValueError thrown. Tried to delete item that did not exist. (Race Condition?)'
#        finally:
#            #unlock dataList
#            pass
#
#
#class Thread(threading.Thread):
#    def __init__(self, t, *args):
#        threading.Thread.__init__(self, target=t, args=args)
#        self.start()




def recieve_information(data):
    #do stuff to seperate the data fields
    #check for ID number
    #print 'inside recieve iformation'
    #print 'given: ' + data
    global macList
    global macList2
    global macList3

   # print macList
   # print macList2
   # print macList3
    
    gatheredList = []
    gatheredList = data.split(",")
    idItem = gatheredList[0]
    timeItem = gatheredList[1]
    pwrItem = gatheredList[2]
    freqItem = gatheredList[3]
    macItem = gatheredList[4]
    ouiItem = gatheredList[5]
    #print gatheredList

    print idItem
    if idItem == '1':
        print 'id number is 1'
    #do stuff to search list
        try: 
          macIndex = macList.index(macItem)
          if timeItem == macList[macIndex+1]:
              print 'time same ignoring'
              pass
          else:
              print 'time different but mac exists, updating'
              macList[macIndex+1] = timeItem
              macList[macIndex+2] = pwrItem
              macList[macIndex+3] = freqItem
              macList[macIndex+4] = ouiItem
              #mac exists but time is different, update all records except mac address
        except(ValueError):
            print 'ValueError handling...'
            macList.append(macItem)
            macList.append(timeItem)
            macList.append(pwrItem)
            macList.append(freqItem)
            macList.append(ouiItem)
            print '___macList being written to___'
            print macList
            print '______________________________'
#Logic: if first node, you're the man.
#Add everything you see to list.
#First check if a mac already exists, if it doesn't exist there will be a ValueError exception.
#Catch exception with except(ValueError): and then append everything, because we need this stuff.

    elif idItem == '2':
        #are we the second node?
        #if so lets check our data against the master list!

        try: 
          macIndex2 = macList2.index(macItem)
          if timeItem == macList2[macIndex+1]:
              pass
          else:
              macList2[macIndex+1] = timeItem
              macList2[macIndex+2] = pwrItem
              macList2[macIndex+3] = freqItem
              macList2[macindex+4] = ouiItem
              #mac exists but time is different, update all records except mac address
        except(ValueError):
            macList2.append(macItem)
            macList2.append(timeItem)
            macList2.append(pwrItem)
            macList2.append(freqItem)
            macList2.append(ouiItem)

    elif idItem == '3':
        #dostuff the stuff strikes back
        try: 
          macIndex3 = macList3.index(macItem)
          if timeItem == macList3[macIndex+1]:
              pass
          else:
              macList3[macIndex+1] = timeItem
              macList3[macIndex+2] = pwrItem
              macList3[macIndex+3] = freqItem
              macList3[macindex+4] = ouiItem
              #mac exists but time is different, update all records except mac address
        except(ValueError):
            macList3.append(macItem)
            macList3.append(timeItem)
            macList3.append(pwrItem)
            macList3.append(freqItem)
            macList3.append(ouiItem)
    else:
        pass
        print 'if/else block failed!'
        #break, but pass for now

def main_work():
    while True:

    
        global macList 
        global macList2
        global macList3
        global dataList
        global matchingMacs
        
        matchingMacs = []
        matchingMacs0 = []
        sleep(1)

        with lock:
            if macList != []:
                tempList = macList[::5]
    #create temp list with all macs from macList (node1)
                tempList2 = macList2[::5]
                tempList3 = macList3[::5]
    
                matchingMacs0[set(tempList).intersection(tempList2)]
                matchingMacs[set(matchingMacs0).intersection(tempList3)]
    #where all macs match create new list named machingMacs
    ########################## NEED LOGIC FOR EMPTY AND TO CLEAR THIS FROM PREVIOUS ITERATIONS ##############################!!!!!!!!!!!!!!!!!!!!!!!!
                for macAddress in matchingMacs:
        #iterate matching macs by macAddress
                    try:
            #set matched macs to index for each iteration
                        matchingMacIndex = tempList.index(macAddress)
                        matchingMacIndex2 = tempList2.index(macAddress)
                        matchingMacIndex3 = tempList3.index(macAddress)
                        try:
                            node1mac = macAddress
                            node1time = macList[matchingMacIndex+1]
                            node1pwr = macList[matchingMacIndex+2]
                            node1freq = macList[matchingMacIndex+3]
                            node1oui = macList[matchingMacIndex+4]
                            node2pwr = macList[matchingMacIndex2+2]
                            node3pwr = macList[matchingMacIndex3+2]
                            try:
                                dataListIndex = dataList.index(macAddress)
                                if dataList[dataListIndex+1] != node1time:
                                    dataList[dataListIndex+1] = node1time
                                    dataList[dataListIndex+4] = node1pwr
                                    dataList[dataListIndex+5] = node2pwr
                                    dataList[dataListIndex+6] = node3pwr
                                else:
                                    pass
                    
                            except(ValueError):
                                datalist.append(node1mac)
                                datalist.append(node1time)
                                datalist.append(node1freq)
                                datalist.append(node1oui)
                                datalist.append(node1pwr)
                                datalist.append(node2pwr)
                                datalist.append(node3pwr)
                            finally:
                                pass
                        finally:
                            pass
                    finally:
                        pass
            else:
                print "empty"

#########################################################
#              Main                                     #
#########################################################

if __name__ == "__main__":
    HOST, PORT = '', 1234
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

# Start a thread with the server -- that thread will then start one
# more thread for each request

server_thread = threading.Thread(target=server.serve_forever)
# Exit the server thread when the main thread terminates

server_thread.daemon = True
server_thread.start()

main_thread_1 = threading.Thread(target=main_work)
print "Server loop running in thread:", server_thread.name
main_thread_1.start()
print "Main_thread_1 running in thread:", main_thread_1.name

while True:
    pass
