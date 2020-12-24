import Information_Retrieval as IR
from PIL import Image
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk
from tkinter import messagebox
import os
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

img_path = input('Enter Image Full Path: ')
input_img = Image.open(img_path)
images = IR.get_similar(input_img)
for img_name in images:
    img = IR.get_image(img_name)
    img.show()
    
    
    
    
    
    
     