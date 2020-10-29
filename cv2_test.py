import numpy as np
import cv2

img = cv2.imread('dog.jpg', -1)

font = cv2.FONT_HERSHEY_SIMPLEX

cv2.putText(img, 'CHESA SEBASTIAN', (50,30), font, 1, 1, 3, cv2.LINE_AA)
cv2.imwrite('chesa.jpg', img)

cv2.imshow('chesa',img)
cv2.waitKey(0)
cv2.destroyAllWindows()