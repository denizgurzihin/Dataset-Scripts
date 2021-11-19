# import the necessary packages
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import os

# initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# get current working directory and go to Data part
cwd = os.getcwd()
next_path = cwd + os.sep + "Data" #This Data field can be change through the directory depends on your where data is
os.chdir(next_path)

#get the names of all labes
label_names = os.listdir()

#create a variable for number of frames in videos
all_frame_numbers = []
all_video_name = []

for label in label_names:
    #return label name as str to change directory as label
    label_name = str(label)
    os.chdir(label_name)

    #get the label_name path, in order to return back
    label_names_path = os.getcwd()

    #create a Mouth_Area directory and get it is path
    mouth_area_dir_path = os.getcwd() + os.sep + "Mouth_Area"

    # change directory as to Mouth_Area directory
    os.chdir(mouth_area_dir_path)

    #get all the videos in the Mouth_Area directory in one of the label
    mouth_Area_Videos = os.listdir()
    #number_videos_in_mouth_area = len(mouth_Area_Videos)

    # counter for name
    counter = 0

    #for every video in a label_name path
    for video in mouth_Area_Videos:
        #count_frames in video
        frame_counter = 0

        counter += 1

        all_video_name.append(video)

        #open the video
        cap = cv2.VideoCapture(video)

        #original image
        orig_image = []

        # Check if camera opened successfully
        if (cap.isOpened() == False):
            print("Error opening video stream or file")
        else:
            while (cap.isOpened()):
                ret, frame = cap.read()

                #check, if we have finished the video or not
                if ret == False:
                    break
                else:
                    frame_counter += 1

                    # convert frames into gray
                    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    orig_image.append(frame_gray)
                    #cv2.imshow('frame', frame_gray)
                    #print(frame_gray.shape)

                #cv2.waitKey(1)
        #cv2.destroyAllWindows()

        all_frame_numbers.append(frame_counter)

    #change back to label path
    os.chdir(label_names_path)
    #change to the data path
    os.chdir(next_path)

file = open("frame_number_with_videos.txt","w")
file1 = open("just_frame_number.txt","w")
for i in range(len(all_frame_numbers)):
    file_input = str(all_video_name[i]) + " is contain " + str(all_frame_numbers[i]) + " frames...\n"
    file.write(file_input)
    file1_input = str(all_frame_numbers[i])+"\n"
    file1.write(file1_input)

file.close()
file1.close