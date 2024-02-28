import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from itertools import groupby

def add_location(obj, name, x1, y1, x2, y2):
    obj.append({'name': name,'x1': x1,'y1': y1,'x2': x2,'y2': y2})

def show(template):
    plt.imshow(template)
    plt.show()
    
def convert(o):
    if isinstance(o, np.int64):
        return int(o)  
         

def read_templates(directory_path):
    templates = []
    files = []
    
    for f in os.listdir(directory_path):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            # 템플릿 이미지를 그레이스케일로 읽어오기
            template = cv2.imread(os.path.join(directory_path, f))
            # 이진화 수행
            template_threshold = preprocessing_blur(template)   

            # 이진화된 이미지를 템플릿 리스트에 추가
            templates.append(template_threshold)

            name, ext = os.path.splitext(f)
            files.append(name) 

    return templates, files

def preprocessing_blur(img):
    # 그레이스케일
    img = cv2.GaussianBlur(img, (3, 3), 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    return gray

def plt_imshow(title='image', img=None, figsize=(8 ,5)):
    plt.figure(figsize=figsize)
 
    if type(img) == list:
        if type(title) == list:
            titles = title
        else:
            titles = []
 
            for i in range(len(img)):
                titles.append(title)
 
        for i in range(len(img)):
            if len(img[i].shape) <= 2:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_GRAY2RGB)
            else:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)
 
            plt.subplot(1, len(img), i + 1), plt.imshow(rgbImg)
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])
 
        plt.show()
    else:
        if len(img.shape) < 3:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
        plt.imshow(rgbImg)
        plt.title(title)
        plt.xticks([]), plt.yticks([])
        plt.show()
 


def group_similar_x_and_command(data):
    # x 값으로 정렬
    sorted_data = sorted(data, key=lambda x: x["x"])
    
    # 그룹화된 결과를 저장할 리스트
    grouped_results = []
    
    # 현재 그룹의 시작점과 그룹에 속한 아이템들을 저장할 리스트
    current_group_start = None
    current_group_items = []
    
    # 아이템을 순회하면서 그룹화 수행
    for item in sorted_data:
        # 만약 현재 그룹의 시작점이 정해지지 않았거나, 이전 아이템과의 x 값 차이가 10보다 큰 경우 새로운 그룹 시작
        if current_group_start is None or item["x"] - current_group_start > 10:
            # 이전 그룹 결과를 리스트에 추가
            if current_group_items:
                grouped_results.append(current_group_items)
            # 새로운 그룹 시작
            current_group_start = item["x"]
            current_group_items = [item]
        else:
            # 이전 그룹에 속함
            current_group_items.append(item)
    
    # 마지막 그룹 결과를 리스트에 추가
    if current_group_items:
        grouped_results.append(current_group_items)
    
    # 각 그룹에서 x 값으로 ratio가 가장 큰 데이터만 선택하여 최종 결과 생성
    final_result = []
    for group in grouped_results:
        max_ratio_data = max(group, key=lambda x: float(x["ratio"]))
        final_result.append(max_ratio_data)

    
    # x 값으로 정렬하여 반환
    sorted_final_result = sorted(final_result, key=lambda x: x["x"])

    # # y값과, ratio는 제외 하고 반환
    # for i in range(len(sorted_final_result)): 
    #     del sorted_final_result[i]['ratio']

    return sorted_final_result