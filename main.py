from tkinter import *
import os
from time import gmtime, strftime
import time
import cv2
from imutils.video import *

CAMERA_INPUT = 1

class Window(Frame):

    def __init__(self, master=None):
        
        Frame.__init__(self, master)   
            
        self.master = master

        self.init_window()

    #Creation of init_window
    def init_window(self):

        self.master.title("Parking Spot Predictor")
        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)
        
        config = Menu(menu)
        config.add_command(label="Create Parking Spot Setup", command=self.client_selectParkingSpot)
        config.add_command(label="Choose Session", command=self.client_sessionViewer)
        config.add_command(label="Load Session/Remove this eventually", command=self.client_mainView)
        config.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label = "Config Options", menu = config)
       
    #Runs File to Select Parking Spaces and Save Them As A File
    def client_selectParkingSpot(self):
        os.system('python Choose_Parking_Spots/crop_image_new.py')

    #View Sessions on live camera, and delete sessions (grab data from csv file and display it over a camera feed)
    def client_sessionViewer(self):
        #SessionViewerFunction()
        exit()
    
    #Function to run opencv with tensorflow
    def client_mainView(self):
        os.system('python Choose_CSV/choose_csv.py')
        os.system('python startMainDisplay.py --output output')
        #os.system('python Machine_Learning_Python/tf_files/label_images_new_loop.py --graph=Machine_Learning_Python/tf_files/retrained_graph.pb --image=Machine_Learning_Python/tf_files/saveTestImage.jpg --camera=' + str(CAMERA_INPUT))

    #Python Exit Command
    def client_exit(self):
        exit()

def saveImageToDir(dir):
    vc = cv2.VideoCapture(int(CAMERA_INPUT))
    time.sleep(2)

    # Get Frame to test for camera connection
    if vc.isOpened(): 
        rval, frame = vc.read()
    else:
        rval = False
    height, width, channels = frame.shape
    print(height)
    print(width)

    #Save One Frame, this frame is used for initial segmentation
    cv2.imwrite(os.path.join(dir,'initial.png'),frame)
    vc.release

#Save time for directory creation/Create directory
directory = "Picture_Saves/" + strftime("%Y_%m_%d_%H_%M_%S", gmtime())
#print(os.getcwd() + "//" +directory)
os.makedirs(directory)
saveImageToDir(directory)

#Display Menu
root = Tk()
root.geometry("600x280")
app = Window(root)
root.mainloop()  
