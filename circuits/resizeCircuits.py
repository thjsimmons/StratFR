"""
This file resizes schematics to constant size and sets background color 
to the Qt stylesheet color
"""

import cv2
import math

def shiftBG(img):
    output = img
    
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            pixel = img[i, j]
            if pixel[0] == 235 and pixel[1] == 235 and pixel[2] == 235:
                output[i, j] = [240, 240, 240]
    return output
    
path = ''
imList = [path + "B.png", path + "BM.png", path + "M.png", path + "MN.png", path + "N.png" ]

newSize = [535, 870, 3]

for imName in imList:
    img = cv2.imread(imName)
    
    y1 = math.ceil((img.shape[0]-newSize[0])/2)
    y2 = img.shape[0] - math.floor((img.shape[0]-newSize[0])/2)
    x1 = math.ceil((img.shape[1]-newSize[1])/2)
    x2 = img.shape[1] - math.floor((img.shape[1]-newSize[1])/2)
    
    if imName == "N.png":
        crop_img = img[int(y1):int(y2), int(x1):int(x2)-1]
    else:
        crop_img = img[int(y1):int(y2), int(x1):int(x2)]

    print("x2-x1=", x2-x1, ", y2-y1=", y2-y1)
    print("img.shape[0]=", crop_img.shape[0], ", img.shape[1]=", crop_img.shape[1])
    #crop_img = shiftBG(crop_img)
    cv2.imwrite(imName, crop_img) 


                
