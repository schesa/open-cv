import tkinter as tk
import os
import cv2
import shutil
from configparser import ConfigParser
import numpy as np

# cap = cv2.VideoCapture("crash.mp4")
cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
ret, frame2 = cap.read()
while(cap.isOpened()):
    moving = False
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)

    # dilated = cv2.dilate(thresh, None, iterations=3)
    
    # contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2. CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        if cv2.contourArea(c)<3000:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame1, "Moving",(20,20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
        moving = True
    if not moving:
        cv2.putText(frame1, "Not moving",(20,20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
    
    cv2.imshow('Result',frame1)
    frame1=frame2
    ret, frame2=cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()