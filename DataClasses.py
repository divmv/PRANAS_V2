from dataclasses import dataclass



@dataclass
class TrialParameters:
        SAMPLING_RATE: int =1000
        BUFFER_SIZE: int = 1000
        RECORD_DURATION: int =10
        UID: str = "Test"
        TRIAL: int = 1
        USER: str ="Computer"
        MODE:str="Combined"
        PORT_Server: int = 9001
        IP_Server: str = "192.168.137.1"
        SEQUENCE="0, 1, 0, 1, 0, 1, 0"
        SEQUENCE_DURATION="20,30,20,30,20,20,20"

@dataclass

class DeviceFlags:
        # Do not change the values
        START_FLAG: bool = False
        CONFIGURE_FLAG: bool = False
        STOP_FLAG:bool = False
        CONNECTION_FLAG:bool =False
        DAQ_SET:bool=False
        SEND_FILE:bool=False

        


