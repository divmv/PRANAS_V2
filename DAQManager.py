#  -*- coding: utf-8 -*-
from __future__ import print_function
from sys import stdout
from time import sleep
from DAQFiles.daqhats.mcc118 import mcc118
from DAQFiles.daqhats.hats import  OptionFlags, HatIDs, HatError
from daqhats_utils import select_hat_device, enum_mask_to_string, \
    chan_list_to_mask
import numpy as np
import sys
import pandas as pd

class DAQManager():
    def __init__(self,currentService):
        self.currentService=currentService
        self.logFile=self.currentService.logFileManage
        self.timeout=5.0
        self.total_samples_read=0
        self.channels=[0,1,2] #X,Y,Power
        self.channel_mask=chan_list_to_mask(self.channels)
        self.num_channels=len(self.channels)
        self.samples_per_channel=0
        self.options=OptionFlags.CONTINUOUS
        self.scan_rate=self.currentService.trialParameters.SAMPLING_RATE
        self.recDataFrame=pd.DataFrame()
        self.READ_ALL_AVAILABLE=int(self.currentService.trialParameters.BUFFER_SIZE)
        self.ResetDAQ()
        self.ConfigureDAQ()
        




    def ConfigureDAQ(self):
        try:
            self.address=select_hat_device(HatIDs.MCC_118)
            self.hat=mcc118(self.address)
            self.logFile.WriteLog('Selected MCC 118 HAT device at address:'+str(self.address),0)
            self.actual_scan_rate=self.hat.a_in_scan_actual_rate(self.num_channels,self.scan_rate)
            self.logFile.WriteLog('Device in continous scan mode',0)
            self.logFile.WriteLog('Channels: '+(''.join([str(chan)+', ' for chan in self.channels]))+' ',0)
            self.logFile.WriteLog('Requested Scan Rate: '+str(self.scan_rate)+' ',0)
            self.logFile.WriteLog('Actual Scan Rate: '+str(self.actual_scan_rate)+' ',0)
            
        except (HatError, ValueError) as err:
            print("Jai Balayya")
            self.logFile.WriteLog(err,1)
            self.currentService.deviceFlags.DAQ_SET=False

    def StartDAQ(self):
        self.hat.a_in_scan_start(self.channel_mask,self.samples_per_channel
                                            ,self.scan_rate,self.options)
        self.currentService.deviceFlags.DAQ_SET=True

    
    def ScanDAQ(self,total_samples_read,nebMode):
        print(self.READ_ALL_AVAILABLE,self.timeout)
        read_result=self.hat.a_in_scan_read(self.READ_ALL_AVAILABLE,self.timeout)
        
        if read_result.hardware_overrun:
            self.logFile.WriteLog('Hardware Overrun',1)
            return 'HardwareOvr'
        elif read_result.buffer_overrun:
            self.logFile.WriteLog('Buffer Overrun',1)
            return 'BuffOvr'
        samples_read_per_channel = int(len(read_result.data) / self.num_channels)
        total_samples_read += samples_read_per_channel
        #print('\r{:12}'.format(samples_read_per_channel),
        #      ' {:12} '.format(total_samples_read), end='')    
        Xpos=[read_result.data[i] for i in range(0,len(read_result.data),3)]
        Ypos=[read_result.data[i] for i in range(1,len(read_result.data),3)]
        Pow=[read_result.data[i] for i in range(2,len(read_result.data),3)]

        currentDF=pd.DataFrame({'Xpos':Xpos,'Ypos':Ypos,'Pow':Pow,'NebMode':nebMode})
        self.recDataFrame=self.recDataFrame.append(currentDF,ignore_index=True)
        if samples_read_per_channel > 0:
            endIndex = samples_read_per_channel * self.num_channels - self.num_channels
            stdout.flush()
            sleep(0.1)
        return 'Success',total_samples_read
        
    def ResetDAQ(self):
        try:
            self.hat.a_in_scan_stop()
            self.hat.a_in_scan_cleanup() 
        except:
            self  
        

        
        
        






