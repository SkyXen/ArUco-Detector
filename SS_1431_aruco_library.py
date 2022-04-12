import numpy as np
import cv2
import cv2.aruco as aruco
import sys
import math
import time

def detect_ArUco(img):
	Detected_ArUco_markers = {}
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)
	param = cv2.aruco.DetectorParameters_create()
	corners, ArUco_id, _ = cv2.aruco.detectMarkers(imgGray, dictionary, parameters=param)

	for i in range(len(ArUco_id)):
		Detected_ArUco_markers[int(ArUco_id[i])] = corners[i]

	return Detected_ArUco_markers


def Calculate_orientation_in_degree(Detected_ArUco_markers):
	ArUco_marker_angles = {}

	markerIds = []
	markerCorners = []

	for x in Detected_ArUco_markers:
		p = x
		q = Detected_ArUco_markers[x]
		markerIds.append(p)
		markerCorners.append(q)

	for i in range(len(markerIds)):
		(topLeft, topRight, bottomRight, bottomLeft) = markerCorners[i][0]
		topLeft = (int(topLeft[0]), int(topLeft[1]))
		topRight = (int(topRight[0]), int(topRight[1]))

		theta = math.atan2((topRight[0] - topLeft[0]), (topRight[1] - topLeft[1]))

		angle = int(np.rad2deg(theta))
		if angle < 0:
			angle += 360

		ArUco_marker_angles[markerIds[i]] = angle



	return ArUco_marker_angles


def mark_ArUco(img, Detected_ArUco_markers, ArUco_marker_angles):

	markerIds = []
	markerCorners = []
	angles = []

	for x in Detected_ArUco_markers:
		p = x
		q = Detected_ArUco_markers[x]
		markerIds.append(p)
		markerCorners.append(q)

	for x in ArUco_marker_angles:
		a = ArUco_marker_angles[x]
		angles.append(a)

	img = aruco.drawDetectedMarkers(img, markerCorners)

	for i in range(len(markerIds)):
		center = markerCorners[i][0]

		M = cv2.moments(center)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])

		(topLeft, topRight, bottomRight, bottomLeft) = markerCorners[i][0]
		topLeft = (int(topLeft[0]), int(topLeft[1]))
		topRight = (int(topRight[0]), int(topRight[1]))
		bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
		bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))

		label = str(angles[i])

		cv2.circle(img, (cX, cY), 1, (0, 0, 255), 8)
		cv2.circle(img, topLeft, 1, (125, 125, 125), 8)
		cv2.circle(img, topRight, 1, (0, 255, 0), 8)
		cv2.circle(img, bottomRight, 1, (180, 105, 255), 8)
		cv2.circle(img, bottomLeft, 1, (255, 255, 255), 8)
		cv2.putText(img, str(markerIds[i]), (cX+5, cY+5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
		cv2.putText(img, label, bottomLeft, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

	return img





