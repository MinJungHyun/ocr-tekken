import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

def add_location(obj, name, x1, y1, x2, y2, mode):
    obj.append({'name': name,'x1': x1,'y1': y1,'x2': x2,'y2': y2,'mode': mode })

def show(template):
    plt.imshow(template)
    plt.show()
    
def convert(o):
    if isinstance(o, np.int64):
        return int(o)  
        
# 이미지 전처리
def preprocessing(img):
    # 그레이스케일
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 이진화
    _, binary = cv2.threshold(gray, 70, 255, cv2.THRESH_TOZERO)  
    
    # 외곽선 그리기
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(binary, contours, -1, (30, 30, 30),2)   
    binary = cv2.bitwise_not(binary) 
    # 이진화
    # _, binary = cv2.threshold(binary, 75, 255, cv2.THRESH_TOZERO)  
    return binary

