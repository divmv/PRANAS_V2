from datetime import datetime
import os
import pathlib
import pandas as pd

class LogFileManage:
        def __init__(self,currentService):
                #Creating and Initializing Log File to which all the session information is written.
                self.currentService=currentService
                self.log_file_name='Log_'+str(self.currentService.trialParameters.UID)+\
                                        '_T'+str(self.currentService.trialParameters.TRIAL)+\
                                        '_'+currentService.trialParameters.MODE+\
                                        '_'+currentService.GetCurrentTime(3)+'.log'
                self.WriteLog('Log started on ' + self.currentService.GetCurrentTime(2), 0)
                self.WriteLog('Initialized local system at ' + self.currentService.GetCurrentTime(1), 0)
                self.currentService=currentService

        def WriteLog(self, writeString, tpe):
                # Writes any string passed as argument to the session's log file opened initially
                if tpe==0:
                        writeString=writeString
                elif tpe==1:
                        writeString=self.currentService.GetCurrentTime(1)+':'+str(writeString)
                
                print(writeString)
                self.logFileFolder=os.path.abspath(os.getcwd())+'//logs'
                self.log_file = open(os.path.join(self.logFileFolder,self.log_file_name),"a")
                self.log_file.writelines(writeString+"\n")
                self.log_file.close()
        
class DataFileManage:
        def __init__(self,currentService):
                self.currentService=currentService
                self.data_file_name='Data_'+str(self.currentService.trialParameters.UID)+\
                                        '_T'+str(self.currentService.trialParameters.TRIAL)+\
                                        '_'+currentService.trialParameters.MODE+\
                                        '_'+currentService.GetCurrentTime(3)+'.csv'
                self.RecordDataFolder=os.path.join(os.getcwd(),'RecordedData')
        def Write2CSV(self,dataFrame):
                dataFrame.to_csv(os.path.join(self.RecordDataFolder,self.data_file_name),index=True,header=True)
        
        def ReadFrmCSV(self,fileName):
                return pd.read_csv(fileName)

        # self.data_file_name="Data_"+str(UID)+'_T'+str(TrialNo)+'_'+Mode

class DataTransfer:
    def __init__(self):
        self
