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

def init(root,fm,original_img, canvas):

    buttons.buttons_init(fm, canvas)
    menu.menu_init(root, original_img, canvas)
    canvas.data.image = None
    canvas.data.angleSelected=None
    canvas.data.rotateWindowClose=False
    canvas.data.endCrop=False
    canvas.data.drawOn=True

    canvas.data.undoQueue=deque([], 10)
    canvas.data.redoQueue=deque([], 10)
    canvas.pack()
    plabel = tk.Label(canvas, text='PROCESSED IMAGE', fg='white', bg='black')
    plabel.pack(side = tk.TOP)
    canvas.create_window(300, 490, window=plabel)  
    original_img.pack()

def run():
    # create the root and the canvas
    # https://stackoverflow.com/questions/24729119/what-does-calling-tk-actually-do
    root = tk.Tk()
    root.title("Morphological Filters")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    fm = tk.Frame(root, width=0.12 * width, height=height, bd=6, bg="green", relief = tk.SUNKEN)
    fm1=tk.Frame(root, width=0.44 * width, height=height, bd=1, bg="black")
    fm2 = tk.Frame(root, width=0.44 * width, height=height, bd=1, bg="black")
    fm.grid(row = 0, column = 0)
    fm1.grid(row = 0, column = 1)
    fm2.grid(row = 0, column = 2)
    # https://www.tutorialspoint.com/python/tk_canvas.htm
    canvasWidth = 600
    canvasHeight = 500
    original_img = tk.Canvas(fm1, width=canvasWidth, height=canvasHeight, \
                    background="white")
    canvas = tk.Canvas(fm2, width=canvasWidth, height=canvasHeight, \
                    background="white")
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width=canvasWidth
    canvas.data.height=canvasHeight
    canvas.data.mainWindow=fm2
    class Struct1: pass
    original_img.data = Struct1()
    original_img.data.width=canvasWidth
    original_img.data.height=canvasHeight
    original_img.data.mainWindow=fm1
    init(root,fm, original_img, canvas)
    root.bind("<Key>", lambda event:keyPressed(canvas, event))
    # and launch the app
    # https://stackoverflow.com/questions/8683217/when-do-i-need-to-call-mainloop-in-a-tkinter-application
    root.mainloop()  # This call BLOCKS (so your program waits)

run()
