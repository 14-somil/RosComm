import serial
import json

class RosComm:
    msgType:dict
    serObj:serial.Serial

    def __init__(self, port = '/dev/ttyUSB0', baud = 115200):

        self.serObj = serial.Serial(port, baud)
        print(f"Node creted to communicate on {port} over baud {baud}.")

    def initPublisher(self, msgToSend:dict = {'data':0}) -> None:
        self.msgType = msgToSend
        print(f"Publisher created to send msg of type {self.msgType}.")

    def publish(self, msgToSend:dict = {'data':0}) -> None:

        #check keys
        if set(self.msgType.keys()) != set(msgToSend.keys()):
            print("The keys of Original dictionary doesn't match with the current one.")
            print("No message sent.")
            return
        
        #check data type
        for key in self.msgType:
            if type(self.msgType[key]) != type(msgToSend[key]):
                print(f"The data type of key: {key} does not match with the original.")
                print("No message sent.")
                return
            
        json_string = json.dumps(msgToSend)

        try:
            if not self.serObj.is_open:
                print("Serial port disconnected")
                return
            
            self.serObj.write(json_string.encode('utf-8'))

        except Exception as e:
            print(f"Exception: {e} occured.")
        