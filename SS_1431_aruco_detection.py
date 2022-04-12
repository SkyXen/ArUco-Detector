import numpy as np
import cv2
import cv2.aruco as aruco
import time
from SS_1431_aruco_library import *


image_list = ["../SS_1431/test_image1.png", "../SS_1431/test_image2.png"]
test_num = 1

for image in image_list:
	img = cv2.imread(image)
	Detected_ArUco_markers = detect_ArUco(img)
	angle = Calculate_orientation_in_degree(Detected_ArUco_markers)
	img2 = mark_ArUco(img,Detected_ArUco_markers, angle)
	result_image = "../SS_1431/Result_image"+str(test_num)+".png"
	cv2.imwrite(result_image, img2)
	test_num = test_num + 1


