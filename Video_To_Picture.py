# import the necessary packages
import numpy as np
import dlib
import cv2
import os

# initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# get current working directory and go to Data part
cwd = os.getcwd()

# create a Picture_Of_Mouth_Area directory and get it is path
picture_of_mouth_area_dir = os.makedirs("5_Picture_Of_Mouth_Area")
picture_of_mouth_area_dir_path = os.getcwd() + os.sep + "5_Picture_Of_Mouth_Area"

next_path = cwd + os.sep + "4_Cropped_Mouth_Area_Dataset" #This Data field can be change through the directory depends on your where data is
os.chdir(next_path)

#get the names of all labes
label_names = os.listdir()

for label in label_names:
    #return label name as str to change directory as label
    label_name = str(label)
    os.chdir(label_name)

    #get the label_name path, in order to return back
    label_names_path = os.getcwd()

    #go to the new folder and createa directory
    os.chdir(picture_of_mouth_area_dir_path)
    picture_label_dir = os.makedirs(str(label))
    picture_label_dir_path = os.getcwd() + os.sep + str(label)

    #return back to label folder
    os.chdir(label_names_path)

    #get all the videos in the Mouth_Area directory in one of the label
    mouth_Area_Videos = os.listdir()

    # counter for name
    counter = 0

    #for every video in a label_name path
    for video in mouth_Area_Videos:
        #count_frames in video
        frame_counter = 0

        counter += 1

        #open the video
        cap = cv2.VideoCapture(video)

        #original image
        orig_image = []

        # change directory as to Picture_Of_Mouth_Area directory
        os.chdir(picture_of_mouth_area_dir_path)

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
                    cv2.imshow('frame', frame_gray)
                    #print(frame_gray.shape)

                cv2.waitKey(1)
        cv2.destroyAllWindows()

        orig = frame_counter
        seq = np.zeros((192, 192))
        x_limit = 32
        y_limit = 32
        iterator_x = 0
        iterator_y = 0
        for i in range(0, 36):
            # seq[iterator_x:iterator_x+x_limit,iterator_y:iterator_y+y_limit] = orig_image[int((i*orig)/49)] movement along x-axis
            seq[iterator_y:iterator_y + y_limit, iterator_x:iterator_x + x_limit] = orig_image[int((i * orig) / 36)]  # movement along y-axis
            iterator_x = iterator_x + x_limit
            if iterator_x == 192:
                iterator_x = 0
                iterator_y = iterator_y + y_limit
        name = video[:len(video)-4] + "_" + str(counter) + '.jpg'
        #go to the neceesary places for writing image
        os.chdir(picture_label_dir_path)
        cv2.imwrite(name, seq)

        # change directory as back to Mouth_Area directory
        os.chdir(label_names_path)


    #change back to label path
    os.chdir(label_names_path)
    #change to the data path
    os.chdir(next_path)

print("Mouth Area has been converted to an .png image succesfully for all video in all label...")
print("This images folder is 5_Picture_Of_Mouth_Area")

