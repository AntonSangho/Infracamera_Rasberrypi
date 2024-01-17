import cv2
import numpy as np
from fastiecm import fastiecm
from picamera import PiCamera
import picamera.array

cam = PiCamera()
cam.rotation = 180
cam.resolution = (1920, 1080)
stream = picamera.array.PiRGBArray(cam)
cam.capture(stream, format='bgr', user_video_port=True)
origianl = stream.array


#origianl = cv2.imread('./images/park.png') 

def display(image, image_name):
    image = cv2.imread('./images/park.png') #load the image
    image = np.array(image, dtype=float)/float(255) #convert to float and normalize
    shape = image.shape 
    height = int(shape[0]/2)
    width = int(shape[1]/2)
    image = cv2.resize(image, (width, height)) #resize image
    cv2.namedWindow('Origianl') #create a named window
    cv2.imshow('Original', image) #show the image
    cv2.waitKey(0) #wait for a key press    
    cv2.destroyAllWindows() #destroy all windows

def contrast_strech(im):
    in_min = np.percentile(im, 5) 
    im_max = np.percentile(im, 95) 

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_max - out_min) / (im_max - in_min))
    out += out_min

    return out

def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom == 0] = 0.01
    #ndvi = (b.astype(float) - r) / bottom
    ndvi = (r.astype(float) - b) / bottom
    return ndvi

display(origianl, 'Original')
contrasted = contrast_strech(origianl)
display(contrasted, 'Contrasted original')
cv2.imwrite('./images/contrasted.png', contrasted)
ndvi = calc_ndvi(contrasted)
display(ndvi, 'NDVI')
ndvi_contrasted = contrast_strech(ndvi)
display(ndvi_contrasted, 'NDVI contrasted')
cv2.imwrite('./images/ndvi_contrasted.png', ndvi_contrasted)
color_mapped_prep = ndvi_contrasted.astype(np.uint8)
color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
display(color_mapped_image, 'Color mapped')
cv2.imwrite('./images/color_mapped.png', color_mapped_image)
cv2.imwrite('./images/origianl.png', original)





