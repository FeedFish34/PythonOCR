import cv2
import numpy as np

import tesserocr
from PIL import Image

#调用笔记本内置摄像头，所以参数为0，如果有其他的摄像头可以调整参数为1，2
cap=cv2.VideoCapture(0)
while True:
    #从摄像头读取图片
    sucess,img=cap.read()
    #转为灰度图片s
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #显示摄像头，背景是灰度。
    cv2.imshow("img",gray)
    #保持画面的持续。
    k=cv2.waitKey(1)
    if k == 27:
        #通过esc键退出摄像
        cv2.destroyAllWindows()
        break
    elif k==ord("s"):
        #通过s键保存图片，并退出。
        cv2.imwrite("image2.jpg",img)
        cv2.destroyAllWindows()
        break
#关闭摄像头
cap.release()

text = tesserocr.image_to_text(Image.open('image2.jpg'),lang='chi_sim')
print(text)
