#-------------------------------------------------------------------------------
# Name:        replace
# Purpose:
#
# Author:      Jenny.Mital
#
# Created:     08/12/2017
# Copyright:   (c) Jenny.Mital 2017
# Licence:     <your licence>
#
#  Copy n-yr hydrology model and create other yrs.
#-------------------------------------------------------------------------------

import os
from shutil import copyfile

filepath = r"H:\pdata\159408\Calcs\Strmwater\Hydrology\Proposed Condition\Rational method"

#os.chdir allows the python file to be in a different folder than the files whose names are changed
os.chdir(filepath)
allfile=os.listdir(filepath)


for file in allfile:
    # ONLY rename .dat
    if file.endswith(".DAT"):
        src = file
        #replace(current, desired)
        dstlist = ["50", "25", "10", "05", "02"]

        for yr in dstlist:
            dst=file.replace("00", yr)
            copyfile(src, dst)
            print dst
            #os.rename(file1, dst)


