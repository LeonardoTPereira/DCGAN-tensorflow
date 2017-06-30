#Leonardo Tortoro Pereira 7573621

#Heap Sort: http://python3.codes/popular-sorting-algorithms/

import sys
import cv2
import numpy as np

#Global variables to decide which pixel was selected by the user
selectX = -1
selectY = -1
hasSelected = 0

#Class that defines a sprite (16x16 image) and its average color
class Sprite(object):
    def __init__(self):
        self.sprite = np.zeros((spriteSize,spriteSize,3), np.uint8)
        self.avgH = 0.0
        self.avgS = 0.0
        self.avgV = 0.0

#Gets the average color for each channel of a sprite, with a normal average
def calcAvgColor(sprite):
    size = len(sprite.sprite)
    h, s, v = cv2.split(sprite.sprite)
    auxH = 0.0
    auxV = 0.0
    auxS = 0.0
    for i in range(size):
        for j in range(size):
            auxH = auxH + h[i][j]
            auxS = auxS + s[i][j]
            auxV = auxV + v[i][j]
    sprite.avgH = np.uint8(auxH/(size*size))
    sprite.avgS = np.uint8(auxS/(size*size))
    sprite.avgV = np.uint8(auxV/(size*size))
	
def compareSprites(spr1, spr2):
    if ((spr1.avgV < spr2.avgV)):
        return 1
    elif ((spr1.avgV > spr2.avgV)):
        return 0
    else:
        if((spr1.avgH < spr2.avgH) ):
            return 1
        elif ((spr1.avgH > spr2.avgH)):
            return 0
        else:
            if((spr1.avgS < spr2.avgS)):
                return 1
            else:
                return 0


'''
def compareSprites(spr1, spr2):
    avg1 = (spr1.avgH+spr1.avgS+spr1.avgV)/3.0
    avg2 = (spr2.avgH+spr2.avgS+spr2.avgV)/3.0
    if avg1 < avg2:
        return 1
    else:
        return 0

'''

def swap(i, j, spriteList, spriteListHSV):                    
     spriteList[i], spriteList[j] = spriteList[j], spriteList[i]
     spriteListHSV[i], spriteListHSV[j] = spriteListHSV[j], spriteListHSV[i]
 
def heapify(end,i,spriteList, spriteListHSV):   
    l=2 * i + 1 
    r=2 * (i + 1)   
    max=i   
    #if l < end and list[i] < list[l]: 
    if l < end and compareSprites(spriteListHSV[i], spriteListHSV[l]): 
        max = l   
    #if r < end and list[max] < list[r]:   
    if r < end and compareSprites(spriteListHSV[max], spriteListHSV[r]):   
        max = r   
    if max != i:   
        swap(i, max, spriteList, spriteListHSV)   
        heapify(end, max, spriteList, spriteListHSV)   
 
def heap_sort(spriteList, spriteListHSV):     
    end = len(spriteList)   
    start = end // 2 - 1
    for i in range(start, -1, -1):   
        heapify(end, i, spriteList, spriteListHSV)   
    for i in range(end-1, 0, -1):   
        swap(i, 0, spriteList, spriteListHSV)   
        heapify(i, 0, spriteList, spriteListHSV)  

def findHueRange(color):
    if color == "green":
        return 42.5, 72.5
    else:
        0, 0
    
# mouse callback function
def getColorInPixel(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global hasSelected
        hasSelected = 1
        global selectX
        selectX = x
        global selectY
        selectY = y

def isNeighbor(sprite, pixel):
    #print(str(sprite.avgH)+"|"+str(sprite.avgS)+"|"+str(sprite.avgV))
    if(sprite.avgH > (pixel[0]-20) and sprite.avgH < (pixel[0]+20)):
        if(sprite.avgS > (pixel[1]-20) and sprite.avgS < (pixel[1]+20)):
            if(sprite.avgV > (pixel[2]-20) and sprite.avgV < (pixel[2]+20)):
                return 1
    return 0

# Create a black image, a window and bind the function to window


filename = input()
isChoosingColor = input()
color = input()
if isChoosingColor=='1': 
    minHue, maxHue = findHueRange(color)
#Read the image
img_original = cv2.imread(filename, cv2.IMREAD_COLOR)
height, width = img_original.shape[:2]

spriteSize = 16
spriteSheet = list()
spriteSheetHSV = list()
spriteCount = 0
sprite = [[Sprite() for row in range(0,spriteSize)] for col in range(0,spriteSize)]


img_hsv = cv2.cvtColor(img_original, cv2.COLOR_BGR2HSV)

width, height = img_original.shape[:2]

cv2.namedWindow('Raw')
cv2.setMouseCallback('Raw',getColorInPixel)
cv2.imshow('Raw', img_original)
#cv2.waitKey(0)
#while(hasSelected==0):
#    pass
print(str(selectX)+" "+str(selectY))
pixel = img_hsv[selectX][selectY]
print(str(pixel[0])+" "+str(pixel[1])+" "+str(pixel[2]))
for i in range(int(width/spriteSize)):
    for j in range(int(height/spriteSize)):
        spriteSheet.append(Sprite())
        spriteSheetHSV.append(Sprite())
        for x in range(spriteSize):
            for y in range(spriteSize):
                (spriteSheet[len(spriteSheet)-1]).sprite[x][y] = img_original[i*spriteSize+x][j*spriteSize+y]
                (spriteSheetHSV[len(spriteSheetHSV)-1]).sprite[x][y] = img_hsv[i*spriteSize+x][j*spriteSize+y]
        calcAvgColor(spriteSheetHSV[len(spriteSheetHSV)-1])
        if isChoosingColor=='1':
            if ((spriteSheetHSV[len(spriteSheetHSV)-1]).avgH < minHue) or ((spriteSheet[len(spriteSheetHSV)-1]).avgH > maxHue):
                spriteSheet.pop()
                spriteSheetHSV.pop()
        if isChoosingColor=='2':
            if(not isNeighbor(spriteSheetHSV[len(spriteSheetHSV)-1], pixel)):
                spriteSheet.pop()
                spriteSheetHSV.pop()
                

size = len(spriteSheet)            
#creates a new image with float, as the uint8 may overflow and gamma returns a float
newHeigth = int((spriteSize*spriteSize*size)/width)
img_res = np.zeros((newHeigth+spriteSize,width,3), np.uint8)

for i in range(int(width/spriteSize)):
    for j in range(int(height/spriteSize)):
        if(spriteCount < size):
            for x in range(spriteSize):
                for y in range(spriteSize):
                    img_res[i*spriteSize+x][j*spriteSize+y] = spriteSheet[spriteCount].sprite[x][y]
            spriteCount = spriteCount + 1
spriteCount = 0


cv2.imshow('Reduced', img_res)

cv2.imwrite('Reduced.png', img_res)

heap_sort(spriteSheet, spriteSheetHSV)
for i in range(int(width/spriteSize)):
    for j in range(int(height/spriteSize)):
        if(spriteCount < size):
            for x in range(spriteSize):
                for y in range(spriteSize):
                    img_res[i*spriteSize+x][j*spriteSize+y] = spriteSheet[spriteCount].sprite[x][y]
            spriteCount = spriteCount + 1
cv2.imshow('Ordered', img_res)

cv2.imwrite('ReducedOrdered.png', img_res)
cv2.waitKey(0)
cv2.destroyAllWindows()