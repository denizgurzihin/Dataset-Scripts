# import the necessary packages
import dlib
import cv2
import os
import shutil

# initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# create a Cropped_Mouth_Area directory and get it is path
discarded_videos_dir = os.makedirs("2_Discarded_Videos")
discarded_videos_dir_path = os.getcwd() + os.sep + "2_Discarded_Videos"

# get current working directory and go to Data part
cwd = os.getcwd()
next_path = cwd + os.sep + "Data" #This Data field can be change through the directory depends on your where data is
os.chdir(next_path)

#get the names of all labes
label_names = os.listdir()

#list of videos will be deleted
discard_these_videos = []

for label in label_names:
    #return label name as str to change directory as label
    label_name = str(label)
    os.chdir(label_name)

    #get the label_name path, in order to return back
    label_names_path = os.getcwd()

    #get all the videos in the label directory
    all_videos = os.listdir()

    #for every video in a label_name path
    for video in all_videos:
        #print(video)
        delete_flag = False

        #open the video
        cap = cv2.VideoCapture(video)

        video_path = os.getcwd() + os.sep + video

        # Check if camera opened successfully
        if (cap.isOpened() == False):
            print("Error opening video stream or file")
        else:
            while (cap.isOpened()):
                ret, frame = cap.read()

                #check, if we have finished the video or not
                if ret == False:
                    # if it is the last frame of the video close the video writer
                    #out.release()
                    break

                # convert frames into gray
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # detect the faces on the frame
                rects = detector(gray, 1)

                #get the number of faces ina frame
                number_of_face = len(rects)

                if (number_of_face == 0):
                    warning = video + "  _This video contains frame with no faces so it will be discarded."
                    print(warning)
                    delete_flag = True
                    discard_these_videos.append(video)
                    break

                elif (number_of_face > 1):
                    warning = video + "  _This video contains frame with more than one faces so it will be discarded."
                    print(warning)
                    delete_flag = True
                    discard_these_videos.append(video)
                    break

            cap.release()
            print(video + "  _This video is nice...")
            if(delete_flag == True):
                shutil.move(video_path, discarded_videos_dir_path)
                #os.remove(video)
                print(video + "  _This video is discarded...")

    #change to the data path
    os.chdir(next_path)

print("\nThe discarded videos are listed in the below")
for discard_video in discard_these_videos:
    print(discard_video)
print("The number of discarded videos is/are : " + str(len(discard_these_videos)))

