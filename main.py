import tkinter as tk
import os
import cv2
import shutil
from configparser import ConfigParser

# Read Configuration
config_object = ConfigParser()
config_object.read("config.ini")
default = config_object["default"]
CFG_BLUR = default["blur"]
print("Blur is {}".format(CFG_BLUR))

# Init tkinter
top = tk.Tk()
top.title("Choose a directory")
top.geometry('300x300')

def generate_aug(path, img_name, aug_dir):
    # augment image
    print(img_name)
    print(path)
    print(os.path.join(aug_dir, img_name))
    img = cv2.imread(os.path.join(path, img_name), -1)
    img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE) 
    cv2.imwrite(os.path.join(aug_dir, img_name), img)

def dir_click(path):
    print(path)
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