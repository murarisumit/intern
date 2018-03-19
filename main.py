import tkinter as tk
import os
import ctypes
from tkinter import messagebox as tkMessageBox
from collections import *

import menu
import buttons
from features import *
import file_op

############ INITIALIZE ##############

def init(root, canvas):

    buttons.buttons_init(root, canvas)
    menu.menu_init(root, canvas)
    canvas.data.image = None
    canvas.data.angleSelected=None
    canvas.data.rotateWindowClose=False
    canvas.data.brightnessWindowClose=False
    canvas.data.brightnessLevel=None
    canvas.data.histWindowClose=False
    canvas.data.solarizeWindowClose=False
    canvas.data.posterizeWindowClose=False
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.endCrop=False
    canvas.data.drawOn=True

    canvas.data.undoQueue=deque([], 10)
    canvas.data.redoQueue=deque([], 10)
    canvas.pack()

def run():
    # create the root and the canvas
    # https://stackoverflow.com/questions/24729119/what-does-calling-tk-actually-do
    root = tk.Tk()
    root.title("Morphological Filters")
    canvasWidth=500
    canvasHeight=500
    # https://www.tutorialspoint.com/python/tk_canvas.htm
    canvas =tk.Canvas(root, width=canvasWidth, height=canvasHeight, \
                    background="white")
    print(type(canvas))
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width=canvasWidth
    canvas.data.height=canvasHeight
    canvas.data.mainWindow=root
    init(root, canvas)
    root.bind("<Key>", lambda event:keyPressed(canvas, event))
    # and launch the app
    # https://stackoverflow.com/questions/8683217/when-do-i-need-to-call-mainloop-in-a-tkinter-application
    root.mainloop()  # This call BLOCKS (so your program waits)

run()
