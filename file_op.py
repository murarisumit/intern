import draw
import file_op
import imghdr
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename


# we use deques so as to make Undo and Redo more efficient and avoid
# memory space isuues
# after each change, we append the new version of the image to
# the Undo queue
def undo(canvas):
    if len(canvas.data.undoQueue)>0:
        # the last element of the Undo Deque is the
        # current version of the image
        lastImage=canvas.data.undoQueue.pop()
        # we would want the current version if wehit redo after undo
        canvas.data.redoQueue.appendleft(lastImage)
    if len(canvas.data.undoQueue)>0:
        # the previous version of the image
        canvas.data.image=canvas.data.undoQueue[-1]
    file_op.save(canvas)
    canvas.data.imageForTk=draw.makeImageForTk(canvas)
    draw.drawImage(canvas)

def redo(canvas):
    if len(canvas.data.redoQueue)>0:
        canvas.data.image=canvas.data.redoQueue[0]
    save(canvas)
    if len(canvas.data.redoQueue)>0:
        # we remove this version from the Redo Deque beacuase it
        # has become our current image
        lastImage=canvas.data.redoQueue.popleft()
        canvas.data.undoQueue.append(lastImage)
    canvas.data.imageForTk=draw.makeImageForTk(canvas)
    draw.drawImage(canvas)

def saveAs(canvas):
    # ask where the user wants to save the file
    if canvas.data.image != None:
        filename=asksaveasfilename(defaultextension=".jpg")
        im = canvas.data.image
        im.save(filename)

def save(canvas):
    if canvas.data.image != None:
        im = canvas.data.image
        im.save(canvas.data.imageLocation)

def newImage(original_img,canvas):
    imageName = askopenfilename()
    filetype=""
    #make sure it's an image file
    filetype = imghdr.what(imageName)
    
    # restrict filetypes to .jpg, .bmp, etc.
    if filetype in ['jpeg', 'bmp', 'png', 'tiff']:
        canvas.data.imageLocation=imageName
        im= Image.open(imageName)
        canvas.data.image=im
        canvas.data.originalImage=im.copy()
        canvas.data.undoQueue.append(im.copy())
        canvas.data.imageSize=im.size #Original Image dimensions
        canvas.data.imageForTk=draw.makeImageForTk(canvas)
        draw.drawImage(canvas)
        original_img.data.imageLocation=imageName
        original_img.data.image=im
        original_img.data.originalImage=im.copy()
        original_img.data.imageSize=im.size #Original Image dimensions
        original_img.data.imageForTk=draw.makeImageForTk(original_img)
        draw.drawImage(original_img)
    else:
        messagebox.showinfo(title="Image File",\
        message="Choose an Image File!" , parent=canvas.data.mainWindow)
    olabel = tk.Label(original_img, text='ORIGINAL IMAGE', fg='white', bg='black')
    olabel.pack(side = tk.TOP)
    original_img.create_window(300, 490, window=olabel)  

