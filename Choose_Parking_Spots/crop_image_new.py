import cv2
import csv
import time
import os
from time import gmtime, strftime
from tkinter import messagebox
from tkinter import *

isSelecting = False
roi = []
w = 1
csv_data = []

#Tkinter UI Window Class
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)   
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):
        self.master.title("Save Session")
        self.pack(fill=BOTH, expand=1)

        L1 = Label(self, text="Name Of Session:")
        L1.place(x=20, y = 20)
        
        self.E1 = Entry(self, bd =5)
        self.E1.place(x=10, y= 50)

        ButtonEntry = Button(self, text="Save Session",command=self.saveInputCSVName, height = 2, width = 20)
        ButtonEntry.place(x=5,y=100)     

    def saveInputCSVName(self):
        returnCSV = saveCSVData(self.E1.get())
        print(returnCSV)
        exit()

#Save CSV Data
def saveCSVData(name):
    with open('Choose_Parking_Spots/csv/' + name + '.csv','w') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerows(csv_data)


#Get Recent Created Folder and grab image
def returnOriginalImage():
    directory = "Picture_Saves/"
    image_directory = max([os.path.join(directory,d) for d in os.listdir(directory)], key=os.path.getmtime)
    image_read_path = image_directory + "/initial.png"
    print(image_read_path)
    img = cv2.imread(image_read_path,cv2.IMREAD_UNCHANGED)
    #img = cv2.resize(img, (960, 540))  
    return img

#Used when user doesn't want to keep rectangle
def restoreBackupImage():
    currentImage = backupImage

#Updates backup image to print a new rectangle on area
def updateBackupImage( newImage ):
    backupImage = newImage

#Handles events pertaning to the main opencv window
def eventROI(event, x, y, flags, param):
    global isSelecting, roi, w, csv_string
    if event == cv2.EVENT_LBUTTONDOWN:
        isSelecting = True
        roi = [x,y,x,y]
    elif event == cv2.EVENT_MOUSEMOVE:
        if isSelecting == True:
            roi[2] = x
            roi[3] = y
    elif event == cv2.EVENT_LBUTTONUP:
        
        #answer = messagebox.askyesno("Question","Keep Recent Chosen Parking Spot?")
        answer = "Yes"
        if answer == "Yes":
            isSelecting = False
            roi[2] = x
            roi[3] = y
            print (w,y1,y2,x1,x2)
            #Create list to put into other csv list
            temp_list = [w,roi[0],roi[1],roi[2],roi[3]]
            csv_data.append(temp_list)
            #draw rectangles and save as new display image
            cv2.rectangle(backupImage, (roi[0],roi[1]), (roi[2], roi[3]), (0,255,0),2)
            updateBackupImage(currentImage)
            w = w + 1
        else:
            isSelecting = False
            restoreBackupImage()

#Display promt for name
def displayPromtForFileName():
    top = Tk()
    top.geometry("200x160")
    app = Window(top)
    top.mainloop()  


    

#Init Vars
windowNameMain = 'Choose Parking Spaces'
windowCropName='Parking Space: '
esc_keycode = 27
wait_time=1
currentImage = returnOriginalImage()
backupImage = returnOriginalImage()


if currentImage is not None:
    print("Cloned current image")
    clone = backupImage.copy()
    cv2.namedWindow(windowNameMain, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(windowNameMain, eventROI)

    while True:
        cv2.imshow(windowNameMain, currentImage)

        if len(roi) == 4:
            currentImage = backupImage.copy()
            roi = [0 if i < 0 else i for i in roi]
            cv2.rectangle(currentImage, (roi[0],roi[1]), (roi[2], roi[3]), (0,255,0),2)
            if roi[0] > roi[2]:
                x1 = roi[2]
                x2 = roi[0]
            else:
                x1 = roi[0]
                x2 = roi[2]
            if roi[1] > roi[3]:
                y1 = roi[3]
                y2 = roi[1]
            else:
                y1 = roi[1]
                y2 = roi[3]
            #Displays each car in seperate window for debugging
            crop_img = clone[y1 : y2,x1 : x2]

            if len(crop_img) and not isSelecting:
                cv2.namedWindow(windowCropName + " " + str(w - 1), cv2.WINDOW_AUTOSIZE)
                cv2.imshow(windowCropName + " " + str(w - 1), crop_img)
            
        k = cv2.waitKey(wait_time)
        if k == esc_keycode:
            cv2.destroyAllWindows()
            displayPromtForFileName()
            break

else:
    print ('''Error: Image Not Found''')