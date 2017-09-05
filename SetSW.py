''' This script creates a symbolic link (junction in Windows '''
import os
import fnmatch
import shutil
import stat
import sys

curr_path = os.getcwd()
target_link = curr_path + '\\SW'

if len(sys.argv) > 1:
    link_path = curr_path + '\\' + sys.argv[1]

    #Remove symbolic link if existing
    if os.path.isdir(target_link):
        cmd = 'rmdir ' + target_link
        os.system(cmd)
        print('Removing existing symbolic link')
    #Create the command 
    cmd = 'mklink /J ' + target_link + ' ' + link_path

    print('Setting symbolic link ' + target_link + ' from ' + link_path)
    # Now set the hard link
    os.system(cmd)

    print('Done')
else:
    print('No target folder specified..\n')
    #print os.path.readlink(target_link) 
    os.system('dir')
