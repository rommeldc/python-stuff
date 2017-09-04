''' This script shuffles and appends number prefix on all mp3 files in the target directory '''


import os
import random

TARGET = '/Rommel'

target_loc = os.getcwd() + TARGET
filelist = []

os.system('clear')
#for root, dirs, files in os.walk("."):
files = os.listdir(target_loc)
for name in files:
    #print name
    name_list =  os.path.splitext(name)
    if (name_list[1] == '.mp3') or (name_list[1] == '.MP3'):
    	filelist.append(name)

#print filelist
#Now randomize the contents of the list
random.shuffle(filelist)
#print filelist
#loop thru the list and start appending the numbers
ctr = 0
for names in filelist:
	if names[:3].isdigit():
		newname = '%03d' % (ctr) + names[3:]
		if newname[3] != '_':
			newname = newname[:3] + '_' + newname[3:]
	else:
		newname = '%03d' % (ctr) + '_' + names
	#Rename the target file
	print 'Renaming %s >> %s' % (names, newname)
	os.rename( os.path.join(target_loc,names), os.path.join(target_loc,newname) )
	ctr = ctr + 1

#Check if the files were renamed
#files = os.listdir(target_loc)
#print files

print 'Renaming completed!!!'

