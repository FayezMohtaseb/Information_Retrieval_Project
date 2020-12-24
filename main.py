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


window= tk.Tk()
window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
window.withdraw()
if messagebox.askyesno('Question'," choose yes if you want to test image retival program otherise click no")==True:
    window.deiconify()
    window.destroy()
    window.quit()
    root = tk.Tk()
    root.withdraw()
    root.update()
    # get a series of gif images you have in the working folder
    # or use full path, or set directory to where the images are
    image_files = []
    img_path = askopenfilename(filetypes=[("Image File", "*.jpg")])

# img_path = input('Enter Image Full Path: ')
# input_img = Image.open(img_path)
# images = IR.get_similar(input_img)
# for img_name in images:
#     img = IR.get_image(img_name)
#     img.show()
#
#
    
    
    
    
     