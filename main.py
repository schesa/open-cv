import tkinter as tk
import os
import cv2
import shutil
from configparser import ConfigParser
import numpy as np

# Read Configuration
config_object = ConfigParser()
config_object.read("config.ini")
default_config = config_object["default"]

CFG_BLUR = int(default_config["Blur"])
print("Blur is {}".format(CFG_BLUR))

CFG_BRIGHTNESS = float(default_config["Brightness"])
print("Brightness is {}".format(CFG_BRIGHTNESS))
CFG_CONTRAST = float(default_config["Contrast"])
print("Contrast is {}".format(CFG_CONTRAST))

CFG_ROTATION = int(default_config["Rotation"])
print("Rotation is {}".format(CFG_ROTATION))

CFG_PADDING = int(default_config["Padding"])
print("Padding is {}".format(CFG_PADDING))

CFG_GAMMA = float(default_config["Gamma"])
print("Gamma is {}".format(CFG_GAMMA))

# Init tkinter
top = tk.Tk()
top.title("Choose a directory")
top.geometry('300x300')

COUNT = 1


def get_aug_img_name(img_name, algorithm_name):
    global COUNT
    aug_img_name = ('_' + algorithm_name + '_' + str(COUNT) + '.').join(img_name.rsplit('.', 1))
    COUNT += 1
    return aug_img_name

def save_img(aug_dir, img_name, algorithm_name, img):
    cv2.imwrite(os.path.join(aug_dir, get_aug_img_name(img_name, algorithm_name)), img)


def generate_aug(path, img_name, aug_dir):
    print('IMG NAME ' + img_name)

    img = cv2.imread(os.path.join(path, img_name), -1)

    # Blur
    median = cv2.medianBlur(img, CFG_BLUR)
    save_img(aug_dir, img_name, 'Blur', median)

    # Contrast and Brightness
    Contrast_Brightness_img = cv2.convertScaleAbs(img, alpha=CFG_CONTRAST, beta=CFG_BRIGHTNESS)
    save_img(aug_dir, img_name, 'Contrast_Brightness', Contrast_Brightness_img)
    # cv2.imwrite(os.path.join(aug_dir, get_aug_img_name(img_name, 'Contrast_Brightness')), img)

    # Rotation
    rotation_img = cv2.rotate(img, CFG_ROTATION)
    save_img(aug_dir, img_name, 'Rotation', rotation_img)

    # Padding
    mean = cv2.mean(img)[0]
    mean_border = cv2.copyMakeBorder(
        img,
        top=CFG_PADDING,
        bottom=CFG_PADDING,
        left=CFG_PADDING,
        right=CFG_PADDING,
        borderType=cv2.BORDER_CONSTANT,
        value=[mean, mean, mean]
    )
    save_img(aug_dir, img_name, 'Reflect_Mean', mean_border)

    wrap_border = cv2.copyMakeBorder(
        img,
        top=CFG_PADDING,
        bottom=CFG_PADDING,
        left=CFG_PADDING,
        right=CFG_PADDING,
        borderType=cv2.BORDER_WRAP
    )
    save_img(aug_dir, img_name, 'Border_Wrap', wrap_border)

    border = cv2.copyMakeBorder(
        img,
        top=CFG_PADDING,
        bottom=CFG_PADDING,
        left=CFG_PADDING,
        right=CFG_PADDING,
        borderType=cv2.BORDER_REFLECT
    )
    save_img(aug_dir, img_name, 'Border_Reflect', border)

    # Gamma
    invGamma = 1.0 / CFG_GAMMA
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    gamma_img = cv2.LUT(img, table)
    save_img(aug_dir, img_name, 'Gamma', gamma_img)


def dir_click(path):
    aug_dir = path + '_aug'

    try:
        os.mkdir(aug_dir)
    except:
        shutil.rmtree(aug_dir)
        os.mkdir(aug_dir)

    images = os.listdir(path)
    for img_name in images:
        generate_aug(path, img_name, aug_dir)


def add_button(name):
    def callback():    
        dir_click(name)

    B = tk.Button(top, text=name, command = callback)
    B.pack()

# Init Path
PATH = os.path.abspath(os.getcwd())
dirs = [f for f in os.scandir(PATH) if f.is_dir()]
for file in dirs:
    add_button(file.path)

# Start UI
top.mainloop()