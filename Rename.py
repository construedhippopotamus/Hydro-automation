#-------------------------------------------------------------------------------
# Name:        replace
# Purpose:
#
# Author:      Jenny.Mital
#
# Created:     08/12/2017
# Copyright:   (c) Jenny.Mital 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
#from shutil import copyfile

filepath = r"C:\Users\Pizzagirl\Documents\Travel\New folder"

#os.chdir allows the python file to be in a different folder than the files whose names are changed
os.chdir(filepath)
allfile=os.listdir(filepath)


print allfile


for file1 in allfile:
    #copyfile(file1, "~" + file1)
    dst=file1.replace("50", "25")
    os.rename(file1, dst)


