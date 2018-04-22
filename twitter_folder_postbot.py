# this is a simple twitter bot
# will start uploading an entire folder with images 
# to the account designated by the access keys

import os
import sys
import time
import datetime
from TwitterAPI import TwitterAPI

# defining parameters
MESSAGE_TEXT = "postbot upload"
DELAY_TIME = 200; # in seconds
CONSUMER_KEY = 'enter here';
CONSUMER_KEY_SECRET = 'enter here';
ACCESS_TOKEN = 'enter here';
ACCESS_TOKEN_SECRET = 'enter here';


# program start
api = TwitterAPI(CONSUMER_KEY, CONSUMER_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET);
				 

current_dir = os.getcwd()
folder_image_list = [];
posted_image_list = [];

# check for images in folder
for file in os.listdir(current_dir):
	if (file.endswith(".jpg") or file.endswith(".bmp") or file.endswith(".png")):
		folder_image_list.append(file)

if(len(folder_image_list)==0):
	print("There are no images to upload and post from the folder");
	os.system('pause');
	sys.exit();
print("Found " + str(len(folder_image_list)) + " images in folder, getting ready to post")
# check if older images have already been posted based on postbot file
file_check = False;
for file in os.listdir(current_dir):
	if file.endswith(".txt"):
		if file.startswith("twitter_postbot"):
				file_check = True;
				old_file = file;

# set up a file to 				
if(file_check):
	fr = open(old_file,"r");
	for line in fr.readlines():
		posted_image_list.append(line.strip('\n'));
	filename = old_file;
	print("Previous postbot run detected, will resume from where it left off")
else:
	timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M");
	filename = "twitter_postbot_" + timestamp + ".txt";
	
fio = open(filename,"w");

# main loop of program
while(True):
	print("Preparing to upload and post images from folder")
	for img in folder_image_list:
		if(img not in posted_image_list):
			imgfile = open(img, 'rb');
			data = imgfile.read();
			# attempt to upload
			request = api.request('media/upload', None, {'media':data});
			if(request.status_code == 200):
				# success
				print("Successfully uploaded image " + img + " , preparing to post")
				media_id = request.json()['media_id'];
				# attempt to post
				request = api.request('statuses/update', {'status': MESSAGE_TEXT, 'media_ids': media_id});
				if(request.status_code == 200):
					# success
					print("*** Successfully posted image " + img);
					posted_image_list.append(img);
					fio.write(img);
					# wait for 5 minutes before another image
					print("Waiting " + str(DELAY_TIME) + " seconds to post again")
					time.sleep(DELAY_TIME);
				else:
					print("Error attempting to post image tweet");
			else:
				print("Error attempting to upload image files");
	
	print("Finished posting images from folder!")
	fio.close();
	sys.exit();
	