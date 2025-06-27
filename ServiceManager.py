# ServiceManager

from DataManager import DataFileManage, LogFileManage
from ConnectionManager2 import ConnectionManager
from ModeManager import RecordMode, BreathEmulationMode, StaticMode
from DataClasses import TrialParameters,DeviceFlags
from datetime import datetime
import time
import os
from kivy.clock import Clock
import threading

class ServiceManager:
        def __init__ (self, gui):
                self.gui = gui
                # self.thisConnection=ConnectionManager(self)
                # self.thisConnection.Run_ConnectionHandlerThread()
                self.connection_Check=False
                self.trialParameters=TrialParameters()
                self.deviceFlags=DeviceFlags()
                self.logFileManage = LogFileManage(self)
                print("contacted Service Manager")
                Clock.schedule_interval(self.process_flags, 0.5)

        def process_flags(self, dt):
                if self.deviceFlags.CONFIGURE_FLAG:
                        self.configure_device()
                if self.deviceFlags.START_FLAG:
                        self.start_mode()
                if self.deviceFlags.STOP_FLAG:
                        self.stop_mode()
                if self.deviceFlags.SEND_FILE:
                        self.send_files()
                        
        def configure_device(self):
                """Handle device configuration."""
                self.logFileManage = LogFileManage(self)
                self.dataFileManage = DataFileManage(self)
                
                # # Write configuration logs
                # self.logFileManage.WriteLog('Device Configured', 1)
                self.logFileManage.WriteLog(f'UID: {self.trialParameters.UID}', 0)
                self.logFileManage.WriteLog(f'Mode: {self.trialParameters.MODE}', 0)
                self.logFileManage.WriteLog(f'Trial: {self.trialParameters.TRIAL}', 0)
                self.logFileManage.WriteLog(f'Duration: {self.trialParameters.RECORD_DURATION} seconds', 0)
                # self.logFileManage.WriteLog(f'Sampling Rate: {self.trialParameters.SAMPLING_RATE}', 0)
                # self.logFileManage.WriteLog(f'Buffer Size: {self.trialParameters.BUFFER_SIZE}', 0)
                self.logFileManage.WriteLog(f'User: {self.trialParameters.USER}', 0)
                self.logFileManage.WriteLog('-----------------------------------', 0)

                # Set mode
                if self.trialParameters.MODE == "BreathEmulate":
                        self.currentMode = BreathEmulationMode(self)
                        self.deviceFlags.CONFIGURE_FLAG = False
                        print("Breath Emulate Mode")
                elif self.trialParameters.MODE == "Static":
                        self.currentMode = StaticMode(self)
                        self.deviceFlags.CONFIGURE_FLAG = False
                        print("Static Mode")
                else:
                        self.currentMode = RecordMode(self)
                        self.deviceFlags.CONFIGURE_FLAG = False
                        print("Combined Mode")
                        
                print("Device configured.")

        
        def start_mode(self):
                """Start the current mode."""
                
                if self.currentMode:
                        print("Mode started.")
                        self.currentMode.Run()
                
                self.deviceFlags.START_FLAG = False
                
        '''
        def start_mode(self):
                """Start the current mode"""
                if self.currentMode:
                        self.mode_thread = threading.Thread(target=self.currentMode.Run)
                        self.mode_thread.daemon = True
                        self.mode_thread.start()
                self.deviceFlags.START_FLAG = False
                print("Mode started.")
        '''

        def stop_mode(self):
                """Stop the current mode."""
                print("Mode stopped.")
                self.deviceFlags.STOP_FLAG = False

        def send_files(self):
                """Send log and data files."""
                if self.logFileManage and self.dataFileManage:
                        log_file_path = os.path.join(self.logFileManage.logFileFolder, self.logFileManage.log_file_name)
                        data_file_path = os.path.join(self.dataFileManage.RecordDataFolder, self.dataFileManage.data_file_name)

                        print(f"Storing log file locally: {log_file_path}")
                        print(f"Storing data file locally: {data_file_path}")

                        # Simulate sending files locally
                        # Replace this with actual file management logic
                        self.deviceFlags.SEND_FILE = False
                        print("Files sent.")

        def GetCurrentTime(self,tpe):
                #Gets current time and returns in string and integer format
                dt_now=datetime.now()
                if tpe==1:
                       return str(dt_now.hour)+':'+str(dt_now.minute)+':'+str(dt_now.second)
                if tpe==2:
                        return str(dt_now.month)+'/'+str(dt_now.day)+'/'+str(dt_now.year) 
                if tpe==3:
                        return str(10000000000*dt_now.year+100000000*dt_now.month+1000000*dt_now.day+10000*dt_now.hour+100*dt_now.minute+dt_now.second)                
              





                    






