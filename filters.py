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
