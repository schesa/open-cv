import tkinter as tk
import os

top = tk.Tk()
top.title("Choose a directory")
top.geometry('300x300')

def dir_click(name):
    print(name)
    os.mkdir(name + '_aug')
    images = os.listdir(name)
    for img in images:
        print(img)

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