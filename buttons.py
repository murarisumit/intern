import tkinter as tk
import features
import draw


def buttons_init(root, canvas):
    backgroundColour="gray"
    buttonWidth=14
    buttonHeight=2
    toolKitFrame=tk.Frame(root)
    cropButton=tk.Button(toolKitFrame, text="Crop",\
                      background=backgroundColour ,\
                      width=buttonWidth, height=buttonHeight, \
                      command=lambda:features.crop(canvas))
    cropButton.grid(row=0,column=0)
    rotateButton=tk.Button(toolKitFrame, text="Rotate",\
                        background=backgroundColour, \
                        width=buttonWidth,height=buttonHeight, \
                        command=lambda: features.rotate(canvas))
    rotateButton.grid(row=1,column=0)
    brightnessButton=tk.Button(toolKitFrame, text="Brightness",\
                            background=backgroundColour ,\
                            width=buttonWidth, height=buttonHeight,\
                            command=lambda:features.brightness(canvas))
    brightnessButton.grid(row=2,column=0)
    histogramButton=tk.Button(toolKitFrame, text="Histogram",\
                           background=backgroundColour ,\
                           width=buttonWidth,height=buttonHeight, \
                           command=lambda: features.histogram(canvas))
    histogramButton.grid(row=3,column=0)
    colourPopButton=tk.Button(toolKitFrame, text="Colour Pop",\
                           background=backgroundColour, \
                           width=buttonWidth,height=buttonHeight, \
                           command=lambda: features.colourPop(canvas))
    colourPopButton.grid(row=4,column=0)
    mirrorButton=tk.Button(toolKitFrame, text="Mirror",\
                        background=backgroundColour, \
                        width=buttonWidth,height=buttonHeight, \
                        command=lambda: features.mirror(canvas))
    mirrorButton.grid(row=5,column=0)
    flipButton=tk.Button(toolKitFrame, text="Flip",\
                      background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight, \
                      command=lambda: features.flip(canvas))
    flipButton.grid(row=6,column=0)
    transposeButton=tk.Button(toolKitFrame, text="Transpose",\
                           background=backgroundColour, width=buttonWidth,\
                           height=buttonHeight,command=lambda: features.transpose(canvas))
    transposeButton.grid(row=7,column=0)
    drawButton=tk.Button(toolKitFrame, text="Draw",\
                      background=backgroundColour ,width=buttonWidth,\
                      height=buttonHeight,command=lambda: draw.drawOnImage(canvas))
    drawButton.grid(row=8,column=0)
    resetButton=tk.Button(toolKitFrame, text="Reset",\
                       background=backgroundColour ,width=buttonWidth,\
                       height=buttonHeight, command=lambda:features.reset(canvas))
    resetButton.grid(row=9,column=0)

    toolKitFrame.pack(side=tk.LEFT)


