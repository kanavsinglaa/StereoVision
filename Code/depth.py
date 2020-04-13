import numpy as np
import cv2
from configs import FOCAL_LENGTH,CAMERA_DISTANCE,X_A,DOFFS,Y
import matplotlib.pyplot as plt
def depth_map(dispMap,orignal_pic):
    print("Calculating depth....")
    depth = np.zeros(dispMap.shape)
    coordinates=[]
    h,w = dispMap.shape
    for r in range(0,h):
        for c in range(0,w):
            disparity= dispMap[r,c]
            Yoffset=((h-r)*2)-Y
            Xoffset=((w-c)*2)-X_A
            depth[r,c] =  (CAMERA_DISTANCE * FOCAL_LENGTH) / (dispMap[r,c])
            # This will contain x,y,z coordinates with R,G,B values for the pixel
            ZZ=(CAMERA_DISTANCE*FOCAL_LENGTH)/(disparity+DOFFS)
            YY=(ZZ/FOCAL_LENGTH)*Yoffset
            XX=(ZZ/FOCAL_LENGTH)*Xoffset
            coordinates+=[[XX,YY,ZZ,orignal_pic[r][c][2],orignal_pic[r][c][1],orignal_pic[r][c][0]]]
    depthmap = plt.imshow(depth,cmap='jet_r')
    plt.colorbar(depthmap)
    plt.show()
    
    return coordinates

