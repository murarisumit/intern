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

    # Filter pull-down Menu
    filtermenu = tk.Menu(menubar, tearoff=0)
    filtermenu.add_command(label="Grassland", \
                           command=lambda:filters.identify_grass(canvas))
    filtermenu.add_command(label="Black and White", \
                           command=lambda:filters.covertGray(canvas))
    filtermenu.add_command(label="Sepia",\
                           command=lambda:filters.sepia(canvas))
    filtermenu.add_command(label="Invert", \
                           command=lambda:filters.invert(canvas))
    filtermenu.add_command(label="Solarize", \
                           command=lambda:filters.solarize(canvas))
    filtermenu.add_command(label="Posterize", \
                           command=lambda:filters.posterize(canvas))
    menubar.add_cascade(label="Filter", menu=filtermenu)
    root.config(menu=menubar)


