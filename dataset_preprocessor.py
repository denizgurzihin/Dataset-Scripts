import sys
import os
import csv

# NOTE this will slice videos with taking input csv and videos should be same dir

def get_videofilename_from_url(video_url):
    filename = video_url[len(video_url)-11:]
    return filename + ".mp4"

label_set = set()
dataset_item_list = []

with open('turkish_audiovisual_word_dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            dataset_item = {
                "video_url": row[0], # TODO change this to videoId
                "label": row[1],
                "start": row[2],
                "end": row[3]
            }
            dataset_item_list.append(dataset_item)
            label_set.add(row[1])
            line_count += 1


# create label dataset folders
for each_label in label_set:
    if not os.path.exists(each_label):
        os.makedirs(each_label)


for each_dataset_item in dataset_item_list:
    video_file = get_videofilename_from_url(each_dataset_item['video_url'])
    label_folder_count = len(os.listdir(os.getcwd() + os.sep + each_dataset_item['label']))
    target_video = each_dataset_item['label'] + "_" + video_file[:11] + "_" + str(label_folder_count + 1) + ".mp4"
    target_video_path = os.getcwd() + os.sep + each_dataset_item['label'] + os.sep + target_video
    if os.path.exists(video_file):
        command = "./ffmpeg" + " -i " + video_file + " -ss " + each_dataset_item['start'] +  " -to " + each_dataset_item['end'] + " -c:v libx264 -c:a aac " + target_video_path
        os.system(command)
    else:
        print("WARNING, video not found: " + video_file)

print("FINISHED....")
