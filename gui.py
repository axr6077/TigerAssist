'''
@author : Ayush Rout
'''
from tkinter import *
from leapMachineLearning import*

class Ctrl:
    def __init__(self, root):
        self.root = root
        self.view = View(root)
        self.model = Model(self)
        self.view.setSubtitle("TigerAssist")
        listener = assistListerner()
        controller = Leap.Controller()
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)

        listener.addUtils(self.model)
        controller.add_listener(listener)

        self.root.mainloop()
        print("Press enter to quit!")
        try:
            sys.stdin.readline()
        except KeyboardInterrupt:
            pass
        finally:
            controller.remove_listener(listener)

        def gotUpdates(self):
            self.view.setSubtitle(self.model.getText())

class Model():

    def __int__(self, ctrl):
        self.ctrl = ctrl
        self.txt = "TigerAssist"

    def getText(self):
        return self.txt

    def textChanged(self, text):
        if (len(self.txt)) < 50:
            self.txt = self.txt + text
        else:
            self.txt = text
        self.ctrl.gotUpdates()

    def clearText(self):
        self.txt = ''
        self.ctrl.gotUpdates()

class View:
    def loadView(self):
        self.subtitle = Label (self.ctrl, font = ('Helvetica', '36'), fg = 'gray30', bg = 'gray32', anchor = S, pady = 50)
        self.subtitle.master.wm_attributes("-topmost", True)
        self.subtitle.master.wm_attributes("-transparentcolor", "gray32")
        self.subtitle.pack(fill = BOTH, expand = 1, side = BOTTOM)

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.loadView()

    def setSubtitle(self, txt):
        self.subtitle.configure(text = txt)

def go():
    root = Tk()
    root.title('TigerAssist')
    root.attributes("-fullscreen", True)
    app = Ctrl(root)

#EOF


