import tkinter as tk
import file_op
import filters
from filters import *

def menu_init(root, canvas):
    menubar=tk.Menu(root)
    # File pull-down Menu
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=lambda:file_op.newImage(canvas))
    filemenu.add_command(label="Save", command=lambda:file_op.save(canvas))
    filemenu.add_command(label="Save As", command=lambda:file_op.saveAs(canvas))
    menubar.add_cascade(label="File", menu=filemenu)

    # Edit pull-down Menu
    editmenu = tk.Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo   Z", command=lambda:file_op.undo(canvas))
    editmenu.add_command(label="Redo   Y", command=lambda:file_op.redo(canvas))
    menubar.add_cascade(label="Edit", menu=editmenu)
    root.config(menu=menubar)
    
    #Filter menu
    filtermenu = tk.Menu(menubar, tearoff=0)

    #Binary Morphology pull-down Menu
    bmormenu = tk.Menu(menubar, tearoff=0)
    bmormenu.add_command(label="Grassland", \
                           command=lambda:filters.identify_grass(canvas))
    bmormenu.add_command(label="Black and White", \
            command=lambda:filters.covertGray(canvas))  
    filtermenu.add_cascade(label="Binary-Morphology", menu=bmormenu)                    
  

    #Gray Level Morphology pull-down Menu
    gmormenu = tk.Menu(menubar, tearoff=0)
    gmormenu.add_command(label="dilation", \
                           command=lambda:filters.dilation(canvas))
    gmormenu.add_command(label="erosion", \
            command=lambda:filters.erosion(canvas))
    filtermenu.add_cascade(label="GrayLevel-Morphology", menu=gmormenu)   
    
    menubar.add_cascade(label="Filter", menu=filtermenu)            
    root.config(menu=menubar)


