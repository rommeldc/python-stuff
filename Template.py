import os
import stat
import sys
from datetime import datetime
import argparse

# -------------------------------------------------------------------------
''' Main Class '''
class ClassTemplate:
# ------------------
    def __init__(self, args):
        os.system('cls')
        self.start_time = datetime.now().replace(microsecond=0)
        self.end_time = 0
        self.stdout_orig = sys.stdout
        self.verbose = args.verbose
        self.output = open('Output.txt', 'w')
# ------------------
    def __del__(self):
        self.output.close()
        self.end_time = datetime.now()
        print('==========================')
        print('Finished. Duration = {0}'.format(self.end_time - self.start_time) )
        print('==========================')
# ------------------
    def StdOutToFile(self):
        sys.stdout = open('Output.txt', 'w')
# ------------------
    def StdOutRestore(self):
        sys.stdout = self.stdout_orig

# ------------------
    def Print(self,msg, toFile=False):
        if self.verbose and (toFile == False):
            print(msg)
        else:
            self.output.write(str(msg) + '\n')
# ------------------
    def Run(self, path):
        print('Run')
'''End of CodeReview class definition'''
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# MAIN program.
# -------------------------------------------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",  
                        help="enable verbose mode",
                        default = False,
                        action="store_true")
    parser.add_argument("-f", "--file", 
                        type = str,
                        default = 'DD DB Bubbles.xlsm',
                        help="The excel file where the table resides",
                        )
    parser.add_argument("-s", "--sheet", 
                        type = str,
                        default = 'Data Range',
                        help="The excel file worksheet name where the table resides",
                        )
    parser.add_argument("-c", "--column", 
                        type = int,
                        default = 0,
                        help="The column to check for worst case matching",
                        )
    args = parser.parse_args()
    obj = ClassTemplate(args)
    obj.Run()
