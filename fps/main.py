# import the necessary packages
from __future__ import print_function
from cam import WebcamVideoStream
from fps import FPS
import argparse
import imutils
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

cam1 = 0
cam2 = 1
cam3 = 2

# grab a pointer to the video stream and initialize the FPS counter
print("[INFO] sampling frames from webcam...")
stream1 = cv2.VideoCapture(cam1)
stream2 = cv2.VideoCapture(cam2)
stream3 = cv2.VideoCapture(cam3)
fps = FPS().start()
# loop over some frames
while fps._numFrames < args["num_frames"]:
	# grab the frame from the stream and resize it to have a maximum
	# width of 400 pixels
	(grabbed1, frame1) = stream1.read()
	(grabbed2, frame2) = stream2.read()
	(grabbed3, frame3) = stream3.read()
	frame1 = imutils.resize(frame1, width=400)
	frame2 = imutils.resize(frame2, width=400)
	frame3 = imutils.resize(frame3, width=400)
	# check to see if the frame should be displayed to our screen
	if args["display"] > 0:
		cv2.imshow("Frame1", frame1)
		cv2.imshow("Frame2", frame2)
		cv2.imshow("Frame3", frame3)
		key = cv2.waitKey(1) & 0xFF
	# update the FPS counter
	fps.update()
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
stream1.release()
stream2.release()
stream3.release()
cv2.destroyAllWindows()

# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs1 = WebcamVideoStream(src=cam1).start()
vs2 = WebcamVideoStream(src=cam2).start()
vs3 = WebcamVideoStream(src=cam3).start()
fps = FPS().start()
# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame1 = vs1.read()
	frame2 = vs2.read()
	frame3 = vs3.read()
	frame1 = imutils.resize(frame1, width=400)
	frame2 = imutils.resize(frame2, width=400)
	frame3 = imutils.resize(frame3, width=400)
	# check to see if the frame should be displayed to our screen
	if args["display"] > 0:
		cv2.imshow("Frame1", frame1)
		cv2.imshow("Frame2", frame2)
		cv2.imshow("Frame3", frame3)
		key = cv2.waitKey(1) & 0xFF
	# update the FPS counter
	fps.update()
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
cv2.destroyAllWindows()
vs1.stop()
vs2.stop()
vs3.stop()