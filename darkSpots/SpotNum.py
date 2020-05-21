# coding:utf-8
import cv2 as cv
import numpy as np
import copy


# 轮廓面积计算函数
def areaCal(contour):
        total_area = 0
        area_list = []
        for i in range(len(contour)):
            new_area = cv.contourArea(contour[i])
            total_area += new_area
            area_list.append(new_area)

        return total_area, area_list


# scharr 算子进行边缘检测
def scharr(filter):
        scharr_x = cv.Scharr(filter, cv.CV_64F, 1, 0)
        scharr_y = cv.Scharr(filter, cv.CV_64F, 0, 1)
        scharr_x = cv.convertScaleAbs(scharr_x)
        scharr_y = cv.convertScaleAbs(scharr_y)
        scharr_xy = cv.addWeighted(scharr_x, 0.5, scharr_y, 0.5, 0)
        return scharr_xy


# 处理暗斑图片
def deal_spot_pic(src_path,dst_path):
    img = cv.imread(src_path) # 1
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)# 2
    img_mean = cv.blur(gray, (17, 17)) # 3去噪
    img_mean1 = cv.blur(img_mean, (17, 17))
    img_mean2 = cv.blur(img_mean1, (17, 17))
    scharr_xy = scharr(img_mean2) # 4边缘检测  调用函数
    kernel=np.ones((7,7),np.uint8)  # 5先开再闭运算
    # 开运算先腐蚀，再膨胀，可清除一些小东西(亮的)，放大局部低亮度的区域
    opening = cv.morphologyEx(scharr_xy,cv.MORPH_OPEN,kernel)
    # 闭运算：先膨胀，再腐蚀，可清除小黑点
    kernel=np.ones((5,5),np.uint8)
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)
    counters,hierarchy = cv.findContours(closing,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE) # 6获得所有的联通区域
    cv.drawContours(img,counters,-1,(0,0,255),3)
    all_area, list_area = areaCal(counters) # 7 all_area的所有联通区域的面积和，list_area是所有联通区域面积的列表,调用函数
    t = copy.deepcopy(list_area)
    max_num = []  # 获得连通区域最大的两个面积
    max_index = []  # 面积最大的两个连通区域的坐标
    for i in range(2):
        num = max(t)
        index = t.index(num)
        t[index] = 0
        max_num.append(num)
        max_index.append(index)
    area_num = len(counters)-2 # 连通区域的个数
    area_square = (all_area-max_num[0]-max_num[1])/max_num[0] # 连通区域的面积占比
    cv.imwrite(dst_path,img)
    return area_num,area_square


