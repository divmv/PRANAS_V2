from __future__ import print_function
from DataClasses import DeviceFlags
from sys import stdout
from time import sleep
import socket
import numpy as np
import pickle
import json
import os
from datetime import datetime
import threading

class ConnectionManager:
##1
    def __init__ (self,currentService):#,saveFilePath,logFilePath):
        self.currentService=currentService
        self.Connection_Thread=threading.Thread(target=self.ConnectionHandlerThread,args=())
        self.RUNCONNECTION_THREAD=False
        self.sleepIntervalTime=0.2
##2
    def Run_ConnectionHandlerThread(self):
        self.RUNCONNECTION_THREAD=True
        self.Connection_Thread.start()
##3
    def Stop_ConnectionHandlerThread(self):
        self.RUNCONNECTION_THREAD=False
        self.Connection_Thread.join()
        self.currentService.deviceFlags.CONNECTION_FLAG=False
        print("Thread joined")    
        

##4
    def BreakTimeAck(self):
        self.sleepIntervalTime=0.2
        sleep(self.sleepIntervalTime)
        self.portalConnection.sendall(b'Ok')
        sleep(self.sleepIntervalTime)
##5
    def SendData2Server(self,sendData):
        self.portalConnection.sendall(str(sendData).encode('ascii'))
        sleep(self.sleepIntervalTime)
   ##5 
    def RecvDataFromServer(self):
        return str(self.portalConnection.recv(1024).decode('ascii'))
##7
    def SendFile(self,fileName):
        fileRead=open(fileName,'rb')
        dataRead=fileRead.read(10485760)
        self.portalConnection.send(dataRead)
        fileRead.close()
        sleep(5)

        self.currentService.deviceFlags.SEND_FILE=False

##8 
    def ConnectionHandlerThread(self):
        while self.RUNCONNECTION_THREAD:
            try:
                print("Trying Connection")
                self.ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.ServerSocket.settimeout(None)
                self.ServerSocket.connect((self.currentService.trialParameters.IP_Server,self.currentService.trialParameters.PORT_Server))
                self.portalConnection=self.ServerSocket
                sleep(0.5)
                if(self.portalConnection.recv(1024).decode('ascii')=='ServerHere!'):
                    print("Acknowledgement received - Thread Made Connection")
                    #self.logFile.WriteLog('Acknowledgement received from Server at '+str(self.logFile.GetCurrentTime()[0]))
                self.portalConnection.sendall(b'Connection Acknowledgement')
                self.currentService.deviceFlags.CONNECTION_FLAG=True
                
                while self.RUNCONNECTION_THREAD:
                    sleep(0.5)
                    currentRequest=self.portalConnection.recv(1024).decode('ascii')
                    if currentRequest=='Configuration':
                        self.currentService.deviceFlags.START_FLAG=False
                        self.currentService.deviceFlags.STOP_FLAG=False
                        print('Config Request')
                        sleep(0.3)
                        self.portalConnection.sendall(b'Ready')
                        
                        sleep(self.sleepIntervalTime)
                        self.currentService.trialParameters.UID=self.portalConnection.recv(2096).decode('ascii')
                        self.BreakTimeAck()
                        self.currentService.trialParameters.TRIAL=int(self.portalConnection.recv(2096).decode('ascii'))
                        self.BreakTimeAck()
                        self.currentService.trialParameters.MODE=(self.portalConnection.recv(2096).decode('ascii'))
                        self.BreakTimeAck()
                        self.currentService.trialParameters.RECORD_DURATION=int(self.portalConnection.recv(2096).decode('ascii'))
                        self.BreakTimeAck()
                        self.currentService.trialParameters.SAMPLING_RATE=int(self.portalConnection.recv(2096).decode('ascii'))
                        self.BreakTimeAck()
                        self.currentService.trialParameters.BUFFER_SIZE=int(self.portalConnection.recv(2096).decode('ascii'))
                        self.BreakTimeAck()
                        self.currentService.trialParameters.USER= self.portalConnection.recv(2096).decode('ascii')
                        self.BreakTimeAck()
                        sleep(0.4)
                        self.portalConnection.sendall(b'Configuration Complete!')
                        self.currentService.deviceFlags.CONFIGURE_FLAG=True

                    


                    if currentRequest=='Stop':
                        self.currentService.deviceFlags.STOP_FLAG=True
                        self.currentService.deviceFlags.START_FLAG=False
                        
                        
                    if currentRequest=='Start':
                            self.currentService.deviceFlags.STOP_FLAG=False
                            self.currentService.deviceFlags.START_FLAG=True

                    if currentRequest=='Send Last File':
                        print('File Request')
                        self.portalConnection.sendall(b'Ready')
                        sleep(2)
                        self.currentService.deviceFlags.SEND_FILE=True

                            
                            

            except Exception as msg:
                print(msg)
                print("Connection Failed")
                self.currentService.deviceFlags.CONNECTION_FLAG=False
                






