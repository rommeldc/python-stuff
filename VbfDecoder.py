import os
import stat
import sys
from datetime import datetime
from xml.etree import ElementTree
import struct
import binascii
# -------------------------------------------------------------------------
''' Main Class '''
class VbfDecoder:
# ------------------
    def __init__(self, enable_debug=False):
        os.system('cls')
        # self.start_time = datetime.now().replace(microsecond=0)
        self.start_time = datetime.now()
        self.end_time = 0
        self.stdout_orig = sys.stdout
        self.bytearray = bytearray()
        self.xml_data = []
        self.start_addr = 0
        self.bytearray_len = 0
        self.end_addr = 0
        self.type_size = {'uint8' : 1, 'uint16' : 2, 'uint32': 4, 'int8' : 1, 'int16' : 2, 'int32': 4 }
        self.enable_debug = enable_debug
# ------------------
    def __del__(self):
        sys.stdout = self.stdout_orig
        # self.end_time = datetime.now().replace(microsecond=0)
        self.end_time = datetime.now()
        print('==========================')
        print('Parsing completed. Duration = {0}'.format(self.end_time - self.start_time) )
        print('==========================')
# ------------------
    def StdOutToFile(self):
        sys.stdout = open('Output.txt', 'w')
# ------------------
    def ToHex(self, value):
        return str( binascii.hexlify( struct.pack( ">I", value) ) , 'ascii') 
# ------------------
    def StdOutRestore(self):
        sys.stdout = self.stdout_orig
# ------------------
    def ReadVBF(self, target_file):
        f = open(target_file,"rb")
        found = False
        for line in f.readlines():
            '''Search for the end of the header '''
            if line[0] == ord('}'):
                found = True
                line = line[1:]
                ''' Following 4 bytes signify the start address'''
                self.start_addr = int(str(binascii.hexlify(line[:4]), 'ascii'), 16)
                line = line[4:]
                ''' Next 4 bytes signify the end address'''
                self.bytearray_len = int(str(binascii.hexlify(line[:4]), 'ascii'), 16)
                line = line[4:]
                self.end_addr = self.start_addr + self.bytearray_len
            if found:
                self.bytearray.extend(line)
                if self.enable_debug:
                    print(line)
        # print('==============================')
        if self.enable_debug:
            print('Start Address = {0}'.format( self.ToHex(self.start_addr) ) )
            print('End Address = {0}'.format( self.ToHex(self.end_addr) ) )
        # for x in self.bytearray:
            # print(binascii.hexlify(x), end = "", flush = True)

# ------------------
    def ParseXML(self, target_file):
        f = open(target_file, 'r')
        tree = ElementTree.parse(f)
        for node in tree.iter('data_items'):
            name = node.attrib.get('name')
            type = node.attrib.get('DataType')
            size = node.attrib.get('size')
            address = node.attrib.get('address')
            init_val = node.attrib.get('InitialValue')
            data_struct = node.attrib.get('StructureOfData')
            type_of_data = node.attrib.get('TypeOfData')
            '''Create the list for every entry'''
            entry_list = []
            entry_list.append(name)
            entry_list.append(type)
            entry_list.append(size)
            entry_list.append(address)
            entry_list.append(data_struct)
            entry_list.append(type_of_data)
            # entry_list.append(init_val)
            # print(entry_list)
            '''Add new entry to master list'''
            self.xml_data.append(entry_list)
# ------------------
    def GetSize(self, type):
        retval = self.type_size[type]
        if retval == None:
            retval = 1
        return retval
# ------------------
    def GetValue(self, address, size, type, data_struct):
        result = None
        ''' If size is unknown, try to get size from the type'''
        if size == None:
            size = self.GetSize(type)
        size = int(size)
        if (address >= self.start_addr) and ( (address + size) <= self.end_addr ):
            start_idx = address - self.start_addr
            # byte_array = str(binascii.hexlify( self.bytearray[start_idx : start_idx + size ] ), 'ascii')
            byte_array = self.bytearray[start_idx : start_idx + size ]
            # print(str(byte_array))
            if data_struct == '1D array':
                pass
            elif data_struct == '2D array':
                pass
            else:
                if type == 'uint16':
                    byte_array = struct.pack( ">H", struct.unpack("<H", byte_array)[0] )
                elif type == 'int16':
                    byte_array = struct.pack( ">h", struct.unpack("<h", byte_array)[0] )
                elif type == 'uint32':
                    byte_array = struct.pack( ">I", struct.unpack("<I", byte_array)[0] )
                elif type == 'int32':
                    byte_array = struct.pack( ">i", struct.unpack("<i", byte_array)[0] )

            result = str(binascii.hexlify( byte_array), 'ascii').upper()
        else:
            if self.enable_debug:
                print('{0} + {1} = {2} will be out of bounds!!'.format(address, size, address + size))
        return result
# ------------------
    def Run(self, vbf, xml):
        '''Redirect stdout to file'''
        self.StdOutToFile()
        self.ParseXML(xml)
        self.ReadVBF(vbf)
        
        '''Iterate the data_items to get the value for each'''
        for item in self.xml_data:
            # print(item)
            name = item[0]
            type = item[1]
            size = item[2]
            address = item[3]
            data_struct = item[4]
            type_of_data = item[5]
            # initval = item[5]
            
            value = self.GetValue( int(address, 16), size, type, data_struct )
            if value != None:
                print(item, end='', flush = True)
                print(' = {0}'.format(value), end='', flush = True)
                if data_struct == 'Scalar':
                    print(' ({0})'.format( int(value, 16) ), end='', flush = True)
                elif data_struct == '1D array':
                    if type_of_data == 'Character':
                        ascii = ''.join(chr(int(value[i:i+2], 16)) for i in range(0, len(value), 2))
                        print(' == (\"{0}\") '.format( ascii ), end='', flush = True)
                print('')
        '''Restore stdout'''
        self.StdOutRestore()
'''End of CodeReview class definition'''
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# MAIN program.
# -------------------------------------------------------------------------
if __name__ == '__main__':
    # curr_dir = os.getcwd()
    arg1 = 'vbffile'
    arg2 = 'xmlfile'
    enable_debug_msgs = False
    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
        if len(sys.argv) > 2:
            arg1 = sys.argv[2]
    decoder = VbfDecoder(enable_debug_msgs)
    decoder.Run(arg1, arg2)
