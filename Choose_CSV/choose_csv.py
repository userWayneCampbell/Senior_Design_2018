from tkinter import *
import os
from time import gmtime, strftime
import cv2
import csv

csv_data = []

class Window(Frame):

    def __init__(self, master=None):
        
        Frame.__init__(self, master)   
            
        self.master = master

        self.init_window()

    #Creation of init_window
    def init_window(self):

        self.master.title("Parking Spot Predictor")
        self.pack(fill=BOTH, expand=1)

        listOfCsvFiles = os.listdir("Choose_Parking_Spots/csv")

        self.variable = StringVar(self)
        self.variable.set(listOfCsvFiles[0])

        self.MenuCSV = OptionMenu(self, self.variable, * listOfCsvFiles)
        self.MenuCSV.pack()

        ButtonSubmit = Button(self, text="Use This Setting", command=self.Submit)
        ButtonSubmit.pack()

    def Submit(self):
        global csv_data
        csv_data = self.variable.get()
        print(csv_data)
        saveCSVData()
        exit()
        
#Save CSV Data
def saveCSVData():
    global csv_data
    with open('Choose_Parking_Spots/currentUsed.csv','w') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerows(csv_data)

#Display Menu
root = Tk()
root.geometry("200x120")
app = Window(root)
root.mainloop()  


