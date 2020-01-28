#!/usr/bin/env python
# coding: utf-8

import os, errno
import sys
import requests
import json
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
videopath = 'YOUR_VIDEO_PATH'
output = 'YOUR_FRAME_HOLD_PATH'
def framemake():
    cap = cv2.VideoCapture(videopath)
    global count
    count = 1
    while True:
        success, image = cap.read()
        if not success:
            break
        print ('Read a new frame: ', success)
        fname = "{}.jpg".format("{}".format(count))
        cv2.imwrite(output + fname, image)
        count += 1
    print("{} images are extracted in {}.".format(count - 1, output))
    

if __name__ == '__main__':
    framemake()

for i in range(1, count):
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"
    url = "https://naveropenapi.apigw.ntruss.com/vision-pose/v1/estimate"
    headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret}
    filepath = output + "{}.jpg".format(i)
    files = {'image': open(filepath, 'rb')}
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code
    if(rescode==200):
        rt = response.text
    else:
        print("Error Code: " + str(rescode))
    json_data = json.loads(response.text)
    dlist = json_data.values()
    data = ' '.join([str(a) for a in dlist])
    data_list = data.split(',')
    x = []
    y = []
    for a in data_list:
        if 'x' in a:
            x.append(round(float(a[6:-2]),4))
        else:
            continue
            
    for a in data_list:
        if 'y' in a:
            y.append(round(float(a[6:-3]),4))
        else:
            continue
    
    get_ipython().run_line_magic('matplotlib', 'inline')
    img = cv2.imread(filepath)
    right_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    photo = Image.open(filepath)
    width, height = photo.size
    new_x = []
    new_y = []
    new_x = [x * width for x in x]
    new_y = [y * height for y in y]
    plt.scatter(new_x ,new_y , c = 'y', s = 7)
    plt.imshow(right_img)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig('YOUR_FRAME_WITH_POINT_PATH/{}.png'.format(i), bbox_inches = "tight")
    
frame = 'YOUR_FRAME_WITH_POINT_PATH/'
def main():
    try:
        if(os.path.isdir(frame)):
            for roots, dirs, files in os.walk(frame, topdown = False):
                
                bIsFirst = True
                for name in files:
                    cur_file = os.path.join(frame, name)
                    cur_img = cv2.imread(cur_file)
                    
                    print("Currently %s being processed..." % (cur_file))
                    
                    if (type(cur_img) == np.ndarray):
                        if (bIsFirst):
                            frame_height = cur_img.shape[0]
                            frame_width = cur_img.shape[1]
                            
                            video_file= os.path.join('YOUR_VIDEO_OUTPUT_PATH', 'YOUR_VIDEO_NAME.avi')
                            out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
                        
                        out.write(cur_img)
                    
                    bIsFirst = False
   
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    out.release()
    
if __name__ == '__main__':
    main()
