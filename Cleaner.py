''' This script deletes certain folders in a target path '''
import os
import fnmatch
import shutil
import stat
import sys

if len(sys.argv) > 1:

    os.system('cls')
    #path = os.getcwd() + "/testFolder"
    target = 'quality'
    #out_file = os.getcwd() + '\\output.txt'
    print(sys.argv)
    path = os.getcwd() + '\\' + sys.argv[1]
    print(path)
    count = 0
    #sys.stdout = open(out_file, 'w')
    print('Removing read-only attributes..')
    for dirpath, dirnames, files in os.walk(path):
        for file in files:
            os.chmod( os.path.join(dirpath, file), stat.S_IWRITE )      # Remove read-only if in case
    print('Done')
            
    for dirpath, dirnames, files in os.walk(path):
        if target in dirpath:
            print('Deleting ' + dirpath + ' ...')
            shutil.rmtree(dirpath)                  # Delete folder and contents
            print('Done')
            count += 1

    print(str(count) + " folders deleted")
else:
    print('No target folder specified!!!')
