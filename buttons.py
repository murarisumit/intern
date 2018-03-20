import tkinter as tk
import features
import draw


def buttons_init(fm, canvas):
    backgroundColour="yellow"
    buttonWidth=14
    buttonHeight=2
    cropButton=tk.Button(fm, text="Crop",\
                      background=backgroundColour ,\
                      width=buttonWidth, height=buttonHeight, \
                      command=lambda:features.crop(canvas))
    cropButton.pack( side = tk.TOP )

    #cropButton.grid(row=0,column=0)
    rotateButton=tk.Button(fm, text="Rotate",\
                        background=backgroundColour, \
                        width=buttonWidth,height=buttonHeight, \
                        command=lambda: features.rotate(canvas))
    rotateButton.pack( side = tk.TOP )
    mirrorButton=tk.Button(fm, text="Mirror",\
                        background=backgroundColour, \
                        width=buttonWidth,height=buttonHeight, \
                        command=lambda: features.mirror(canvas))
    mirrorButton.pack( side = tk.TOP )                    
    flipButton=tk.Button(fm, text="Flip",\
                      background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight, \
                      command=lambda: features.flip(canvas))
    flipButton.pack( side = tk.TOP )
    transposeButton=tk.Button(fm, text="Transpose",\
                           background=backgroundColour, width=buttonWidth,\
                           height=buttonHeight,command=lambda: features.transpose(canvas))
    transposeButton.pack( side = tk.TOP )
    resetButton=tk.Button(fm, text="Reset",\
                       background=backgroundColour ,width=buttonWidth,\
                       height=buttonHeight, command=lambda:features.reset(canvas))
    resetButton.pack( side = tk.TOP )



