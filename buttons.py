import tkinter as tk
import features
import draw


def buttons_init(root, canvas):
    backgroundColour="yellow"
    buttonWidth=14
    buttonHeight=2
    toolKitFrame=tk.Frame(root, width=16, height=18, bg="blue")
    toolKitFrame.pack( side = tk.TOP )

    cropButton=tk.Button(toolKitFrame, text="Crop",\
                      background=backgroundColour ,\
                      width=buttonWidth, height=buttonHeight, \
                      command=lambda:features.crop(canvas))
    cropButton.pack( side = tk.TOP )

    #cropButton.grid(row=0,column=0)
    rotateButton=tk.Button(toolKitFrame, text="Rotate",\
                        background=backgroundColour, \
                        width=buttonWidth,height=buttonHeight, \
                        command=lambda: features.rotate(canvas))
    rotateButton.pack( side = tk.TOP )
    mirrorButton=tk.Button(toolKitFrame, text="Mirror",\
                        background=backgroundColour, \
                        width=buttonWidth,height=buttonHeight, \
                        command=lambda: features.mirror(canvas))
    mirrorButton.pack( side = tk.TOP )                    
    flipButton=tk.Button(toolKitFrame, text="Flip",\
                      background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight, \
                      command=lambda: features.flip(canvas))
    flipButton.pack( side = tk.TOP )
    transposeButton=tk.Button(toolKitFrame, text="Transpose",\
                           background=backgroundColour, width=buttonWidth,\
                           height=buttonHeight,command=lambda: features.transpose(canvas))
    transposeButton.pack( side = tk.TOP )
    resetButton=tk.Button(toolKitFrame, text="Reset",\
                       background=backgroundColour ,width=buttonWidth,\
                       height=buttonHeight, command=lambda:features.reset(canvas))
    resetButton.pack( side = tk.TOP )
    toolKitFrame.pack(side=tk.LEFT)



