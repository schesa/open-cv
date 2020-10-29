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

CFG_SCALE = float(default_config["Scale"])
print("Scale is {}".format(CFG_SCALE))

CFG_SHEAR = float(default_config["Shear"])
print("Shear is {}".format(CFG_SHEAR))

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


def apply_alg(name, img, value, value2=0):
    if name.lower() == 'blur':
        median = cv2.medianBlur(img, int(value))
        return median
    elif name.lower() == 'contrast_brightness':
        Contrast_Brightness_img = cv2.convertScaleAbs(img, alpha=value, beta=value2)
        return Contrast_Brightness_img
    elif name.lower() == 'rotation':
        rotation_img = cv2.rotate(img, int(value))
        return rotation_img
    elif name.lower() == 'gamma':
        invGamma = 1.0 / float(value)
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        gamma_img = cv2.LUT(img, table)
        return gamma_img
    elif name.lower() == 'scale':
        res_img = cv2.resize(img,None,fx=float(value), fy=float(value))
        return res_img
    else:
        print('Algorithm ' + name + ' not implemented')
        return img


def generate_aug(path, img_name, aug_dir):
    print('IMG NAME ' + img_name)

    img = cv2.imread(os.path.join(path, img_name), -1)

    # Blur
    median = apply_alg('Blur', img, CFG_BLUR)
    save_img(aug_dir, img_name, 'Blur', median)

    # Contrast and Brightness
    Contrast_Brightness_img = apply_alg('Contrast_Brightness', img, CFG_CONTRAST, CFG_BRIGHTNESS)
    save_img(aug_dir, img_name, 'Contrast_Brightness', Contrast_Brightness_img)

    # Rotation
    rotation_img = apply_alg('Rotation', img, CFG_ROTATION)
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
    # invGamma = 1.0 / CFG_GAMMA
    # table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    # gamma_img = cv2.LUT(img, table)
    gamma_img = apply_alg('Gamma', img, CFG_GAMMA)
    save_img(aug_dir, img_name, 'Gamma', gamma_img)

    # Scale
    res_img = apply_alg('Scale', img, CFG_SCALE)
    save_img(aug_dir, img_name, 'Scale', res_img)

    # Shear
    rows, cols = img.shape[:2]       
    pts1 = np.float32([[5,5],[20,5],[5,20]])
    pt1 = 5+CFG_SHEAR*np.random.uniform()-CFG_SHEAR/2
    pt2 = 20+CFG_SHEAR*np.random.uniform()-CFG_SHEAR/2
    pts2 = np.float32([[pt1,5],[pt2,pt1],[5,pt2]])
    shear_M = cv2.getAffineTransform(pts1,pts2)
    shear_img = cv2.warpAffine(img,shear_M,(cols,rows))
    save_img(aug_dir, img_name, 'Shear', shear_img)

    #Combos
    for combo_name in config_object:
        if combo_name.lower() != 'default':
            print(combo_name)
            for algorithm_name in config_object[combo_name]:
                value = config_object[combo_name][algorithm_name]
                print(algorithm_name+" "+value)
                img = apply_alg(algorithm_name, img, value)
            save_img(aug_dir, img_name, combo_name, img)


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