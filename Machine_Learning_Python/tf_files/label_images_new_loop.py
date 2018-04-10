from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import argparse
import sys
import time
import cv2
import csv
import time

import numpy as np
import tensorflow as tf

CAMERA_INPUT = 0

#Disable CPU instruction set
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

numberOfParkingSpots = 0 
readerOfCSVData = []
currentCSVfile = ""

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

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

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)
  
if __name__ == "__main__":
    ReadCSVData()
    file_name = ""
    model_file = "Machine_Learning_Python/tf_files/retrained_graph.pb"
    label_file = "Machine_Learning_Python/tf_files/retrained_labels.txt"
    input_height = 224
    input_width = 224
    input_mean = 128
    input_std = 128
    input_layer = "input"
    output_layer = "final_result"

    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="image to be processed")
    parser.add_argument("--graph", help="graph/model to be executed")
    parser.add_argument("--labels", help="name of file containing labels")
    parser.add_argument("--input_height", type=int, help="input height")
    parser.add_argument("--input_width", type=int, help="input width")
    parser.add_argument("--input_mean", type=int, help="input mean")
    parser.add_argument("--input_std", type=int, help="input std")
    parser.add_argument("--input_layer", help="name of input layer")
    parser.add_argument("--output_layer", help="name of output layer")
    parser.add_argument("--camera", help="number of opencv camera")
    args = parser.parse_args()

    if args.graph:
        model_file = args.graph
    if args.image:
        file_name = args.image
    if args.labels:
        label_file = args.labels
    if args.input_height:
        input_height = args.input_height
    if args.input_width:
        input_width = args.input_width
    if args.input_mean:
        input_mean = args.input_mean
    if args.input_std:
        input_std = args.input_std
    if args.input_layer:
        input_layer = args.input_layer
    if args.output_layer:
        output_layer = args.output_layer
    if args.camera:
        CAMERA_INPUT = int(args.camera)
        print(CAMERA_INPUT)

    graph = load_graph(model_file)
    

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name);
    output_operation = graph.get_operation_by_name(output_name);

    #Capture Video to send to created graph
    vc = cv2.VideoCapture(CAMERA_INPUT)

    # Get Frame to test for camera connection
    if vc.isOpened(): 
        rval, frame = vc.read()
    else:
        rval = False

    height, width, channels = frame.shape

    print(height)
    print(width)
    print(file_name)
    print(os.getcwd() + '//tf_files//saveTestImage.jpg')
    cv2.imwrite(os.getcwd() + '//tf_files//saveTestImage.jpg', frame )

    with open('Choose_Parking_Spots/csv/' + currentCSVfile, 'r') as np:
            readerOfCSVData = csv.reader(np, delimiter=',')
            for row in readerOfCSVData:
                print(row)
                numberOfParkingSpots = int(row[0])
    frame_count = 0
    fps_start = time.time()
    with tf.Session(graph=graph) as sess:
        print("new session")
        while rval:
        #Loop through csv data
        #cv2.imshow('frame', frame)

            #every # frames
            if frame_count%1000==0:
                    print(frame_count)
                
                    with open('Choose_Parking_Spots/csv/' + currentCSVfile, 'r') as np:
                        readerOfCSVData = csv.reader(np, delimiter=',')
                        #Loop through given parking spaces
                        for row in readerOfCSVData:
                            #Crop Image based on csv file
                            #Find Prediction of imag
                            cropped_image = crop_image(frame.copy(), row[1], row[2], row[3], row[4])
                            height, width, channels = cropped_image.shape
                            
                            #Just reshape to 1 dimension
                            cropped_image1 = cv2.resize(cropped_image, (224,224))
                            #cv2.imshow("name", cropped_image)
                            #cv2.imshow("name1", cropped_image1)
                            one_dimension = cropped_image1.reshape(1,cropped_image1.shape[0],cropped_image1.shape[1],cropped_image1.shape[2])

                            #Get Results from tensorflow
                            start = time.time()
                            results = sess.run(output_operation.outputs[0],{input_operation.outputs[0]: one_dimension})
                            end=time.time()

                            #Print Results
                            resultList = results.tolist()
                            print('Car Prediction: ' + str(resultList[0][0]))
                            print('Space Prediction: ' + str(resultList[0][1]))
                            #print('Evaluation time (1-image): {:.3f}s\n\n'.format(end-start))

                            if resultList[0][0] > .1:
                                print(str(row[0] + ' CAR = 1'))
                                color = [0,255,0]
                            else:
                                print(str(row[0] + ' CAR = 0'))
                                color = [255,0,0]

                            #Print Rectangle at position with information
                            if True:
                                cv2.rectangle(frame, (int(row[1]),int(row[2])), (int(row[3]), int(row[4])), (color[0],color[1],color[2]),1)
                                cv2.imshow('frame', frame)
                            fps_current = time.time()
                            #print(frame_count/(fps_current-fps_start))

                    rval, frame = vc.read()
                    
                    key = cv2.waitKey(1)
                    if key == 27: # exit on ESC
                        break
            frame_count += 1
    vc.release()
    exit()