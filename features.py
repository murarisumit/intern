import draw
import file_op
from PIL import Image, ImageDraw, ImageOps
import tkinter as tk
from tkinter import messagebox as tkMessageBox


def closeHistWindow(canvas):

    if canvas.data.image!=None:
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.histWindowClose=True

def histogram(canvas):

    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    histWindow=tk.Toplevel(canvas.data.mainWindow)
    histWindow.title("Histogram")
    canvas.data.histCanvasWidth=350
    canvas.data.histCanvasHeight=475
    histCanvas = tk.Canvas(histWindow, width=canvas.data.histCanvasWidth, \
                        height=canvas.data.histCanvasHeight)
    histCanvas.pack()
    # provide sliders to the user to manipulate red, green and blue amounts in the image
    redSlider=tk.Scale(histWindow, from_=-100, to=100, \
                    orient=tk.HORIZONTAL, label="R")
    redSlider.pack()
    blueSlider=tk.Scale(histWindow, from_=-100, to=100,\
                     orient=tk.HORIZONTAL, label="B")
    blueSlider.pack()
    greenSlider=tk.Scale(histWindow, from_=-100, to=100,\
                      orient=tk.HORIZONTAL, label="G")
    greenSlider.pack()
    OkHistFrame=tk.Frame(histWindow)
    OkHistButton=tk.Button(OkHistFrame, text="OK", \
                        command=lambda: closeHistWindow(canvas))
    OkHistButton.grid(row=0,column=0)
    OkHistFrame.pack(side=tk.BOTTOM)
    initialRGB=(0,0,0)
    changeColours(canvas, redSlider, blueSlider, \
                  greenSlider, histWindow, histCanvas, initialRGB)

def changeColours(canvas, redSlider, blueSlider, \
                  greenSlider, histWindow, histCanvas, previousRGB):

    if canvas.data.histWindowClose==True:
        histWindow.destroy()
        canvas.data.histWindowClose=False
    else:
        # the slider value indicates the % by which the red/green/blue
        # value of the pixels of the image need to incresed (for +ve values)
        # or decreased (for -ve values)
        if canvas.data.image!=None and histWindow.winfo_exists() :
            R, G, B= canvas.data.image.split()
            sliderValR=redSlider.get()
            (previousR, previousG, previousB)= previousRGB
            scaleR=(sliderValR-previousR)/100.0
            R=R.point(lambda i: i+ int(round(i*scaleR)))
            sliderValG=greenSlider.get()
            scaleG=(sliderValG-previousG)/100.0
            G=G.point(lambda i: i+ int(round(i*scaleG)))
            sliderValB=blueSlider.get()
            scaleB=(sliderValB-previousB)/100.0
            B=B.point(lambda i: i+ int(round(i*scaleB)))
            canvas.data.image = Image.merge(canvas.data.image.mode, (R, G, B))

            canvas.data.imageForTk=draw.makeImageForTk(canvas)
            draw.drawImage(canvas)
            displayHistogram(canvas, histWindow, histCanvas)
            previousRGB=(sliderValR, sliderValG, sliderValB)
            canvas.after(200, lambda: changeColours(canvas, redSlider,\
                blueSlider, greenSlider,  histWindow, histCanvas, previousRGB))

def displayHistogram(canvas,histWindow, histCanvas):

    histCanvasWidth=canvas.data.histCanvasWidth
    histCanvasHeight=canvas.data.histCanvasHeight
    margin=50
    if canvas.data.image!=None:
        histCanvas.delete(tk.ALL)
        im=canvas.data.image
        #x-axis
        histCanvas.create_line(margin-1, histCanvasHeight-margin+1,\
                               margin-1+ 258, histCanvasHeight-margin+1)
        xmarkerStart=margin-1
        for i in range(0,257,64):
            xmarker="%d" % (i)
            histCanvas.create_text(xmarkerStart+i,\
                                   histCanvasHeight-margin+7, text=xmarker)
        #y-axis
        histCanvas.create_line(margin-1, \
                               histCanvasHeight-margin+1, margin-1, margin)
        ymarkerStart= histCanvasHeight-margin+1
        for i in range(0, histCanvasHeight-2*margin+1, 50):
            ymarker="%d" % (i)
            histCanvas.create_text(margin-1-10,\
                                   ymarkerStart-i, text=ymarker)

        R, G, B=im.histogram()[:256], im.histogram()[256:512], \
                 im.histogram()[512:768]
        for i in range(len(R)):
            pixelNo=R[i]
            histCanvas.create_oval(i+margin, \
                            histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,\
                            histCanvasHeight-pixelNo/100.0+1-margin, \
                                   fill="red", outline="red")
        for i in range(len(G)):
            pixelNo=G[i]
            histCanvas.create_oval(i+margin, \
                            histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,\
                            histCanvasHeight-pixelNo/100.0+1-margin, \
                                   fill="green", outline="green")
        for i in range(len(B)):
            pixelNo=B[i]
            histCanvas.create_oval(i+margin,\
                            histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,\
                            histCanvasHeight-pixelNo/100.0+1-margin,\
                                   fill="blue", outline="blue")

