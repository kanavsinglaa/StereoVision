# Stereo Point Cloud Generation
This program used two images taken from cameras aligned on a horizon to create a 3D scene; a point cloud of the environment. This program intends to mimic how are eyes and brain work to provide depth to whatever you are see.
Code folder contains all the coding files, which will be needed.

A detailed explanation of how this algorithm works is provided <a href="./Point-Clouds_from_StereoImages_report.pdf">here</a>.

## Results

<h4>Input Image</h4>
<img src="Code/img0.png" width=400>
This is an input image that comes from the camera on the left. This and almost identical right shifted image (from the right camera) are the imputs to the algorithmm.


The algorithm initially streo implements blocks matching to match features and regions in both the pictures; which results in a *disparity* map. This is implemented by comparing the similarity of windows around the pixels to be compared, based on the windows matching corresponding pixels are matched. Have a look at the report to understand how the algorithm works in detail.
Using the disparities, we can then calculate the depth for each pixel.


Here are the results for the matching, in the form of disparity and depth map.
Disparity Map | Depth Map
:------------:|:--------------------:
![](Results/Disparity_map.png)|![](Results/Depth_map.png)
## Running

```bash
    main.py
```

## Point clouds 
Once we get the *disparities*, they are triangulated to gives us respective depths. From these depths we can form point clouds to depict the 3D scene. Read the report for in-depth understanding of how these clouds are constructed.

Here is the point cloud computed from the result of basic block matching algorithm and the ones mentioned in the report:
<h4>Clouds Constructed From Basic Block Matching</h4>

Straight view | Rotated view
:------------:|:--------------------:
![](Results/PointCloud.png)|![](Results/PointCloud2.png)


Further noise filtering and smoothening can result in neater point clouds. More advanced algorithms such as stereoSGBM takes those improvements into account, resulting in well knitted point clouds.

<h4>Cloud Constructed From Semi Global Block Matching</h4>
![](Results/SGBM.gif)

3D scenes like this one can be constructed by using 2D images, giving mobile robots a sense of their environment. 
