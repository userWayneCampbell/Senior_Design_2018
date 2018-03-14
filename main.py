from tkinter import *
import os

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

        sessionViewerButton = Button(self, text="SessionViewer",command=self.client_sessionViewer, height = 10, width = 20)
        sessionViewerButton.place(x=205, y=5)

        exitButton = Button(self, text="Exit", command=self.client_exit, height = 5, width = 45)
        exitButton.place(x=5, y=175)

       
    #Runs File to Select Parking Spaces and Save Them As A File
    def client_selectParkingSpot(self):
        os.system('python Choose_Parking_Spots/crop_image_new.py')

    #View Sessions on live camera, and delete sessions (grab data from csv file and display it over a camera feed)
    def client_sessionViewer(self):
        #SessionViewerFunction()
        exit()

    #Python Exit Command
    def client_exit(self):
        exit()

#Display Menu
root = Tk()
root.geometry("400x280")
app = Window(root)
root.mainloop()  
