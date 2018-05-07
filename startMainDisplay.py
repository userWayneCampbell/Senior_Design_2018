# USAGE
# python photo_booth.py --output output

from __future__ import print_function
from Machine_Learning_Python.mainDisplay import MainDisplay
from imutils.video import *
import imutils
from imutils.video import VideoStream
import argparse
import time

#Parse
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="Not Used")
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="Not Used")
args = vars(ap.parse_args())

# initialize the video stream and warmup camera
print("[INFO] warming up camera...")

vs = WebcamVideoStream(src=0).start()
time.sleep(2.0)

# start the app
pba = MainDisplay(vs, args["output"])
pba.root.mainloop()
