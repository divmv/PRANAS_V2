# ModeManager.py

from DAQManager import DAQManager
import time
from datetime import datetime
import os
import threading
import requests
import warnings

warnings.filterwarnings("ignore")

class ModeManager():

    global nebState
    nebState=0
    
    '''
    def __init__(self,currentService):
        
        self.currentService=currentService
        self.logFile=self.currentService.logFileManage
        self.curDuration = 0
        
        self.stateSet = True
        self.thisState = -1
        self.curDuration = 0
        self.endDuration = 0


        if self.currentService.trialParameters.MODE=="BreathEmulate":
            if self.stateSet:
                print(self.stateSet)
                self.stateSet = False
                self.thisState += 1
                self.SwitchControl(self.nebStates[self.thisState])
            if self.thisState <= len(self.stepDurations):
                self.endDuration = self.stepDurations[self.thisState]
                self.curDuration = 0
            else:
                self.curDuration += 1
            if self.curDuration >= self.endDuration - 1:
                self.stateSet = True
                self.curDuration = 0

            print("entered be if statement")
            self.paraData=self.currentService.trialParameters
            self.nebControl={'NebStatus':True,'StepDurations':list(map(int,self.paraData.SEQUENCE_DURATION.split(','))),'NebStates':list(map(int,self.paraData.SEQUENCE.split(',')))}
            self.currentService.trialParameters.RECORD_DURATION=sum(self.nebControl['StepDurations'])
            
            self.logFile.WriteLog('Step Durations:'+self.paraData.SEQUENCE_DURATION,0)
            self.logFile.WriteLog('Nebulizer States:'+self.paraData.SEQUENCE,0)
            
            self.stepDurations=self.nebControl['StepDurations']
            self.nebStates=self.nebControl['NebStates']
            
            self.thisState=-1
            self.stateSet=True
        self.DAQ=DAQManager(self.currentService)
        self.modeData=self.currentService.deviceFlags
    '''
    
    def __init__(self, currentService):
        self.currentService = currentService
        self.logFile = self.currentService.logFileManage

        self.stateSet = True
        self.thisState = -1
        self.curDuration = 0
        self.endDuration = 0
        self.nebState = 0
        
        if self.currentService.trialParameters.MODE == "Static":
            print("entered first static if")
            # write functionality

        if self.currentService.trialParameters.MODE == "BreathEmulate":
            # print("entered be if statement")
            self.paraData = self.currentService.trialParameters

            self.nebControl = {
                'NebStatus': True,
                'StepDurations': list(map(int, self.paraData.SEQUENCE_DURATION.split(','))),
                'NebStates': list(map(int, self.paraData.SEQUENCE.split(',')))
            }

            self.stepDurations = self.nebControl['StepDurations']
            self.nebStates = self.nebControl['NebStates']

            # self.currentService.trialParameters.RECORD_DURATION = sum(self.stepDurations)

            self.logFile.WriteLog('Step Durations: ' + self.paraData.SEQUENCE_DURATION, 0)
            self.logFile.WriteLog('Nebulizer States: ' + self.paraData.SEQUENCE, 0)

        self.DAQ = DAQManager(self.currentService)
        self.modeData = self.currentService.deviceFlags


    def SwitchControl(self,nebstate1):
        global nebState
        nebState=nebstate1
        print(nebstate1)
        if nebstate1==0:
            requests.post("https://maker.ifttt.com/trigger/off_switch/with/key/bQbEEqB8H2G9oAy3ndl-aK")
            print('Nebulizer Off')
        elif nebstate1==1:    
            requests.post("https://maker.ifttt.com/trigger/on_switch/with/key/bQbEEqB8H2G9oAy3ndl-aK")
            print('Nebulizer On') 

    def current_time_string(self):
        return datetime.now().strftime("%H:%M:%S")

    def RegularModeRun(self):
    
        self.total_samples_read=0
        startTime=time.time()
        # totalTime = self.currentService.trialParameters.RECORD_DURATION
        totalTime = self.currentService.trialParameters.RECORD_DURATION
        # print(f'Start time: {self.current_time_string()}')
        self.logFile.WriteLog(f": Recording Started", 1)
        # print(current_time_string() + ":Recording Started")
        # print(f'Total Duration: {totalTime}')
        self.logFile.WriteLog(f"Total Duration: {totalTime} seconds", 0)
        elapsed = 0
        # step_durations = self.serviceManager.trialParameters.STEP_DURATIONS
        # nebulizer_states = self.serviceManager.trialParameters.NEBULIZER_STATES

        current_step_index = 0
        step_start_time = time.time()
        self.logFile.WriteLog('Recording Started',1)
        self.DAQ.StartDAQ()

        while (elapsed) < totalTime and (not self.modeData.STOP_FLAG):
            msg,self.total_samples_read=self.DAQ.ScanDAQ(self.total_samples_read,nebState)

            elapsed = int(time.time() - startTime)
            # print(f'Time Elapsed: {elapsed}')
            # print(f"{self.current_time_string()}:Time Elapsed (s):{elapsed} of {totalTime}")
            self.logFile.WriteLog(f"{self.current_time_string()}:Time Elapsed (s):{elapsed} of {totalTime}", 0)
            if self.currentService.trialParameters.MODE=="BreathEmulate":
                print("Breath Emulation")
            
            if self.currentService.trialParameters.MODE=="Static":
                print("entered static if statement")
                # WRITE STATIC MODE FUNCTIONALITY
            if msg=='HardwareOvr':
                self.logFile.WriteLog('Hardware Over Run')
                break
            elif msg=='BuffOvr':
                self.logFile.WriteLog('Buffer Over Run')
                break
            time.sleep(0.1)  # sleep
            

        '''
        while not self.modeData.STOP_FLAG and self.modeData.CONNECTION_FLAG:
            currentTime = time.time()
            msg,self.total_samples_read=self.DAQ.ScanDAQ(self.total_samples_read,nebState)
            # COMMENT OUT BELOW
            
            if self.currentService.trialParameters.MODE=="BreathEmulate":
                if self.stateSet:
                    print(self.stateSet)
                    self.stateSet=False
                    self.thisState+=1
                    self.SwitchControl(self.nebStates[self.thisState])
                    if self.thisState<=len(self.stepDurations):
                        endDuration=self.stepDurations[self.thisState]
                        curDuration=0
                else:
                    curDuration+=1
                    if curDuration>=endDuration-1:
                        self.stateSet=True
                        curDuration=0
            #TILL HERE
            
            if self.currentService.trialParameters.MODE=="BreathEmulate":
                
                if self.stateSet:
                    self.stateSet = False
                    self.thisState += 1
                    self.stateStartTime = time.time()

                    if self.thisState < len(self.nebStates):
                        self.SwitchControl(self.nebStates[self.thisState])
                        self.endDuration = self.stepDurations[self.thisState]
                        
                    else:
                        print("Breath Emulation sequence complete.")
                        # break  # or continue without switching

                # else:
                    # elapsed_time = int(currentTime - startTime)
                    # self.logFile.WriteLog(f'(i put)Time Elapsed (s): {elapsed_time}', True)

                    # if elapsed >= self.endDuration:
                        # self.stateSet = True
            if self.currentService.trialParameters.MODE=="Static":
                print("entered static if statement")
                # WRITE STATIC MODE FUNCTIONALITY

            elapsed = int(time.time() - startTime)
            if elapsed == totalTime:
                print(f'Elapsed Time: {elapsed}')
                self.logFile.WriteLog(f'(i put)Time Elapsed (s): {elapsed}', True)
            
            # self.logFile.WriteLog('Time Elapsed (s):'+str(int(currentTime-startTime)+1)+' of '+str(self.currentService.trialParameters.RECORD_DURATION),True)
            if msg=='HardwareOvr':
                self.logFile.WriteLog('Hardware Over Run')
                break
            elif msg=='BuffOvr':
                self.logFile.WriteLog('Buffer Over Run')
                break
            else:
                currentTime=time.time()
                timeElapsed=currentTime-startTime
                continue
            time.sleep(0.5)  # sleep for 1 second
        '''

        self.DAQ.ResetDAQ()
        if self.modeData.CONNECTION_FLAG:
            self.currentService.thisConnection.SendData2Server('Recording Complete!')

        self.logFile.WriteLog('Recording Ended ',1)
        # self.logFile.WriteLog('Data Recording Complete for a Duration of '+str(int(timeElapsed))+'s',0)
        self.logFile.WriteLog(f'Data Recording Complete for a Duration of {elapsed}s', 0)
        self.logFile.WriteLog('Final Data Frame Size:'+str(self.DAQ.recDataFrame.shape),0)
        self.DAQ.recDataFrame.index.name='Samples'

        self.currentService.dataFileManage.Write2CSV(self.DAQ.recDataFrame)



        

class RecordMode(ModeManager):
    def __init__(self,currentService):
        ModeManager.__init__(self,currentService)
    def Run(self):
        print("entered record/combined mode")
        self.RegularModeRun()

class BreathEmulationMode(ModeManager):
    def __init__(self,currentService):
        ModeManager.__init__(self,currentService)
        #self.Nebulizer_Thread=threading.Thread(target=self.NebulizerControl,args=())
    def Run(self):
        print("entered be mode")
        self.RegularModeRun()

class StaticMode(ModeManager):
    def __init__(self,currentService):
        ModeManager.__init__(self,currentService)
    def Run(self):
        print("entered static mode")
        self.RegularModeRun()
        
    
   
