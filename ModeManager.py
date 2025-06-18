# ModeManager.py

from DAQManager import DAQManager
import time
import os
import threading
import requests
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
            print("entered be if statement")
            self.paraData = self.currentService.trialParameters

            self.nebControl = {
                'NebStatus': True,
                'StepDurations': list(map(int, self.paraData.SEQUENCE_DURATION.split(','))),
                'NebStates': list(map(int, self.paraData.SEQUENCE.split(',')))
            }

            self.stepDurations = self.nebControl['StepDurations']
            self.nebStates = self.nebControl['NebStates']

            self.currentService.trialParameters.RECORD_DURATION = sum(self.stepDurations)

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
    '''           
    def RegularModeRun(self):
        self.total_samples_read = 0
        start_time = time.time()
        self.logFile.WriteLog('Recording Started', 1)
        self.DAQ.StartDAQ()

        max_duration = self.currentService.trialParameters.RECORD_DURATION 
        self.stateStartTime = time.time()

        while not self.modeData.STOP_FLAG and self.modeData.CONNECTION_FLAG:
            current_time = time.time()
            elapsed_time = int(current_time - start_time)

            # Optional safety: break if max_duration is reached
            if max_duration > 0 and elapsed_time >= max_duration:
                self.logFile.WriteLog('Maximum configured duration reached.', 0)
                break

            msg, self.total_samples_read = self.DAQ.ScanDAQ(self.total_samples_read, nebState)

            if self.currentService.trialParameters.MODE == "BreathEmulate":
                if self.stateSet:
                    self.stateSet = False
                    self.thisState += 1
                    self.stateStartTime = time.time()

                    if self.thisState < len(self.nebStates):
                        self.SwitchControl(self.nebStates[self.thisState])
                        self.endDuration = self.stepDurations[self.thisState]
                    else:
                        self.logFile.WriteLog('Breath Emulation sequence complete.', 0)
                        # Do not break, let the user manually stop
                else:
                    if time.time() - self.stateStartTime >= self.endDuration:
                        self.stateSet = True

            if self.currentService.trialParameters.MODE == "Static":
                # Write functionality
                printf("Static Mode if entered in MM")
                pass

            self.logFile.WriteLog(f'Time Elapsed (s): {elapsed_time}', True)

            if msg == 'HardwareOvr':
                self.logFile.WriteLog('Hardware Over Run')
                break
            elif msg == 'BuffOvr':
                self.logFile.WriteLog('Buffer Over Run')
                break

            # time.sleep(0.5)  # To avoid tight loop
            
        self.DAQ.ResetDAQ()
        if self.modeData.CONNECTION_FLAG:
            self.currentService.thisConnection.SendData2Server('Recording Complete!')

        final_elapsed = int(time.time() - start_time)
        self.logFile.WriteLog('Recording Ended', 1)
        self.logFile.WriteLog(f'Data Recording Complete for a Duration of {final_elapsed}s', 0)
        self.logFile.WriteLog('Final Data Frame Size: ' + str(self.DAQ.recDataFrame.shape), 0)
        self.DAQ.recDataFrame.index.name = 'Samples'
        self.currentService.dataFileManage.Write2CSV(self.DAQ.recDataFrame)

    
    '''
    def RegularModeRun(self):
    
        self.total_samples_read=0
        startTime=time.time()
        endTime=startTime+self.currentService.trialParameters.RECORD_DURATION
        max_duration = self.currentService.trialParameters.RECORD_DURATION
        currentTime=time.time()
        timeElapsed = 0
        self.logFile.WriteLog('Recording Started',1)
        self.DAQ.StartDAQ()
        while not self.modeData.STOP_FLAG and self.modeData.CONNECTION_FLAG:
            currentTime = time.time()
            msg,self.total_samples_read=self.DAQ.ScanDAQ(self.total_samples_read,nebState)
            # COMMENT OUT BELOW
            '''
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
            '''
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

                else:
                    elapsed_time = int(currentTime - startTime)
                    self.logFile.WriteLog(f'(i put)Time Elapsed (s): {elapsed_time}', True)

                    if elapsed >= self.endDuration:
                        self.stateSet = True
            if self.currentService.trialParameters.MODE=="Static":
                print("entered static if statement")
                # WRITE STATIC MODE FUNCTIONALITY
            
            self.logFile.WriteLog('Time Elapsed (s):'+str(int(currentTime-startTime)+1)+' of '+str(self.currentService.trialParameters.RECORD_DURATION),True)
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
        

        self.DAQ.ResetDAQ()
        if self.modeData.CONNECTION_FLAG:
            self.currentService.thisConnection.SendData2Server('Recording Complete!')

        self.logFile.WriteLog('Recording Ended ',1)
        # self.logFile.WriteLog('Data Recording Complete for a Duration of '+str(int(timeElapsed))+'s',0)
        self.logFile.WriteLog(f'Data Recording Complete for a Duration of {elapsed_time}s', 0)
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
        
    
   
