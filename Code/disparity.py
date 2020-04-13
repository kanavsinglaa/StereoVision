import cv2
import numpy as np
import time 
import matplotlib.pyplot as plt

def generate_window(row, col, image, blockSize):
    window = (image[row:row + blockSize, col:col + blockSize])
    return window

def disparitymap(imgL,imgR,dispMap=[]):
    # Size of the search window 
    blockSize = 5
    h, w = imgL.shape
    dispMap = np.zeros((h, w))
    # maximum disparity to search for (Tuned by experimenting)
    max_disp = int(w//3)
    # Initializing disparity value 
    dispVal = 0
    tic=time.time()
    for row in range(0, h - blockSize + 1, blockSize):
        for col in range(0, w - blockSize + 1, blockSize):
            winR = generate_window(row, col, imgR, blockSize)
            sad = 9999
            dispVal = 0
            for colL in range(col + blockSize, min(w - blockSize, col + max_disp)):
                winL = generate_window(row, colL, imgL, blockSize)
                tempSad = int(abs(winR- winL).sum())
                if tempSad < sad:
                    sad = tempSad
                    dispVal = abs(colL - col)
            for i in range(row, row + blockSize):
                for j in range(col, col + blockSize):
                    dispMap[i, j] = dispVal

  
        # Updating progress 
        if (row % 50 == 0):
            print('Row number {} Percent complete {} %'.format(row,row*100/h))
    toc = time.time()
    print('elapsed time... {} mins'.format((toc - tic)/60 ))
    #printing the disparity amap
    print("Disparity map....\n")
    plt.title('Disparity Map')
    plt.ylabel('Height {}'.format(dispMap.shape[0]))
    plt.xlabel('Width {}'.format(dispMap.shape[1]))
    plt.imshow(dispMap,cmap='gray')
    plt.show()

    return dispMap


# print("Calculating depth....")
# depth = np.zeros(dispMap.shape)

# for r in range(0,h):
#     for c in range(0,w):
#         depth[r,c] =  (CAMERA_DISTANCE * FOCAL_LENGTH) / dispMap[r,c]

# image = plt.imshow(depth,cmap='jet_r')
# plt.colorbar(image)
# plt.show()




