# RosComm

## Setup instructions

1. Clone the repository.
2. Navigate to the folder and open terminal
3. Run in terminal
    ```bash
    pip install .
    ```

## Example Code

```python
import RosComm

msgToSend = {
    "data" : ""
}

msgToRecieve = {
    "time" : 0
}

node = RosComm('/dev/ttyUSB0', 115200) #default port: "/dev/ttyUSB0" and baudrate: 115200

#define the type of message to recieve and send
node.initPublisher(msgToSend)
node.initSubscriber(msgToRecieve)

while True:
    node.publish({"data" : "Hello World"})

    print(node.getRecievedMessage()) #To get the last recived message

```