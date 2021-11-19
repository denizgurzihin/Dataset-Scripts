# import the necessary packages
from imutils import face_utils
import numpy as np
import dlib
import cv2
import os

# initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# get current working directory and go to Data part
cwd = os.getcwd()

# create a Cropped_Mouth_Area directory and get it is path
mouth_area_dir = os.makedirs("4_Cropped_Mouth_Area_Dataset")
mouth_area_dir_path = os.getcwd() + os.sep + "4_Cropped_Mouth_Area_Dataset"

next_path = cwd + os.sep + "Data" #This Data field can be change through the directory depends on your where data is
os.chdir(next_path)

#get the names of all labes
label_names = os.listdir()

for label in label_names:
    #return label name as str to change directory as label
    label_name = str(label)
    os.chdir(label_name)

    #get the label_name path, in order to return back
    label_names_path = os.getcwd()

    #get all the videos in the label directory
    all_videos = os.listdir()

    #go to the 4_Cropped_Mouth_Area folder and create a label directory
    os.chdir(mouth_area_dir_path)
    mouth_area_label_dir = os.makedirs(str(label))
    mouth_area_label_dir_path = os.getcwd() + os.sep + str(label)

    #return back to the normal label path
    os.chdir(label_names_path)

    #for every video in a label_name path
    for video in all_videos:
        #open the video
        cap = cv2.VideoCapture(video)

        #change directory as to Mouth_Area directory
        os.chdir(mouth_area_label_dir_path)

        #create the filename for cropped video
        filename = video[0:len(video)-4] + "_MouthArea.mp4"

        # for saving video(size parameter ayarlancak)
        out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), 10, (32, 32), 0)

        # Check if camera opened successfully
        if (cap.isOpened() == False):
            print("Error opening video stream or file")
        else:
            while (cap.isOpened()):
                ret, frame = cap.read()

                #check, if we have finished the video or not
                if ret == False:
                    # if it is the last frame of the video close the video writer
                    out.release()
                    break

                # convert frames into gray
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # detect the faces on the frame
                rects = detector(gray, 1)

                #get the number of faces ina frame
                number_of_face = len(rects)

                if (number_of_face == 0):
                    warning = video + "  _This video contains frame with no faces."
                    print(warning)
                    #release the video writer and delete the video
                    out.release()
                    os.remove(filename)
                    break

                elif (number_of_face > 1):
                    warning = video + "  _This video contains frame with more than one faces."
                    print(warning)
                    # release the video writer and delete the video
                    out.release()
                    os.remove(filename)
                    break

                elif (number_of_face == 1):
                    cv2.imshow('frame', gray)

                    # loop over the face detections
                    for (i, rect) in enumerate(rects):
                        # determine the facial landmarks for the face region, then convert the landmark (x, y)-coordinates to a NumPy array
                        shape = predictor(gray, rect)
                        shape = face_utils.shape_to_np(shape)

                        # loop over the face parts individually
                        for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
                            if (name == "mouth"):
                                # display the name of the face part on the image

                                # extract the ROI of the face region as a separate image
                                (x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
                                roi = gray[y:y + h, x:x + w]

                                # for resizing if we need this part and give decision on height and width
                                final = cv2.resize(roi, (32, 32))

                                # save as video
                                out.write(final)

                                # show the particular face part
                                cv2.imshow("Mouth Facial Marks", final)

                                # if we commend this waitkey we will done it faster, they are putting some delay with this delay we can see whats
                                #going on
                                #cv2.waitKey(1)
                                #cv2.waitKey(1)

            #release the video writer and video, destroy all windows with cv2
            out.release
            cap.release()
            cv2.destroyAllWindows()

        #change back to label path
        os.chdir(label_names_path)
    #change to the data path
    os.chdir(next_path)

print("Mouth Area has been found on all videos in all labels and mouth area has been cropped into a new folder corresponds to label...")
print("Folder name is 4_Cropped_Mouth_Area_Dataset")