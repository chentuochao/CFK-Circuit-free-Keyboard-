import cv2 as cv
import math
import numpy as np
import copy
import functools

def draw_circle(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        print(x,y)
      

def draw_circle2(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        print(x,y)
        cv.circle(src2, (x,y), 5, (0,0,0), -1)
        cv.imshow('image2', src2)



src1=cv.imread("./kbd.jpg")
print(src1.shape)#, src1.size())
(h, w) = src1.shape[:2] #10
center = (w // 2, h // 2) #11


downy = 400
upy = h - 230
downx = 20
upx = w - 200

'''
downy = 100
upy = h - 100
downx = 20
upx = w - 10
'''

src1 = src1[ downy : upy, downx : upx, 0:]
#cv.setMouseCallback('image',draw_circle)
cv.imshow('image', src1)
src2 = copy.deepcopy(src1)

for x in range(0, upx - downx):
    for y in range(0 , upy - downy):
        r = int(src1[y,x,2])
        g = int(src1[y,x,1])
        b = int(src1[y,x,0])
        #if r+g+b > 130 and r+g+b<450:
        if  r > 160 and r - g > 20 and r-b >20:
            src2[y, x] =np.array([255,255,255]) 
        else:
            src2[y, x] = np.array([0,0,0]) 

cv.circle(src2, (48,61), 5, (255,255,255), -1)
cv.circle(src2, (804,192), 5, (0,0,0), -1)

'''
point = [[1238,27], [1394, 437],[47, 31],[47, 131]]
for i in point:
    
'''

cv.namedWindow('image2')
cv.imshow('image2', src2)
cv.setMouseCallback('image2',draw_circle2)

kernel = np.ones((3, 3), np.uint8)
while 1:
    if(cv.waitKey (0) == 121):
        break
    print("ssss")
    src2 = cv.erode(src2, kernel)  # 腐蚀
    src2 = cv.dilate(src2, kernel)  # 腐蚀
    cv.imshow('image2', src2)

kernel = np.ones((7, 7), np.uint8)
src2 = cv.dilate(src2, kernel)  # 腐蚀
src2 = cv.dilate(src2, kernel)  # 腐蚀

gray = cv.cvtColor(src2, cv.COLOR_BGR2GRAY)
ret, binary = cv.threshold(gray,127,255,cv.THRESH_BINARY)  
contours, hierarchy = cv.findContours(binary,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)  

image = np.zeros([upy-downy, upx - downx])
points = []
for contour in contours:
    M = cv.moments(contour)  # 计算第一条轮廓的各阶矩,字典形式
    center_x = int(M["m10"] / M["m00"])
    center_y = int(M["m01"] / M["m00"])
    points.append([center_x,center_y])
    #cv.drawContours(src2, contours, 0, 255, -1)#绘制轮廓，填充
    cv.circle(image, (center_x, center_y), 7, 128, -1)#绘制中心点
cv.imshow('result', image)
cv.setMouseCallback('result',draw_circle)

Q_O = 153
Y_space = 58
rQO = 790 - 163
ry = 378 - 138

px = Q_O/rQO
py = Y_space / ry
min = 10000
p0 = points[0]
for point in points:
    if min > point[0] + point[1]:
        min = point[0] + point[1]
        p0 = point
        
result = []
for point in points:
    kx = px*(point[0] -p0[0]) 
    ky = py*(point[1] -p0[1]) 
    result.append([kx, ky])

def mycmp(p1, p2):
    if p1[1] - p2[1] > 5:
        return 1
    elif p1[1] - p2[1] < -5:
        return -1
    else:
        if p1[0] - p2[0] > 5:
            return 1
        else: return -1
        


points2= sorted(result, key=functools.cmp_to_key(mycmp))
with open("keyboard.txt","w") as f:                                                   #设置文件对象
    for point in points2:                                                                #对于双层列表中的数据
        f.writelines(str(point[0]) +' ' + str(point[1])+'\n')                                                            #写入文件

print("new")
cv.imshow('image2', src2)
cv.waitKey(0)
cv.destroyAllWindows()