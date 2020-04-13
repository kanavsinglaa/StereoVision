import cv2
from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean
from skimage import io
import PIL.ExifTags
import PIL.Image
import numpy as np


def Image_processing(image_location):
    img= color.rgb2gray(io.imread(image_location))
    img = rescale(img, 0.5, anti_aliasing=False)

    return img

def downsample_image(image, reduce_factor):
	for i in range(0,reduce_factor):
		#Check if image is color or grayscale
		if len(image.shape) > 2:
			row,col = image.shape[:2]
		else:
			row,col = image.shape

		image = cv2.pyrDown(image, dstsize= (col//2, row // 2))
	return image

def create_output(vertices, filename):
	ply_header = '''ply
		format ascii 1.0
		element vertex %(vert_num)d
		property float x
		property float y
		property float z
		property uchar red
		property uchar green
		property uchar blue
		end_header
		'''
	with open(filename, 'w') as f:
		f.write(ply_header %dict(vert_num=len(vertices)))
		np.savetxt(f,vertices,'%f %f %f %d %d %d')