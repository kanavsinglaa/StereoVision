import cv2
import numpy as np
import time 
import matplotlib.pyplot as plt
from depth import depth_map
from configs import img_path1,img_path2
from disparity import disparitymap
from image import Image_processing,downsample_image,create_output


def main():
    img=cv2.imread(img_path1,1)
    img= downsample_image(img,1)
    
    imgL=Image_processing(img_path1)
    imgR=Image_processing(img_path2)
    plt.imshow(imgL, cmap='gray')
    plt.show()
    
    Map= disparitymap(imgL,imgR)
    coordinates= depth_map(Map,img)
    print('\n Creating the output file... \n')
    create_output(coordinates,'praxis.ply')
 
    

main()