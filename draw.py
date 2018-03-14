import file_op
from PIL import Image, ImageDraw
from PIL import ImageTk
from PIL import ImageOps
import tkinter as tk



def drawOnImage(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=True
    drawWindow=tk.Toplevel(canvas.data.mainWindow)
    drawWindow.title="Draw"
    drawFrame=tk.Frame(drawWindow)
    redButton=tk.Button(drawFrame, bg="red", width=2, \
                     command=lambda: colourChosen(drawWindow,canvas, "red"))
    redButton.grid(row=0,column=0)
    blueButton=tk.Button(drawFrame, bg="blue", width=2,\
                      command=lambda: colourChosen(drawWindow,canvas, "blue"))
    blueButton.grid(row=0,column=1)
    greenButton=tk.Button(drawFrame, bg="green",width=2, \
                       command=lambda: colourChosen(drawWindow,canvas, "green"))
    greenButton.grid(row=0,column=2)
    magentaButton=tk.Button(drawFrame, bg="magenta", width=2,\
                         command=lambda: colourChosen(drawWindow,canvas, "magenta"))
    magentaButton.grid(row=1,column=0)
    cyanButton=tk.Button(drawFrame, bg="cyan", width=2,\
                      command=lambda: colourChosen(drawWindow,canvas, "cyan"))
    cyanButton.grid(row=1,column=1)
    yellowButton=tk.Button(drawFrame, bg="yellow",width=2,\
                        command=lambda: colourChosen(drawWindow,canvas, "yellow"))
    yellowButton.grid(row=1,column=2)
    orangeButton=tk.Button(drawFrame, bg="orange", width=2,\
                        command=lambda: colourChosen(drawWindow,canvas, "orange"))
    orangeButton.grid(row=2,column=0)
    purpleButton=tk.Button(drawFrame, bg="purple",width=2, \
                        command=lambda: colourChosen(drawWindow,canvas, "purple"))
    purpleButton.grid(row=2,column=1)
    brownButton=tk.Button(drawFrame, bg="brown",width=2,\
                       command=lambda: colourChosen(drawWindow,canvas, "brown"))
    brownButton.grid(row=2,column=2)
    blackButton=tk.Button(drawFrame, bg="black",width=2,\
                       command=lambda: colourChosen(drawWindow,canvas, "black"))
    blackButton.grid(row=3,column=0)
    whiteButton=tk.Button(drawFrame, bg="white",width=2, \
                       command=lambda: colourChosen(drawWindow,canvas, "white"))
    whiteButton.grid(row=3,column=1)
    grayButton=tk.Button(drawFrame, bg="gray",width=2,\
                      command=lambda: colourChosen(drawWindow,canvas, "gray"))
    grayButton.grid(row=3,column=2)
    drawFrame.pack(side=tk.BOTTOM)

def colourChosen(drawWindow, canvas, colour):
    if canvas.data.image!=None:
        canvas.data.drawColour=colour
        canvas.data.mainWindow.bind("<B1-Motion>",\
                                    lambda event: drawDraw(event, canvas))
    drawWindow.destroy()

def drawDraw(event, canvas):
    if canvas.data.drawOn==True:
        x=int(round((event.x-canvas.data.imageTopX)*canvas.data.imageScale))
        y=int(round((event.y-canvas.data.imageTopY)*canvas.data.imageScale))
        draw = ImageDraw.Draw(canvas.data.image)
        draw.ellipse((x-3, y-3, x+ 3, y+3), fill=canvas.data.drawColour,\
                     outline=None)
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

######################## FEATURES ###########################

############### FILTERS ######################


################ EDIT MENU FUNCTIONS ############################

def keyPressed(canvas, event):
    if event.keysym=="z":
        file_op.undo(canvas)
    elif event.keysym=="y":
        file_op.redo(canvas)

############# MENU COMMANDS ################


######## CREATE A VERSION OF IMAGE TO BE DISPLAYED ON THE CANVAS #########

def makeImageForTk(canvas):
    im=canvas.data.image
    if canvas.data.image!=None:
        # Beacuse after cropping the now 'image' might have diffrent
        # dimensional ratios
        imageWidth=canvas.data.image.size[0]
        imageHeight=canvas.data.image.size[1]
        #To make biggest version of the image fit inside the canvas
        if imageWidth>imageHeight:
            resizedImage=im.resize((canvas.data.width,\
                int(round(float(imageHeight)*canvas.data.width/imageWidth))))
            # store the scale so as to use it later
            canvas.data.imageScale=float(imageWidth)/canvas.data.width
        else:
            resizedImage=im.resize((int(round(float(imageWidth)*canvas.data.height/imageHeight)),\
                                    canvas.data.height))
            canvas.data.imageScale=float(imageHeight)/canvas.data.height
        # we may need to refer to ther resized image atttributes again
        canvas.data.resizedIm=resizedImage
        return ImageTk.PhotoImage(resizedImage)

def drawImage(canvas):
    if canvas.data.image!=None:
        # make the canvas center and the image center the same
        canvas.create_image(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0,
                        canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0,
                            anchor=tk.NW, image=canvas.data.imageForTk)
        canvas.data.imageTopX=int(round(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0))
        canvas.data.imageTopY=int(round(canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0))
