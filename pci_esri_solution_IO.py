#**************************************************** 
#
#			   I/O Functions
#
#****************************************************

import glob
import os
import shutil
import sys
import fnmatch

def normalize_path(directory_check): #Adds a backslash (\) if necessary.
	if directory_check.endswith('\\'):
		print "Normalization not required on io path: ", directory_check
		return directory_check
	
	else:
		norm_io_path = directory_check + '\\'
		print "io path normalized to: ", norm_io_path
		return norm_io_path
        
        
def get_inputs(input_directory, file_format, create_txt_mfile):
    print "checking for input files"
    if create_txt_mfile == 'YES':
        print "creating text mfile for batch processing"
        txt_mfile = open(input_directory + 'image_stack.txt', 'a')
        for r,d,f in os.walk(input_directory):
            for file in fnmatch.filter(f, file_format):
                print "found valid input file: ", file
                txt_mfile.write(os.path.join(r,file))
                txt_mfile.write('\n')
                
        txt_mfile.close()
        imgstack_mfile = input_directory + 'image_stack.txt'
        return imgstack_mfile
    else:
        input_files_list = []
        for r,d,f in os.walk(input_directory):
            for file in fnmatch.filter(f, file_format):
                print "found valid input file: ", file
                input_files_list.append(os.path.join(r,file))
        return input_files_list
    
def validate_files(file_path):
    if os.path.isfile(file_path):
        print "found the file: " + file_path
    else:
        print "Could not find " + file_path + "\n\nPlease check that the file exists\
 AND that the path is correct."
        exit()
