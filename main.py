import tkinter as tk
import os
import cv2
import shutil

top = tk.Tk()
top.title("Choose a directory")
top.geometry('300x300')

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
        print(img_name)
        print(path)
        print(os.path.join(aug_dir, img_name))
        img = cv2.imread(os.path.join(path, img_name), -1)
        img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE) 
        cv2.imwrite(os.path.join(aug_dir, img_name), img)
        print(img_name)

def add_button(name):
    def callback():    
        dir_click(name)

    B = tk.Button(top, text=name, command = callback)
    B.pack()

path = r"C:\Users\user\Desktop\SEBI"
dirs = [f for f in os.scandir(path) if f.is_dir()]

for file in dirs:
    add_button(file.path)

top.mainloop()