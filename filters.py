import cv2
import draw
import file_op
import numpy as np
from PIL import Image, ImageOps
import preprocess
import tkinter as tk


def covertGray(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    #### The existing method to convert to a grayscale image converts the ####
    ####         image mode, so I used my own function to convert         ####
    # value of each channel of a pixel is set to the average of the original
    # values of the channels
    if canvas.data.image!=None:
        data=[]
        for col in range(canvas.data.image.size[1]):
            for row in range(canvas.data.image.size[0]):
                r, g, b= canvas.data.image.getpixel((row, col))
                avg= int(round((r + g + b)/3.0))
                R, G, B= avg, avg, avg
                data.append((R, G, B))
        canvas.data.image.putdata(data)
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=draw.makeImageForTk(canvas)
        draw.drawImage(canvas)

def sepia(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    # this method first converts the image to B&W and then adds the
    # same amount of red and green to every pixel
    if canvas.data.image!=None:
        sepiaData=[]
        for col in range(canvas.data.image.size[1]):
            for row in range(canvas.data.image.size[0]):
                r, g, b= canvas.data.image.getpixel((row, col))
                avg= int(round((r + g + b)/3.0))
                R, G, B= avg+100, avg+50, avg
                sepiaData.append((R, G, B))
        canvas.data.image.putdata(sepiaData)
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=draw.makeImageForTk(canvas)
        draw.drawImage(canvas)

def invert(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.invert(canvas.data.image)
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=draw.makeImageForTk(canvas)
        draw.drawImage(canvas)

def solarize(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    solarizeWindow=tk.Toplevel(canvas.data.mainWindow)
    solarizeWindow.title("Solarize")
    solarizeSlider=tk.Scale(solarizeWindow, from_=0, to=255, orient=tk.HORIZONTAL)
    solarizeSlider.pack()
    OkSolarizeFrame=tk.Frame(solarizeWindow)
    OkSolarizeButton=tk.Button(OkSolarizeFrame, text="OK",\
                            command=lambda: closeSolarizeWindow(canvas))
    OkSolarizeButton.grid(row=0,column=0)
    OkSolarizeFrame.pack(side=tk.BOTTOM)
    ### beacsue intial silderVal=0
    performSolarize(canvas, solarizeWindow, solarizeSlider, 255)

def performSolarize(canvas, solarizeWindow, solarizeSlider, previousThreshold):

    if canvas.data.solarizeWindowClose==True:
        solarizeWindow.destroy()
        canvas.data.solarizeWindowClose=False

    else:
        # the  slider denotes the % of solarization thta the user wants,
        # so the threshold (above which pixels are inverted) is inversely
        # related to the slider value
        if solarizeWindow.winfo_exists():
            sliderVal=solarizeSlider.get()
            threshold_=255-sliderVal
            if canvas.data.image!=None and threshold_!=previousThreshold:
                canvas.data.image=ImageOps.solarize(canvas.data.image,\
                                                    threshold=threshold_)
                canvas.data.imageForTk=draw.makeImageForTk(canvas)
                draw.drawImage(canvas)
            canvas.after(200, lambda: performSolarize(canvas, \
                                solarizeWindow, solarizeSlider, threshold_))

def closeSolarizeWindow(canvas):

    if canvas.data.image!=None:
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.solarizeWindowClose=True

def posterize(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    # we basically reduce the range of colurs from 256 to 5 bits
    # and so, assign +a single new value to each colour value
    # in each succesive range
    posterData=[]
    if canvas.data.image!=None:
        for col in range(canvas.data.imageSize[1]):
            for row in range(canvas.data.imageSize[0]):
                r, g, b= canvas.data.image.getpixel((row, col))
                if r in range(32):
                    R=0
                elif r in range(32, 96):
                    R=64
                elif r in range(96, 160):
                    R=128
                elif r in range(160, 224):
                    R=192
                elif r in range(224,256):
                    R=255
                if g in range(32):
                    G=0
                elif g in range(32, 96):
                    G=64
                elif g in range(96, 160):
                    G=128
                elif r in range(160, 224):
                    g=192
                elif r in range(224,256):
                    G=255
                if b in range(32):
                    B=0
                elif b in range(32, 96):
                    B=64
                elif b in range(96, 160):
                    B=128
                elif b in range(160, 224):
                    B=192
                elif b in range(224,256):
                    B=255
                posterData.append((R, G, B))
        canvas.data.image.putdata(posterData)
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=draw.makeImageForTk(canvas)
        draw.drawImage(canvas)

def identify_grass(canvas):
    preprocess.preprocessor(canvas)
    '''
    This feature will be used to identify grass in a picture
    '''
    pass


def dilation(canvas):
    '''
    #TODO: Write what function does.
    '''
    covertGray(canvas)
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        print(type(canvas.data.image))
       
        # Taking a matrix of size 5 as the kernel
        image_data = np.asarray(canvas.data.image)
        kernel = np.ones((5,5), np.uint8)
 
        # The first parameter is the original image,
        # kernel is the matrix with which image is 
        # convolved and third parameter is the number 
        # of iterations, which will determine how much 
        # you want to erode/dilate a given image. 
        dilated_image = cv2.dilate(image_data, kernel, iterations=1)
        print(type(dilated_image))
        canvas.data.image = Image.fromarray(dilated_image)
        print(type(canvas.data.image))
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=draw.makeImageForTk(canvas)
        draw.drawImage(canvas) 

def erosion(canvas):
    '''
    #TODO: Write what function does.
    '''
    covertGray(canvas)       
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        print(type(canvas.data.image))
       
        # Taking a matrix of size 5 as the kernel
        image_data = np.asarray(canvas.data.image)
        kernel = np.ones((5,5), np.uint8)
 
        # The first parameter is the original image,
        # kernel is the matrix with which image is 
        # convolved and third parameter is the number 
        # of iterations, which will determine how much 
        # you want to erode/dilate a given image. 
        dilated_image = cv2.erode(image_data, kernel, iterations=1)
        print(type(dilated_image))
        canvas.data.image = Image.fromarray(dilated_image)
        print(type(canvas.data.image))
        file_op.save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=draw.makeImageForTk(canvas)
        draw.drawImage(canvas) 
