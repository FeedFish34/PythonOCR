import serial
import pytesseract
from PIL import Image
import re
import logging
import os

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"    # 日志格式化输出
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"                        # 日期格式
fp = logging.FileHandler('Debug.txt', encoding='utf-8')
fs = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])
text = ""
List = []
ResMsg = ""

# #调用笔记本内置摄像头，所以参数为0，如果有其他的摄像头可以调整参数为1，2
# cap=cv2.VideoCapture(0)
# while True:
#      #从摄像头读取图片
#      sucess,img=cap.read()
#      #转为灰度图片s
#      gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#      #显示摄像头，背景是灰度。
#      cv2.imshow("img",gray)
#      #保持画面的持续。
#      k=cv2.waitKey(1)
#      if k == 27:
#          #通过esc键退出摄像
#          cv2.destroyAllWindows()
#
#          break
#      elif k==ord("s"):
#          #通过s键保存图片，并退出。
#          cv2.imwrite("image2.jpg",img)
#          cv2.destroyAllWindows()
#
#          print(text)
#          break
#
# cap.release()

text = pytesseract.image_to_string(Image.open('D:/image2.jpg'), lang='chi_sim')
text = re.sub("\D", "", text)
print(text)


def do_checksum(source_string):
     """  Verify the packet integritity """
     sum = 0
     max_count = 3
     count = 0
     while count < max_count:
         val = ord(source_string[count + 1]) * 256 + ord(source_string[count])
         sum = sum + val
         sum = sum & 0xffffffff
         count = count + 2
     if max_count < len(source_string):
         sum = sum + ord(source_string[len(source_string) - 1])
         sum = sum & 0xffffffff

     sum = (sum >> 16) + (sum & 0xffff)
     sum = sum + (sum >> 16)
     answer = ~sum
     answer = answer & 0xffff
     answer = answer >> 8 | (answer << 8 & 0xff00)
     print(answer)
     return answer


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
            List.append(EnqString)
            ResMsg = StxString + text + EtxString
            logging.debug("校验数据：" + ResMsg)
            List.append(ResMsg + str(do_checksum(ResMsg)))
            List.append(EotString)
            logging.debug("发送：" + List[0])
            serial.write(bytes(List[0].encode('utf-8')))  # 数据写回
            List.pop(0)
            text = ""
        data = recv(serial)
        if data != b'':
            print("receive : ", data)
            for s in data:
                if (s == 6 and len(List) > 0):
                    logging.debug("发送2：" + List[0])
                    serial.write(bytes(List[0].encode('utf-8')))  # 数据写回
                    List.pop(0)
                if (s == 5 or s == 2 or s == 3):
                    print("回复ACK")
                    logging.debug("发送ACK：" + chr(int("06")))
                    serial.write(bytearray(chr(int("06")), encoding="utf-8"))  # 数据写回
            logging.debug("接收：" + data.decode('utf-8'))

