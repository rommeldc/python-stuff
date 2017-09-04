''' This scripts walks thru a folder and subfolders looking for specific files deemed as thrash to delete '''



import os
import shutil
import stat
import zipfile
import openpyxl
import string
import subprocess
from datetime import datetime
from re import sub
import csv
IMPL_LIST = ['.', '_']
# -------------------------------------------------------------------------
''' Main Class '''
class MetaCleaner:
# ------------------
    def __init__(self):
        self.count = 0
        self.found = 0
        self.list = IMPL_LIST

# ----------------------------------------------------------
    def Run(self, dir):
        if os.path.isdir(dir):
            for root, dirs, files in os.walk(dir):
                for file in files:
                    if file[:1] in self.list:
                        target = os.path.join(root, file)
                        os.chmod(target, stat.S_IWRITE)
                        os.remove(target)
                        # print(target)
                        self.count = self.count + 1
        print('Found and deleted {0} items..'.format(self.count))
'''End of CodeReview class definition'''
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# MAIN program.
# -------------------------------------------------------------------------
if __name__ == '__main__':
    time_started = datetime.now().replace(microsecond=0)
    os.system('cls')
    print('==========================')
    print('Cleaning started @ {0}'.format(time_started) )
    print('==========================')
    search_dir = r'C:\Workspace\Scripts\MetaCleaner\Target_Drive'
    meta_cleaner = MetaCleaner()
    meta_cleaner.Run(search_dir)
    time_subproc = datetime.now().replace(microsecond=0)
    print('==========================')
    print('Cleaning completed. Duration = {0}'.format(time_subproc - time_started) )
    print('==========================')
