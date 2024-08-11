from arduinoReader import ArduinoReader
from simulator import Simulator
from queue import Queue
import time

measurementQueue = Queue()

ar = ArduinoReader()
sim = Simulator()
sim.startSim()

lastAngles = [0, 0, 0]

#Auxiliary methods
def auxReader():
    ar.readLine(measurementQueue) #[angleX, angleY, angleZ, force1 ,force2]

def dataProcessing():
    if measurementQueue.qsize() >= 1:
        measurement = measurementQueue.get()
        arduinoAngles = [measurement[0], measurement[1], measurement[2]]

        #Simulation move by angles diffrence between n and n+1 frame.
        dataForSim = [0, 0, 0]
        for i in range(0, 3):
            dataForSim[i] = arduinoAngles[i] - lastAngles[i]
            lastAngles[i] = arduinoAngles[i]

        #Adding force1 and force2 values to array
        dataForSim.extend([measurement[3], measurement[4]])
        sim.oneTick(dataForSim)
      
timeLimit = 600 #in seconds

ts = time.time()

#Program works for 10 minutes until finished 
while(time.time() - ts < timeLimit):
    try:
        auxReader()
        dataProcessing()
    except KeyboardInterrupt:
        break

sim.stopped()

print("Done")
