from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import argparse
import sys
import time
import cv2
import csv

import numpy as np
import tensorflow as tf

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

def give_prediction(image, input_height=299, input_width=299,
				input_mean=0, input_std=255):
    input_name = "file_reader"
    output_name = "normalized"
    np_image = np.asarray(image)

    float_caster = tf.cast(np_image, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.Session()
    result = sess.run(normalized)

    with tf.Session(graph=graph) as sess:
            start = time.time()
            results = sess.run(output_operation.outputs[0],
                            {input_operation.outputs[0]: t})
            end=time.time()
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)
    return labels, results
    #print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))

    #for i in top_k:
    #    print(labels[i], results[i])

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
    print(y1 + " " + y2 + " " + x1 + " " + x2)
    crop_img = this_image[int(y1) : int(y2),int(x1) : int(x2)]
    cv2.imshow("name", crop_img)
    return crop_img
  
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

    graph = load_graph(model_file)
    

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name);
    output_operation = graph.get_operation_by_name(output_name);

    #Capture Video to send to created graph
    #vc = cv2.VideoCapture("tf_files/test_videos/20180213_191717.mp4")
    vc = cv2.VideoCapture(1)

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
                numberOfParkingSpots = int(row[0])

    while rval:
        #Loop through csv data
        cv2.imshow('frame', frame)
        with open('Choose_Parking_Spots/csv/' + currentCSVfile, 'r') as np:
            readerOfCSVData = csv.reader(np, delimiter=',')
            #Loop through given parking spaces
            for row in readerOfCSVData:
                #Crop Image based on csv file
                #Find Prediction of image

                #WAY WITHOUT SAVING FILE
                ##cropped_image = crop_image(frame, row[1], row[2], row[3], row[4])
                ##result_labels, result_result = give_prediction(cropped_image)

                #WAY WITH SAVING FILE(SLOWER)
                print(row[0])
                #cropped_image = crop_image(frame.copy(), row[1], row[2], row[3], row[4])
                cropped_image = frame[int(row[1]) : int(row[2]),int(row[3]) : int(row[4])]
                height, width, channels = cropped_image.shape
                print(height)
                print(width)
                ##cv2.imshow("name", cropped_image)
                ##cv2.imwrite(os.getcwd() + '//tf_files//saveTestImage.jpg', cropped_image )
                ##t = read_tensor_from_image_file(file_name,
                ##                            input_height=input_height,
                ##                           input_width=input_width,
                ##                            input_mean=input_mean,
                ##                            input_std=input_std)

                ##with tf.Session(graph=graph) as sess:
                ##    start = time.time()
                ##    results = sess.run(output_operation.outputs[0],
                ##                    {input_operation.outputs[0]: t})
                ##    end=time.time()
                ##results = np.squeeze(results)

                ##top_k = results.argsort()[-5:][::-1]
                ##labels = load_labels(label_file)

                ##print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))

                ##for i in top_k:
                ##    print(labels[i], results[i])

                #Print Rectangle at position with information
                cv2.rectangle(frame, (int(row[1]),int(row[2])), (int(row[3]), int(row[4])), (0,255,0),2)
                cv2.imshow('frame', frame)
                print(row)
            
            rval, frame = vc.read()
            key = cv2.waitKey(1)
            if key == 27: # exit on ESC
                break
    vc.release()
    exit()