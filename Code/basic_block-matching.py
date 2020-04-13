import cv2
import numpy as np
import time 
import matplotlib.pyplot as plt

#====================================
#Function to create point cloud file


def downsample_image(image, reduce_factor):
	for i in range(0,reduce_factor):
		#Check if image is color or grayscale
		if len(image.shape) > 2:
			row,col = image.shape[:2]
		else:
			row,col = image.shape

		image = cv2.pyrDown(image, dstsize= (col//2, row // 2))
	return image

#=========================================================
# Stereo 3D reconstruction 
#=========================================================
# The distance between the two cameras, taken from calib.txt
CAMERA_DISTANCE = 193.001

# The focal length of the two cameras, taken from calib.txt
FOCAL_LENGTH = 3979.911

#Specify image paths
img_path1 = r'C:\Users\Kanav\Desktop\left.png'
img_path2 = r'C:\Users\Kanav\Desktop\right.png'
start=time.time()
#Load pictures in grayscale 
L = cv2.imread(img_path1,0)
R = cv2.imread(img_path2,0)
imgL=downsample_image(L,3)
imgR=downsample_image(R,3)
DSubpixel= np.zeros(imgL.shape,dtype=float)


ndisp = 55
halfBlockSize = 2
blockSize = 2 * halfBlockSize + 1

h,w = imgL.shape[:2]

for r in range(0,h):
    min_r= max(0,r-halfBlockSize)
    max_r= min(h-1,r+halfBlockSize)

    for c in range(0,w):
        min_c= max(0,c-halfBlockSize)
        max_c= min(w-1,c+halfBlockSize)
        
        #Here mind = 0, setting the limits so that we don't go outside of the pic
        min_d= 0
        max_d= min(ndisp,w-max_c-1)
        #Block from imgR as a temp
        temp = imgR[min_r:max_r,min_c:max_c]
        numBlocks= max_d-min_d+1
        #zero vector
        block_differneces = np.zeros(numBlocks,dtype=int)
        
        
        for i in range(0,max_d+1):
            #selecting the block from the left pic at a distance i 
            block= imgL[min_r:max_r,(min_c+i):(max_c+i)]
            blockIndex = i-min_d
            block_differneces[blockIndex]=sum(sum(abs(temp-block)))
        #sort and return the indeces of the sorted elements 

        sort_index=np.argsort(block_differneces)
        bestmatch_index =sort_index[0]
        d=bestmatch_index + min_d
        if (bestmatch_index == 0) or (bestmatch_index == numBlocks-1):
            DSubpixel[r,c]=d
        else:
            D1=block_differneces[bestmatch_index-1]
            D2=block_differneces[bestmatch_index]
            D3=block_differneces[bestmatch_index+1]
            #estimation of subpixel location for the true best match 
            DSubpixel[r,c] = d - (0.5 * ((D3- D1) / (D1 - (2*D2) + D3)))
    #Update the progress very 10th row 
    if (r%10)==0:
        print('Rows completed: ',r,' Percent complete: ',(r/h)*100)
#Time taken 
end= time.time()
print("Elapsed time...",(end-start)/60," mins\n")

#printing a disparity map 
print("Disparity map....\n")
plt.title('Disparity Map')
plt.ylabel('Height {}'.format(DSubpixel.shape[0]))
plt.xlabel('Width {}'.format(DSubpixel.shape[1]))
plt.imshow(DSubpixel,cmap='gray')
plt.show()

print("Calculating depth....")
depth = np.zeros(DSubpixel.shape,dtype=float)

for r in range(0,h):
    for c in range(0,w):
        depth[r,c] =  CAMERA_DISTANCE * FOCAL_LENGTH / abs(DSubpixel[r,c])

print(depth.max())

