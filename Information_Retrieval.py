from PIL import Image
import numpy as np
import pandas as pd
import os
import time


def load_dataset(path=os.getcwd() + '/Dataset/'):
    return os.listdir(path)


def get_image(name, path=os.getcwd() + '/Dataset/'):
    return Image.open(path + name)


def resize_image(image, size=(150, 150)):
    return image.resize(size)


def get_histogram(image):
    rgb_histogram = []
    for channel_id in range(3):
        histogram, _ = np.histogram(image.getdata(band=channel_id), bins=8, range=(0, 255))
        rgb_histogram.append(histogram)
    return tuple(rgb_histogram)


def save_histograms(histograms_df):
    histograms_df.to_csv('Dataset_Histograms.csv')


def compute_dataset_histograms(path=os.getcwd() + '/Dataset/', img_size=(150, 150)):
    start_time = time.time()
    img_list = load_dataset(path=path)

    names = []
    histograms = []
    for img_name in img_list:
        try:
            img = get_image(img_name)
        except IOError:
            print(f'WARNING: "{img_name}" is not an image!')
            continue
        img = resize_image(img, size=img_size)
        hist = get_histogram(img)
        names.append(img_name)
        histograms.append(hist)

    df_ = pd.DataFrame({'Image Name': names, 'Histogram': histograms})
    save_histograms(df_)
    end_time = time.time()
    duration = end_time - start_time
    print(f'Finished in {duration:.1f} seconds')
    return df_


def load_histograms():
    try:
        return pd.read_csv('Dataset_Histograms.csv')
    except FileNotFoundError:
        print('Dataset histograms not found\nComputing histograms ...')
        return compute_dataset_histograms()


if __name__ == '__main__':
    df = load_histograms()
