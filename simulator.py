from vpython import *
from vpython.no_notebook import stop_server
from math import radians

class Simulator():
    #Auxiliary variables
    gripper = False
    counter = 0
    rotateAll = False

    #Setting scene and text in visualization
    scene = canvas(align = "left", width = 400, height = 600)
    gripText = wtext(pos = scene.title_anchor, text = "Chwytak jest w pozycji: <b>Otwartej</b>")

    def __init__(self):
        #Variables for dragging method
        self.drag = False
        self.mouseOrigin = vec(0, 0, 0)

        #Setting scene background color and deleting points of light
        self.scene.background = vec(1, 1, 1)
        self.scene.ambient = vec(1, 1, 1)
        self.scene.lights = []

        #Setting colors for each section
        self.colorBase = vec(128.0/255.0, 128.0/255.0, 128.0/255.0)
        self.colorElemC1 = vec(243.0/255.0, 12.0/255.0, 12.0/255.0)
        self.colorElemB2 = vec(12.0/255.0, 230.0/255.0, 12.0/255.0)
        self.colorElemB3 = vec(12.0/255.0, 12.0/255.0, 243.0/255.0)

        #Creating base
        sceneBaseShaft = cylinder(pos = vec(0, 0, 0), axis = vec(0, 5, 0), radius = 1, opacity = 0.2, color = self.colorBase)
        sceneBaseBall = sphere(pos = vec(0, 6, 0), radius = 2, opacity = 0.2, color = self.colorBase)

        #Creating method for dragging
        self.scene.bind('mousedown', self.down)
        self.scene.bind('mousemove', self.move)
        self.scene.bind('mouseup', self.up)

    #Method when hold down left mouse button on canvas
    def down(self):
        self.drag = True
        self.mouseOrigin = self.scene.mouse.pos

    #Method when move mouse cursor on cavas
    def move(self):
        if self.drag: # mouse button is down
            self.scene.camera.pos = self.scene.camera.pos - 0.1 * (self.scene.mouse.pos - self.mouseOrigin)

    #Method when release left mouse button on canvas
    def up(self):
        self.drag = False

    def initiatorLocal(self):
        #Create first element (C)
        elemCRightDownShaft = cylinder(pos = vec(1.5, 0, 0), axis = vec(1, 0, 0), radius = 1.2, color = self.colorElemC1)
        elemCLeftDownShaft = cylinder(pos = vec(-1.5, 0, 0), axis = vec(-1, 0, 0), radius = 1.2, color = self.colorElemC1)
        elemCRightConnector = box(pos = vec(2, 3.5, 0), size = vec(1, 7, 1), color = self.colorElemC1)
        elemCLeftConnector = box(pos = vec(-2, 3.5, 0), size = vec(-1, 7, 1), color = self.colorElemC1)
        elemCRightUpShaft = cylinder(pos = vec(1.5, 7, 0), axis = vec(1, 0, 0), radius = 1.2, color = self.colorElemC1)
        elemCLeftUpShaft = cylinder(pos = vec(-1.5, 7, 0), axis = vec(-1, 0, 0), radius = 1.2, color = self.colorElemC1)
        elemCBounding = sphere(pos = vec(0, 7, 0), radius = 2, opacity = 0.8, color = self.colorElemC1)
        elemC = compound([elemCRightDownShaft, elemCLeftDownShaft, elemCRightConnector, elemCLeftConnector,
                        elemCRightUpShaft, elemCLeftUpShaft, elemCBounding], origin = vec(0, 0, 0))
        elemC.pos = vec(0, 6, 0)
        #elemC.rotate(angle = pi/2, axis = vec(1, 0, 0), origin = vec(0, 6, 0))
                        
        #Create second element (B)
        elemBRightDownShaft = cylinder(pos = vec(0, 0, 1.5), axis = vec(0, 0, 1), radius = 1.2, color = self.colorElemB2)
        elemBLeftDownShaft = cylinder(pos = vec(0, 0, -1.5), axis = vec(0, 0, -1), radius = 1.2, color = self.colorElemB2)
        elemBRightConnector = box(pos = vec(0, 3.5, 1.5 + 0.5), size = vec(1, 7, 1), color = self.colorElemB2)
        elemBLeftConnector = box(pos = vec(0, 3.5, -1.5 - 0.5), size = vec(-1, 7, 1), color = self.colorElemB2)
        elemBRightUpShaft = cylinder(pos = vec(0, 7, 1.5), axis = vec(0, 0, 1), radius = 1.2, color = self.colorElemB2)
        elemBLeftUpShaft = cylinder(pos = vec(0, 7, -1.5), axis = vec(0, 0, -1), radius = 1.2, color = self.colorElemB2)
        elemBBounding = sphere(pos = vec(0, 7, 0), radius = 2, color = self.colorElemB2)
        elemB = compound([elemBRightDownShaft, elemBLeftDownShaft, elemBRightConnector, elemBLeftConnector,
                        elemBRightUpShaft, elemBLeftUpShaft, elemBBounding], origin = vec(0, 0, 0))
        elemB.pos = vec(0, 13, 0)
        #elemB.rotate(angle = pi/4, axis = vec(0, 0, 1), origin = elemB.pos)

        #Create third element (A)
        elemAShaft = cylinder(pos = vec(0, 0, 0), axis = vec(0, 7, 0), radius = 0.75, color = self.colorElemB3)
        elemABall = sphere(pos = vec(0, 7, 0), radius = 1, color = self.colorElemB3)
        elemADirection = cylinder(pos = vec(0, 7, 0), axis = vec(3, 0, 0), radius = 0.5, color = self.colorElemB3)
        elemA = compound([elemAShaft, elemABall, elemADirection], origin = vec(0, 0, 0))
        elemA.pos = vec(0, 20, 0)
        #elemA.rotate(angle = pi/4, axis = vec(0, 1, 0), origin = elemA.pos)

        #Create fourth element for trail
        tpc = sphere(pos = vec(3, 27, 0), radius = 1, opacity = 0.1)

        return [elemC, elemB, elemA, tpc]

    #Method that rotate all components relative to a 0, 0, 0 point
    def rotationLocal(self, joints, angles):
        joints[2].rotate(angle = angles[2], axis = joints[0].up, origin = joints[2].pos)
        joints[3].rotate(angle = angles[2], axis = joints[0].up, origin = joints[2].pos)

        joints[1].rotate(angle = angles[1], axis = cross(joints[0].axis, joints[0].up), origin = joints[1].pos)
        joints[2].rotate(angle = angles[1], axis = cross(joints[0].axis, joints[0].up), origin = joints[1].pos)
        joints[3].rotate(angle = angles[1], axis = cross(joints[0].axis, joints[0].up), origin = joints[1].pos)

        joints[0].rotate(angle = angles[0], axis = joints[0].axis, origin = joints[0].pos)
        joints[1].rotate(angle = angles[0], axis = joints[0].axis, origin = joints[0].pos)
        joints[2].rotate(angle = angles[0], axis = joints[0].axis, origin = joints[0].pos)
        joints[3].rotate(angle = angles[0], axis = joints[0].axis, origin = joints[0].pos)       

    #Debug method
    def rotationAll(self, b):
        self.rotateAll = not self.rotateAll
        if self.rotateAll:
            b.text = 'Stop All'
        else:
            b.text = 'Start All'

    def startSim(self):
        if __name__ == "__main__":
            button(text = 'Start All', bind = self.rotationAll)

        self.dt = 0.01
        self.jointsLocal = self.initiatorLocal()
        if __name__ == "__main__":
            self.anglesLocal = [0.0, 0.0, 0.0]
            self.anglesDtLocal = [0.76 * self.dt, 1.3 * self.dt, 2.1 * self.dt] #radians
            self.mulMatrixLocal = [1, 1, 1]

        #Making trail point and starting tracking
        trailLocal = attach_trail(self.jointsLocal[3], type = 'curve', radius = 0.1, color = vec(0, 0, 0), retain = 10)
        trailLocal.start()

    def oneTick(self, angles):
        #Visualization frame rate
        rate(1/self.dt)
            
        if __name__ == "__main__":
            if self.rotateAll:
                if abs(self.anglesLocal[0]) >= radians(135): self.mulMatrixLocal[0] = self.mulMatrixLocal[0] * -1
                if abs(self.anglesLocal[1]) >= radians(135): self.mulMatrixLocal[1] = self.mulMatrixLocal[1] * -1
                if abs(self.anglesLocal[2]) >= radians(350): self.mulMatrixLocal[2] = self.mulMatrixLocal[2] * -1
                    
                for i in range(0, 3):
                    self.anglesDtLocal[i] = self.anglesDtLocal[i] * self.mulMatrixLocal[i]
                        
                #angles = angles + anglesDt
                for i in range(0, 3):
                    self.anglesLocal[i] = self.anglesLocal[i] + self.anglesDtLocal[i]
                        
                self.rotationLocal(self.jointsLocal, self.anglesDtLocal)

        self.rotationLocal(self.jointsLocal, [-radians(angles[0]), radians(angles[1]), radians(angles[2])])

        #print(f"Angles3: {angles[3]}; Angles4: {angles[4]}")

        #Checking if user open wide his/her hand
        if angles[3] >= 500 and angles[4] >= 550 and self.counter > 10:
            self.gripper = not self.gripper
            self.counter = 0

        if self.gripper:
            self.gripText.text = "Chwytak jest w pozycji: <b>Zamkniętej</b>"
        else:
            self.gripText.text = "Chwytak jest w pozycji: <b>Otwartej</b>"

        if self.counter >= 30:
            self.counter = 30
        else:
            self.counter = self.counter + 1

        print(f"counter: {self.counter}")

    def stopped(self):
        stop_server()

if __name__ == "__main__":
    sim = Simulator()

    sim.startSim()
    while True:
        sim.oneTick([0, 0, 0, 0, 0])
