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