def colourPop(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=True
    canvas.data.drawOn=False
    tkMessageBox.showinfo(title="Colour Pop", message="Click on a part of the image which you want in colour" , parent=canvas.data.mainWindow)
    if canvas.data.cropPopToHappen==False:
        canvas.data.mainWindow.bind("<ButtonPress-1>", lambda event: getPixel(event, canvas))

def getPixel(event, canvas):
    # have to check if Colour Pop button is pressed or not, otherwise, the root
    # events which point to different functions based on what button has been
    # pressed will get mixed up
    try: # to avoid confusion between the diffrent events
        # asscoaited with crop and colourPop
        if canvas.data.colourPopToHappen==True and \
           canvas.data.cropPopToHappen==False and canvas.data.image!=None :
            data=[]
            # catch the location of the pixel selected by the user
            # multiply it by the scale to get pixel's olaction of the
            #actual image
            canvas.data.pixelx=\
            int(round((event.x-canvas.data.imageTopX)*canvas.data.imageScale))
            canvas.data.pixely=\
            int(round((event.y-canvas.data.imageTopY)*canvas.data.imageScale))
            pixelr, pixelg, pixelb= \
            canvas.data.image.getpixel((canvas.data.pixelx, canvas.data.pixely))
            # the amount of deviation allowed from selected pixel's value
            tolerance=60
            for y in range(canvas.data.image.size[1]):
                for x in range(canvas.data.image.size[0]):
                    r, g, b= canvas.data.image.getpixel((x, y))
                    avg= int(round((r + g + b)/3.0))
                    # if the deviation of each pixel value > tolerance,
                    # make them gray else keep them coloured
                    if (abs(r-pixelr)>tolerance or
                        abs(g-pixelg)>tolerance or
                        abs(b-pixelb)>tolerance ):
                        R, G, B= avg, avg, avg
                    else:
                        R, G, B=r,g,b
                    data.append((R, G, B))
            canvas.data.image.putdata(data)
            file_op.save(canvas)
            canvas.data.undoQueue.append(canvas.data.image.copy())
            canvas.data.imageForTk=draw.makeImageForTk(canvas)
            draw.drawImage(canvas)
    except:
        pass
    canvas.data.colourPopToHappen=False

def crop(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    # have to check if crop button is pressed or not, otherwise,
    # the root events which point to
    # different functions based on what button has been pressed
    # will get mixed up
    canvas.data.cropPopToHappen=True
    tkMessageBox.showinfo(title="Crop", \
                          message="Draw cropping rectangle and press Enter" ,\
                          parent=canvas.data.mainWindow)
    if canvas.data.image!=None:
        canvas.data.mainWindow.bind("<ButtonPress-1>", \
                                    lambda event: startCrop(event, canvas))
        canvas.data.mainWindow.bind("<B1-Motion>",\
                                    lambda event: drawCrop(event, canvas))
        canvas.data.mainWindow.bind("<ButtonRelease-1>", \
                                    lambda event: endCrop(event, canvas))

def startCrop(event, canvas):
    # detects the start of the crop rectangle
    if canvas.data.endCrop==False and canvas.data.cropPopToHappen==True:
        canvas.data.startCropX=event.x
        canvas.data.startCropY=event.y

def drawCrop(event,canvas):
    # keeps extending the crop rectange as the user extends
    # his desired crop rectangle
    if canvas.data.endCrop==False and canvas.data.cropPopToHappen==True:
        canvas.data.tempCropX=event.x
        canvas.data.tempCropY=event.y
        canvas.create_rectangle(canvas.data.startCropX, \
                                canvas.data.startCropY,
                                 canvas.data.tempCropX, \
            canvas.data.tempCropY, fill="gray", stipple="gray12", width=0)

def endCrop(event, canvas):
    # set canvas.data.endCrop=True so that button pressed movements
    # are not caught anymore but set it to False when "Enter"
    # is pressed so that crop can be performed another time too
    if canvas.data.cropPopToHappen==True:
        canvas.data.endCrop=True
        canvas.data.endCropX=event.x
        canvas.data.endCropY=event.y
        canvas.create_rectangle(canvas.data.startCropX, \
                                canvas.data.startCropY,
                                 canvas.data.endCropX, \
            canvas.data.endCropY, fill="gray", stipple="gray12", width=0 )
        canvas.data.mainWindow.bind("<Return>", \
                                lambda event: performCrop(event, canvas))

def performCrop(event,canvas):
    canvas.data.image=\
    canvas.data.image.crop(\
    (int(round((canvas.data.startCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
    int(round((canvas.data.startCropY-canvas.data.imageTopY)*canvas.data.imageScale)),
    int(round((canvas.data.endCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
    int(round((canvas.data.endCropY-canvas.data.imageTopY)*canvas.data.imageScale))))
    canvas.data.endCrop=False
    canvas.data.cropPopToHappen=False
    file_op.save(canvas)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=draw.makeImageForTk(canvas)
    draw.drawImage(canvas)

def rotateFinished(canvas, rotateWindow, rotateSlider, previousAngle):
    if canvas.data.rotateWindowClose==True:
        rotateWindow.destroy()
        canvas.data.rotateWindowClose=False
    else:
        if canvas.data.image!=None and rotateWindow.winfo_exists():
            canvas.data.angleSelected=rotateSlider.get()
            if canvas.data.angleSelected!= None and \
               canvas.data.angleSelected!= previousAngle:
                canvas.data.image=\
                canvas.data.image.rotate(float(canvas.data.angleSelected))
                canvas.data.imageForTk=draw.makeImageForTk(canvas)
                draw.drawImage(canvas)
        canvas.after(200, lambda:rotateFinished(canvas,\
                    rotateWindow, rotateSlider, canvas.data.angleSelected) )

def closeRotateWindow(canvas):
    if canvas.data.image!=None:
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.rotateWindowClose=True

def rotate(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    rotateWindow=tk.Toplevel(canvas.data.mainWindow)
    rotateWindow.title("Rotate")
    rotateSlider=tk.Scale(rotateWindow, from_=0, to=360, orient=tk.HORIZONTAL)
    rotateSlider.pack()
    OkRotateFrame=tk.Frame(rotateWindow)
    OkRotateButton=tk.Button(OkRotateFrame, text="OK",\
                          command=lambda: closeRotateWindow(canvas))
    OkRotateButton.grid(row=0,column=0)
    OkRotateFrame.pack(side=tk.BOTTOM)
    rotateFinished(canvas, rotateWindow, rotateSlider, 0)

def closeBrightnessWindow(canvas):
    if canvas.data.image!=None:
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.brightnessWindowClose=True

def changeBrightness(canvas, brightnessWindow, brightnessSlider, \
                     previousVal):
    if canvas.data.brightnessWindowClose==True:
        brightnessWindow.destroy()
        canvas.data.brightnessWindowClose=False

    else:
        # increasing pixel values according to slider value increases
        #brightness we change ot according to the difference between the
        # previous value and the current slider value
        if canvas.data.image!=None and brightnessWindow.winfo_exists():
            sliderVal=brightnessSlider.get()
            scale=(sliderVal-previousVal)/100.0
            canvas.data.image=canvas.data.image.point(\
                lambda i: i+ int(round(i*scale)))
            canvas.data.imageForTk=draw.makeImageForTk(canvas)
            draw.drawImage(canvas)
            canvas.after(200, \
            lambda: changeBrightness(canvas, brightnessWindow, \
                                     brightnessSlider, sliderVal))

def brightness(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    brightnessWindow=tk.Toplevel(canvas.data.mainWindow)
    brightnessWindow=tk.title("Brightness")
    brightnessSlider=tk.Scale(brightnessWindow, from_=-100, to=100,\
                           orient=tk.HORIZONTAL)
    brightnessSlider.pack()
    OkBrightnessFrame=tk.Frame(brightnessWindow)
    OkBrightnessButton=tk.Button(OkBrightnessFrame, text="OK", \
                              command=lambda: closeBrightnessWindow(canvas))
    OkBrightnessButton.grid(row=0,column=0)
    OkBrightnessFrame.pack(side=tk.BOTTOM)
    changeBrightness(canvas, brightnessWindow, brightnessSlider,0)
    brightnessSlider.set(0)

def reset(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    ### change back to original image
    if canvas.data.image!=None:
        canvas.data.image=canvas.data.originalImage.copy()
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=draw.makeImageForTk(canvas)
        draw.drawImage(canvas)

def mirror(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.mirror(canvas.data.image)
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=draw.makeImageForTk(canvas)
        draw.drawImage(canvas)

def flip(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.flip(canvas.data.image)
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=draw.makeImageForTk(canvas)
        draw.drawImage(canvas)

def transpose(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    # I treated the image as a continuous list of pixel values row-wise
    # and simply excnaged the rows and the coloums
    # in oder to make it rotate clockewise, I reversed all the rows
    if canvas.data.image!=None:
        imageData=list(canvas.data.image.getdata())
        newData=[]
        newimg=Image.new(canvas.data.image.mode,\
                (canvas.data.image.size[1], canvas.data.image.size[0]))
        for i in range(canvas.data.image.size[0]):
            addrow=[]
            for j in range(i, len(imageData), canvas.data.image.size[0]):
                addrow.append(imageData[j])
            addrow.reverse()
            newData+=addrow
        newimg.putdata(newData)
        canvas.data.image=newimg.copy()
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=draw.makeImageForTk(canvas)
        draw.drawImage(canvas)

def identify_grass():
    '''
    This feature will be used to identify grass in a picture
    '''
    pass
