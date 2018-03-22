from tkinter import *
import os
from time import gmtime, strftime
import cv2

class Window(Frame):

    def __init__(self, master=None):
        
        Frame.__init__(self, master)   
            
        self.master = master

        self.init_window()

    #Creation of init_window
    def init_window(self):

        self.master.title("Parking Spot Predictor")
        self.pack(fill=BOTH, expand=1)

        selectParkingSpotButton = Button(self, text="Define Parking Spots",command=self.client_selectParkingSpot, height = 10, width = 20)
        selectParkingSpotButton.place(x=5, y=5)

        sessionViewerButton = Button(self, text="Session Viewer",command=self.client_sessionViewer, height = 10, width = 20)
        sessionViewerButton.place(x=205, y=5)

        mainViewButton = Button(self, text="Main Viewer",command=self.client_mainView, height = 16, width = 20)
        mainViewButton.place(x=405, y=5)

        exitButton = Button(self, text="Exit", command=self.client_exit, height = 5, width = 45)
        exitButton.place(x=5, y=175)

       
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
        os.system('python Machine_Learning_Python/tf_files/label_images_new_loop.py --graph=Machine_Learning_Python/tf_files/retrained_graph.pb --image=Machine_Learning_Python/tf_files/saveTestImage.jpg')

    #Python Exit Command
    def client_exit(self):
        exit()

def saveImageToDir(dir):
    vc = cv2.VideoCapture(0)

    # Get Frame to test for camera connection
    if vc.isOpened(): 
        rval, frame = vc.read()
    else:
        rval = False

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
