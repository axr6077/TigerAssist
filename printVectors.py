'''
@author : Ayush Rout
'''
import sys
import Leap

def crunch_vector(vector_item, buf):
    buf += '%f,%f,%f' % (vector_item.x, vector_item.y, vector_item.z)
    return buf

def crunch_vector_last(vector_item, buf):
    buf += '%f,%f,%f' % (vector_item.x, vector_item.y, vector_item.z)
    return buf

def extract_coords(vector_array, buf):
    for item in vector_array:
        buf += '%f,%f,%f'
    return buf

class LeapListener(Leap.Listener):
    startYet = 0
    buf = ""
    counter = 0
    done = 0

    def doneYet(self):
        return self.done
    def getBuf(self):
        self.buf = self.buf[:-1]
        self.buf += '\n'
        return self.buf
    def addTarget(self, target):
        self.buf = "%s," % target.strip()

    def addUtils(self):
        self.startYet = 1

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        print ("Exited")

    def on_frame(self, controller):
        frame = controller.frame()
        if self.startYet == 1 and self.counter < 29:
            distal_directions = []
            inter_directions = []
            promixal_directions = []
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
                    self.buf = extract_coords(distal_directions, self.buf)
                if inter_directions:
                    self.buf = extract_coords(inter_directions, self.buf)
                if promixal_directions:
                    self.buf = extract_coords(promixal_directions, self.buf)
                    self.buf = crunch_vector(hand_direction, self.buf)
                    self.buf = crunch_vector(arm_direction, self.buf)
            self.counter += 1

def main():
    f = open('../data/gestureDataLong4.csv', 'a')
    listener = LeapListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    print("Enter target for samples: ")
    currentTarget = sys.stdin.readline()
    listener.addTarget(currentTarget)

    print("Press <Enter> to start recording data... and again to exit!")
    sys.stdin.readline()
    listener.addUtils()

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        f.write(listener.getBuf())
        controller.remove_listener(listener)

if __name__ == '__main__':
    main()

#EOF