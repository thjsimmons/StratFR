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
    
path = 'circuits/'
imList = [path + "B2.png", path + "BM2.png", path + "M2.png", path + "MN2.png", path + "N2.png" ]

newSize = [535, 870, 3]

for imName in imList:
    img = cv2.imread(imName)
    
    y1 = math.ceil((img.shape[0]-newSize[0])/2)
    y2 = img.shape[0] - math.floor((img.shape[0]-newSize[0])/2)
    x1 = math.ceil((img.shape[1]-newSize[1])/2)
    x2 = img.shape[1] - math.floor((img.shape[1]-newSize[1])/2)
    crop_img = img[int(y1):int(y2), int(x1):int(x2)]

    crop_img = shiftBG(crop_img)
    cv2.imwrite(imName, crop_img) 


                
