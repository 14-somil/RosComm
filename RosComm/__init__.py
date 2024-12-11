import serial
import json
import threading
import time

class RosComm:
    msgTypeSent:dict
    msgTypeRecieved:dict
    serObj:serial.Serial
    port:str
    baud:int
    lock:threading.Lock

    def __init__(self, port = '/dev/ttyUSB0', baud = 115200):
        try:
            self.port = port
            self.baud = baud
            self.serObj = serial.Serial(port, baud, timeout=1)
            self.lock = threading.Lock()
            print(f"Node created to communicate on {port} over baud {baud}.")
        except serial.SerialException as e:
            print(f"Could not open serial port: {e}")
            raise

    def initPublisher(self, msgToSend:dict = {'data':0}) -> None:
        self.msgTypeSent = msgToSend
        print(f"Publisher created to send msg of type {self.msgTypeSent}.")

    def publish(self, msgToSend:dict = {'data':0}) -> None:

        #check keys
        if set(self.msgTypeSent.keys()) != set(msgToSend.keys()):
            print("The keys of Original dictionary doesn't match with the current one.")
            print("No message sent.")
            return
        
        #check data type
        for key in self.msgTypeSent:
            if type(self.msgTypeSent[key]) != type(msgToSend[key]):
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
        
    def initSubscriber(self, msgToRecieve:dict = {'data':0}):
        self.msgTypeRecieved = msgToRecieve
        print(f"Subcriber initialized of type {self.msgTypeRecieved}")

        def subThread():
            print("Subscriber thread initialised")
            while True:

                try: 
                    if not self.serObj.is_open:
                        time.sleep(1)
                        continue
                    
                    if self.serObj.in_waiting > 0:
                        json_string = self.serObj.readline().decode('utf-8').strip()
                        
                        try:
                            recievedMsg = json.loads(json_string)
                        except json.JSONDecodeError:
                            print("Error decoding JSON data.")
                            continue

                        if set(recievedMsg.keys()) != set(self.msgTypeRecieved.keys()):
                            print("The keys of Original dictionary doesn't match with the current one.")
                            print("Skipping this message.")
                            continue
                        
                        for key in recievedMsg:
                            if type(recievedMsg[key]) != type(self.msgTypeRecieved[key]):
                                print(f"The data type of key: {key} does not match with the original.")
                                print("Skipping this message.")
                                continue
                        
                        with self.lock:
                            self.msgTypeRecieved = recievedMsg
                    
                    time.sleep(0.01)
                except Exception as e:
                    print(f"Error in subscriber thread: {e}")
                    time.sleep(1)        
        thread = threading.Thread(target=subThread)
        thread.daemon = True
        thread.start()

    def getReceivedMessage(self):
        with self.lock:
            return self.msgTypeRecieved
        
    def close(self):

        if self.serObj and self.serObj.is_open:
            self.serObj.close()
            print(f"Serial port {self.port} closed.")