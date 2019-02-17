'''
@author : Ayush Rout
'''
import os, sys, inspect, threading, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path += ["/../lib/Leap", "../lib/x64", "../lib"]
import Leap
from MatchMachineLearning import *

def vector_extract(vector_item, buf):
    buf.append(vector_item.x)
    buf.append(vector_item.y)
    buf.append(vector_item.z)
    return buf

def multi_vector_extract(vector_array, buf):
    for item in vector_array:
        buf.append(item.x)
        buf.append(item.y)
        buf.append(item.z)
    return buf

class assistListerner(Leap.Listener):
    buf = []
    frameCount = 0
    resultCount = 0
    passedThree = 0
    previousResult = " "
    previousPrintChar = ""
    printedSpace = False
    staticLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    def addUtils(self, model):
        self.report = model

    def on_init(self, controller):
        print("Initialized")
        getGestureDataFromFile()

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        frame = controller.frame()
        distal_directions = []
        inter_directions = []
        promixal_directions = []
        if not frame.hands.is_empty:
            for hand in frame.hands:
                handType = "Left Hand" if hand.is_left else "Right Hand"
                activeHand = frame.hands.frontmost
                activeArm = activeHand.arm
                arm_direction = activeArm.direction
                hand_direction = activeHand.direction

                for finger in activeHand.fingers:
                    distal_directions.append(finger.bone(3).direction)
                    inter_directions.append(finger.bone(2).direction)
                    promixal_directions.append(finger.bone(1).direction)

                if distal_directions:
                    self.buf = multi_vector_extract(distal_directions, self.buf)
                if inter_directions:
                    self.buf = multi_vector_extract(inter_directions, self.buf)
                if promixal_directions:
                    self.buf = multi_vector_extract(promixal_directions, self.buf)
                    self.buf = vector_extract(hand_direction, self.buf)
                    self.buf = vector_extract(arm_direction, self.buf)
                    result = ""
                    if(len(self.buf)) == 1479:
                        result = compareMachine.matchGesture(np.array(self.buf))
                        if not result == ' ' and not result == '':
                            print(result)
                        self.frameCount = 0
                    else:
                        print("Not enough data")

                    if (len(self.buf)) >= 1479:
                        self.buf = self.buf[51:]

                    if (result == self.previousResult):
                        self.resultCount += 1
                    else:
                        self.resultCount = 0
                        self.previousResult = result
                    if result in self.staticLetters:
                        if self.resultCount == 10:
                            self.resultCount = False
                            self.report.textChanged(result)
                            self.resultCount = 0
                    else:
                        if not self.previousPrintChar == result:
                            self.printedSpace = False
                            self.report.textChanged(result)
                            self.previousPrintChar = result
                    print("\n")

            else:
                List = [0.0] * 51
                self.buf = self.buf + List
                del List[:]
                self.buf = self.buf[51:]
                self.frameCount += 1

                if(self.frameCount == 37):
                    self.passedThree += 1
                    self.frameCount = 0
                if (self.passedThree == 15):
                    self.passedThree = 0
                    self.report.clearText()
                if self.printedSpace == False and self.passedThree == 2:
                    self.printedSpace = True
                    self.report.textChanged(' ')
                    self.previousPrintChar = ' '
                else:
                    self.previousResult = ''
                    self.previousPrintChar = ''
#EOF