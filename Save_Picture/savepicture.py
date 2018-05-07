import cv2
import pathlib
import datetime
import os
import sys

#   -Wayne Campbell
#   Opens Webcam and displays feed. Also creates directory to store images based on time and date
#   Pased from the C# main program.
#   argv[0] = the name of the folder to create (string)
#   argv[1] = show opencv output (-true or -false)

dir = '//' + sys.argv[1]

#Path Of Directory to create
print (os.getcwd())
print ( os.getcwd() + dir)
os.makedirs(os.getcwd() + dir)

#Preview window and webcam setup
if sys.argv[2] == 'true':
    cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

# Get Frame to test for camera connection
if vc.isOpened(): 
    rval, frame = vc.read()
else:
    rval = False

#Save One Frame, this frame is used for initial segmentation
cv2.imwrite(os.path.join(os.getcwd() + dir,'initial.png'),frame)

#Loop through webcam frames, save and show.
while rval:
    cv2.imwrite(os.path.join(os.getcwd() + dir,'test.png'),frame)
    if sys.argv[2] == 'true':
        cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(2000)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")