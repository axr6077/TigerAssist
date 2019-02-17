from tkinter import *
from leapMachineLearning import*

class Ctrl:
    def __init__(self, root):
        self.root = root
        self.view = View(root)
        self.model = Model(self)
