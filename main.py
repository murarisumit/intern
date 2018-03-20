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

def init(root, fm_tools, orig_canvas, processed_canvas):

    buttons.buttons_init(fm_tools, processed_canvas)
    menu.menu_init(root, orig_canvas, processed_canvas)
    processed_canvas.data.image = None
    processed_canvas.data.angleSelected = None
    processed_canvas.data.rotateWindowClose = False
    processed_canvas.data.endCrop = False
    processed_canvas.data.drawOn = True

    processed_canvas.data.undoQueue=deque([], 10)
    processed_canvas.data.redoQueue=deque([], 10)
    processed_canvas.pack()
    plabel = tk.Label(processed_canvas, text='PROCESSED IMAGE', fg='white', bg='black')
    plabel.pack(side = tk.TOP)
    processed_canvas.create_window(300, 490, window=plabel)  
    orig_canvas.pack()

def run():
    # create the root and the canvas
    # https://stackoverflow.com/questions/24729119/what-does-calling-tk-actually-do
    root = tk.Tk()
    root.title("Morphological Filters")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    fm_tools = tk.Frame(root, width=0.12 * width, height=height, bd=6, bg="green", relief = tk.SUNKEN)
    fm_orig = tk.Frame(root, width=0.44 * width, height=height, bd=1, bg="black")
    fm_processed = tk.Frame(root, width=0.44 * width, height=height, bd=1, bg="black")
    fm_tools.grid(row = 0, column = 0)
    fm_orig.grid(row = 0, column = 1)
    fm_processed.grid(row = 0, column = 2)
    # https://www.tutorialspoint.com/python/tk_canvas.htm
    #TODO hardcoded height and width.
    canvasWidth = 600
    canvasHeight = 500
    orig_canvas = tk.Canvas(fm_orig, width=canvasWidth, height=canvasHeight, \
                    background="white")
    processed_canvas = tk.Canvas(fm_processed, width=canvasWidth, height=canvasHeight, \
                    background="white")
    # Set up canvas data and call init
    class Struct: pass
    processed_canvas.data = Struct()
    processed_canvas.data.width = canvasWidth
    processed_canvas.data.height = canvasHeight
    processed_canvas.data.mainWindow = fm_processed

    orig_canvas.data = Struct()
    orig_canvas.data.width = canvasWidth
    orig_canvas.data.height = canvasHeight
    orig_canvas.data.mainWindow = fm_orig
    init(root, fm_tools, orig_canvas, processed_canvas)
    #root.bind("<Key>", lambda event:keyPressed(processed_canvas, event))
    # and launch the app
    # https://stackoverflow.com/questions/8683217/when-do-i-need-to-call-mainloop-in-a-tkinter-application
    root.mainloop()  # This call BLOCKS (so your program waits)

run()
