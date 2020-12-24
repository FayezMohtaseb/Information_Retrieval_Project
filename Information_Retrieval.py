from PIL import Image
import numpy as np
import pandas as pd
import os
import time
from itertools import cycle
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

class App(tk.Tk):
    '''Tk window/label adjusts to size of image'''
    def __init__(self, image_files, x, y, delay):
        # the root will be self
        tk.Tk.__init__(self)
        # set x, y position only
        self.geometry('+{}+{}'.format(x, y))
        self.delay = delay
        # allows repeat cycling through the pictures
        # store as (img_object, img_name) tuple
        self.pictures = cycle((tk.PhotoImage(file=image), image)
                              for image in image_files)
        self.picture_display = tk.Label(self)
        self.picture_display.pack()

    def show_slides(self):
        '''cycle through the images and show them'''
        # next works with Python26 or higher
        img_object, img_name = next(self.pictures)
        self.picture_display.config(image=img_object)
        # shows the image filename, but could be expanded
        # to show an associated description of the image
        self.title(img_name)
        self.after(self.delay, self.show_slides)

    def run(self):
        self.mainloop()


def load_dataset(path=os.getcwd() + '/Dataset/'):
    return os.listdir(path)


def get_image(name, path=os.getcwd() + '/Dataset/'):
    return Image.open(path + name)


def resize_image(image, size=(150, 150)):
    return image.resize(size)


def get_histogram(image):
    rgb_histogram = []
    for channel_id in range(3):
        histogram, _ = np.histogram(image.getdata(band=channel_id), bins=128, range=(0, 255))
        rgb_histogram.append(histogram)
    return tuple(rgb_histogram)


def save_histograms(histograms_df):
    histograms_df.to_pickle('Dataset_Histograms.pkl')


def compute_dataset_histograms(path=os.getcwd() + '/Dataset/', img_size=(150, 150)):
    start_time = time.time()
    img_list = load_dataset(path=path)

    names = []
    histograms = []
    for image_name in img_list:
        try:
            image = get_image(image_name)
        except IOError:
            print(f'WARNING: "{image_name}" is not an image!')
            continue
        image = resize_image(image, size=img_size)
        hist = get_histogram(image)
        names.append(image_name)
        histograms.append(hist)

    df_ = pd.DataFrame({'Image Name': names, 'Histogram': histograms})
    save_histograms(df_)
    end_time = time.time()
    duration = end_time - start_time
    print(f'Finished in {duration:.1f} seconds')
    return df_


def load_histograms():
    try:
        return pd.read_pickle('Dataset_Histograms.pkl')
    except FileNotFoundError:
        print('Dataset histograms not found\nComputing histograms ...')
        return compute_dataset_histograms()


def compute_distance(rgb_hist1, rgb_hist2):
    rgb_dist = []
    for i in range(3):
        rgb_dist.append(np.linalg.norm(rgb_hist1[i] - rgb_hist2[i]))
    return np.linalg.norm(rgb_dist)


def get_similar(image, quantity=10):
    image = resize_image(image)
    input_hist = get_histogram(image)
    df = load_histograms()
    dist_list = []
    for i in range(len(df)):
        dist = compute_distance(input_hist, df['Histogram'][i])
        dist_list.append([df['Image Name'][i], dist])
    dist_list.sort(key=lambda x: x[1])
    return [x[0] for x in dist_list[:quantity]]


if __name__ == '__main__':
    img_path = input('Enter Image Full Path: ')
    input_img = Image.open(img_path)
    images = get_similar(input_img)
    for img_name in images:
        img = get_image(img_name)
        img.show()
