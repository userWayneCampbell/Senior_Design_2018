from tkinter import *
from tkinter import messagebox
import os
from time import gmtime, strftime
import time
import cv2
from imutils.video import *
import shutil

#OpenCV port for camera input (Change if you want to use second camera)
CAMERA_INPUT = 0

class Window(Frame):

    def __init__(self, master=None):
        
        Frame.__init__(self, master)   
            
        self.master = master

        self.init_window()

    #Creation of init_window
    def init_window(self):

        self.master.title("Capstone 2018: Start Menu")
        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)
        
        config = Menu(menu)
        config.add_command(label="Create Parking Lot Session Positions", command=self.client_selectParkingSpot)
        config.add_command(label="Delete All Sessions", command=self.client_deleteSessions)
        config.add_command(label="Run Main Display", command=self.client_mainView)
        config.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label = "Config/Run/Exit", menu = config)

        about = Menu(menu)
        about.add_command(label="Senior Project Team Info", command=self.client_Info)
        menu.add_cascade(label = "About", menu = about)
       
    #Runs File to Select Parking Spaces and Save Them As A File
    def client_selectParkingSpot(self):
        os.system('python Choose_Parking_Spots/crop_image_new.py')

    #Delete Sessions
    def client_deleteSessions(self):
        shutil.rmtree(os.getcwd() + '/Choose_Parking_Spots/csv/')
        os.makedirs(os.getcwd() + '/Choose_Parking_Spots/csv/')
    
    #Choose your sessions, and run tensorflow display
    def client_mainView(self):
        os.system('python Choose_CSV/choose_csv.py')
        os.system('python startMainDisplay.py --output output')

    #Display Information about Senior Project Team
    def client_Info(self):
        win = Toplevel()
        win.title('About')
        win.geometry("500x100")
        message = "Ohio Northern University Senior Design \nReal-Time Parking Monitor"
        Label(win, text=message, font='Helvetica 10 bold').pack()
        message = "\n Members: Wayne Campbell, Bryce Gray, Miranda Huddle, Hayden Shenfield \n Advisor: Dr. Youssfi"
        Label(win, text=message, font='Helvetica 9').pack()
        Button(win, text='Exit', command=win.destroy).pack()
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
    time.sleep(2)
    #Wait and Take better picture
    cv2.imwrite(os.path.join(dir,'initial.png'),frame)
    vc.release

#Save time for directory creation/Create directory
directory = "Picture_Saves/" + strftime("%Y_%m_%d_%H_%M_%S", gmtime())
#print(os.getcwd() + "//" +directory)
os.makedirs(directory)
saveImageToDir(directory)

#Display Menu
root = Tk()
root.geometry("600x150")
app = Window(root)
root.mainloop()  
