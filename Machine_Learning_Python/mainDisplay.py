# import the necessary packages
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
import csv
import time
import math

import numpy as np
import tensorflow as tf

numberOfParkingSpots = 0 
readerOfCSVData = []
currentCSVfile = ""

TIMER_LENGTH = 30


class MainDisplay:
	def __init__(self, vs, outputPath):
		
		#Store stream object, output, and set all frame variables to None
		self.vs = vs
		self.outputPath = outputPath
		self.frame = None
		self.thread = None
		self.stopEvent = None

		# Create TK Window
		self.root = tki.Tk()
		self.panel = None

		# Thread that pools for new frames from camera
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()

		# set a callback to handle when the window is closed
		self.root.wm_title("Capstone 2018: Vehicle Detection")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	def videoLoop(self):
		# DISCLAIMER:
		# I'm not a GUI developer, nor do I even pretend to be. This
		# try/except statement is a pretty ugly hack to get around
		# a RunTime error that Tkinter throws due to threading
		carTime = [0] * 50
		CarTimeOne = 0
		CAMERA_INPUT = 0

		#Disable CPU instruction set
		os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
		
		ReadCSVData()
		model_file = "Machine_Learning_Python/tf_files/retrained_graph.pb"
		label_file = "Machine_Learning_Python/tf_files/retrained_labels.txt"
		input_height = 224
		input_width = 224
		input_mean = 128
		input_std = 128
		input_layer = "input"
		output_layer = "final_result"
		input_name = "import/" + input_layer
		output_name = "import/" + output_layer
		graph = load_graph(model_file)
		input_operation = graph.get_operation_by_name(input_name)
		output_operation = graph.get_operation_by_name(output_name)
		
		with open('Choose_Parking_Spots/csv/' + currentCSVfile, 'r') as np:
			readerOfCSVData = csv.reader(np, delimiter=',')
			for row in readerOfCSVData:
				print(row)
				numberOfParkingSpots = int(row[0])
		frame_count = 0
		fps_start = time.time()
		time_start = 0
		with tf.Session(graph=graph) as sess:
			try:
				# keep looping over frames until we are instructed to stop
				while not self.stopEvent.is_set():
					# grab the frame from the video stream and resize it to
					# have a maximum width of 300 pixels
					self.frame = self.vs.read()
					self.frame = imutils.resize(self.frame, width=640, height=480)

					#Tensorflow Loop
					with open('Choose_Parking_Spots/csv/' + currentCSVfile, 'r') as np:
						readerOfCSVData = csv.reader(np, delimiter=',')
						for row in readerOfCSVData:
							#Resize Image for Tensorflow
							cropped_image = crop_image(self.frame.copy(), row[1], row[2], row[3], row[4])
							height, width, channels = cropped_image.shape
					
							cropped_image1 = cv2.resize(cropped_image, (224,224))

							one_dimension = cropped_image1.reshape(1,cropped_image1.shape[0],cropped_image1.shape[1],cropped_image1.shape[2])
							#Start Tensorflow Session
							with sess.as_default():
								tensor = tf.constant(one_dimension)

							resized = tf.image.resize_bilinear(tensor, [input_height, input_width])
							normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
							with sess.as_default():
								result = sess.run(normalized)
							#Record time and get results
							start = time.time()
							results = sess.run(output_operation.outputs[0],{input_operation.outputs[0]: result})
							end=time.time()
							#Debug print
							resultList = results.tolist()
							print(str(row[0]) + ' Car Prediction: ' + str(resultList[0][0]))

							#10 second Timer
							#New Car
							#color = [211,211,211]
							if resultList[0][0] > .9 and carTime[int(row[0])] == 0:
								color = [0,255,0]
								carTime[int(row[0])] = time.time() + TIMER_LENGTH
								print("Car New")

							#Car Past Time
							elif resultList[0][0] > .9 and time.time() > carTime[int(row[0])]:
								color = [0,0,255]	
								print("Car Past Time")

							elif resultList[0][0] > .9:
								color = [0,255,0]
								print("Car Still There")

							#Car Not There
							if resultList[0][0] < .9:
								color = [211,211,211]
								carTime[int(row[0])] = 0
								print("Car Left")

                            #Print Rectangle at position with information
							if True:
								cv2.rectangle(self.frame, (int(row[1]),int(row[2])), (int(row[3]), int(row[4])), (color[0],color[1],color[2]),2)
								#cv2.rectangle(self.frame, (int(row[1])+10,int(row[3])+10), (int(row[3])+50, int(row[4])-80), (255,255,255),-1)
								if carTime[int(row[0])] != 0 and carTime[int(row[0])] > 0:
									font = FONT_HERSHEY_COMPLEX_SMALL = 5
									cv2.putText(self.frame,str(math.floor((carTime[int(row[0])] - time.time()) * 100) / 100),(int(row[1])-50,int(row[2])), font, 1,(255,255,255),2,cv2.LINE_AA)
			
					#OpenCV needs BGR, PIL uses RGB, so swap channels and convert to formats
					image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
					image = Image.fromarray(image)
					image = ImageTk.PhotoImage(image)
			
					# if the panel is not None, we need to initialize it
					if self.panel is None:
						self.panel = tki.Label(image=image)
						self.panel.image = image
						self.panel.pack(side="left", padx=10, pady=10)
			
					# otherwise, simply update the panel
					else:
						self.panel.configure(image=image)
						self.panel.image = image

			except RuntimeError:
				print("[INFO] caught a RuntimeError")
			except e:
				print("[INFO] caught a RuntimeError")

	def onClose(self):
		# set the stop event, cleanup the camera, and allow the rest of
		# the quit process to continue
		print("[INFO] closing...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()


	

def load_graph(model_file):
	graph = tf.Graph()
	graph_def = tf.GraphDef()

	with open(model_file, "rb") as f:
		graph_def.ParseFromString(f.read())
	with graph.as_default():
		tf.import_graph_def(graph_def)

	return graph

def load_labels(label_file):
	label = []
	proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
	for l in proto_as_ascii_lines:
		label.append(l.rstrip())
	return label

#Read in CSV Data and Save to variables
def ReadCSVData():
	global numberOfParkingSpots
	global readerOfCSVData
	global currentCSVfile
	with open('Choose_Parking_Spots/currentUsed.csv','r') as fp:
		reader = csv.reader(fp, delimiter=',')
		for row in reader:
			currentCSVfile += ''.join(row)

#Crops image
def crop_image(this_image, r0,r1,r2,r3):
	if r0 > r2:
		x1 = r2
		x2 = r0
	else:
		x1 = r0
		x2 = r2
	if r1 > r3:
		y1 = r3
		y2 = r1
	else:
		y1 = r1
		y2 = r3
	#print("opencv display values: " + y1 + " " + y2 + " " + x1 + " " + x2)
	crop_img = this_image[int(y1) : int(y2),int(x1) : int(x2)]
	#cv2.imshow("name", crop_img)
	return crop_img