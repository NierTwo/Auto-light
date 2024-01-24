import Class
import cv2
import numpy as np
import os
import time
import atexit
import subprocess


bri=Class.Brightness()
# 打开摄像头
cap = cv2.VideoCapture(0)  # 0表示第一个摄像头，如果有多个摄像头，可以尝试其他值

# 循环检测
while 1:
    time.sleep(1)
    # 获取当前亮度
    now_brightness = bri.now_brightness
    # 读取一帧图像
    ret, frame = cap.read()
    # 灰度均值
    mean_value = np.mean(frame)
    normalize_value = mean_value * 100 / 255
    real_brightness = int(normalize_value)
    # 设定阈值，避免震荡，允许误差
    if real_brightness > now_brightness:
        bri.increase()
    else:
        if abs(real_brightness-now_brightness)>=10:
            bri.reduce()