import serial.tools.list_ports

class ArduinoReader:
    def __init__(self):
        self.serialInst = serial.Serial()

        #Getting list of used ports
        ports = serial.tools.list_ports.comports()
        portList = []

        #Printing all of used ports
        for onePort in ports:
            portList.append(str(onePort))
            print(str(onePort))

        val = input("Select port: COM")

        #Checking for port that match the user input
        for x in range(0, len(portList)):
            if portList[x].startswith("COM" + str(val)):
                portVar = "COM" + str(val)
                print([portList[x]])

        #Setting for Serial port
        self.serialInst.baudrate = 9600
        self.serialInst.port = portVar
        self.serialInst.open()

    #Reading one line from Serial buffer
    def readLine(self, queue_):
        try:
            #angX;angY;angZ;force1;force2
            if self.serialInst.in_waiting:
                packet = self.serialInst.readline()
                if packet is not None:
                    decodePacket = packet.decode("utf").rstrip("\r\n")
                    dataString = decodePacket.split(";")
                    data = []
                    for x in dataString:
                        data.append(float(x))
                    if __name__ == '__main__':
                        print(data)
                    queue_.put(data)
        except:
            print("Something went wrong!")

if __name__ == '__main__':
    from queue import Queue
    ar = ArduinoReader()
    que = Queue()
    while True:
        ar.readLine(que)
