import cv2
import serial
import tesserocr
from PIL import Image
import re
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"    # 日志格式化输出
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"                        # 日期格式
fp = logging.FileHandler('Debug.txt', encoding='utf-8')
fs = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])
text = ""

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
         text = tesserocr.image_to_text(Image.open('image2.jpg'), lang='chi_sim')
         text = re.sub("\D", "", text)
         print(text)
         break

cap.release()

def recv(serial):
    while True:
        data = serial.read_all()
        if data == '':
            continue
        else:
            break
        sleep(0.02)
    return data


if __name__ == '__main__':
    serial = serial.Serial('COM1', 9600, timeout=0.5)
    if serial.isOpen():
        print("open success")
    else:
        print("open failed")
    while True:
        EnqString = chr(int("05"))
        StxString = chr(int("02"))
        EtxString = chr(int("03"))
        EotString = chr(int("04"))
        if (text != ""):
            text = EnqString + StxString + text + EtxString + EotString
            logging.debug("发送：" + text)
            serial.write(bytearray(text, encoding="utf-8"))  # 数据写回
            text = ""
        data = recv(serial)
        if data != b'':
            print("receive : ", data)
            logging.debug("接收：" + data.decode('utf-8'))

