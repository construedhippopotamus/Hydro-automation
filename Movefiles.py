# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:21:24 2018

@author: Pizzagirl

Move files into folders by matching characters in the filename and folder name

NOTE: this currently won't work for 100yr files since the 1 is chopped off.

IMPORTANT: toggle status to determine whether files of same name in destination will be replaced.

"""
import re
import os
from shutil import move

#status = replace: overwrite destination file of same name
status = "replace"
#status = skip: don't move source file if destination file has same name
#status = "skip"

#location of files that need to be relocated
srcfolder=r'C:\Users\Pizzagirl\Documents\programming\MOVEFOLDER'

#location of main folder that holds folders that files should be moved to
destfolder = r'C:\Users\Pizzagirl\Documents\programming\DESTFOLDER'

#list of folders to move files into. Must all be within same destfolder
folders = ['2-YR', '5-YR', '10-YR', '25-YR', '50-YR']

#isolate numbers from file names
fldrnum = [int(f.replace('-YR', '')) for f in folders]
"""fldrnum = []
for f in folders:
    fldrnum = int()
"""
print "fldrnum", type(fldrnum[0])

dictionary = dict(zip(fldrnum, folders))
print "dictionary", dictionary

extension = ['DAT', 'DNA', 'HDG', 'RES']

allfile = os.listdir(srcfolder)

for file1 in allfile:
    
    
    #only move hydrology files
    if file1[-3:] in extension:
        print file1
        
        #extract numbers from filename
        filenum = int(re.findall(r'\d\d', file1)[0]) 
        #print "filenum", filenum
        
        #this line is supposed to return fldrnum that matches. not sure I trust it.
        matchnum = next(x for x in fldrnum if x == filenum)
        #print "matchnum", type(matchnum)

        #should return folder with same numbers as RM filename
        #could just add in "-YR" to each value to make folder name instead of using dictionary
        matchfldr = dictionary[matchnum]
        #print "matchfldr", matchfldr
        
        dest = os.path.join(destfolder, matchfldr)
        #print "dest", dest
        
        origin = os.path.join(srcfolder, file1)
        #print "origin", origin
        
        #path of hypothetical destination file of same name
        destfile = os.path.join(dest, file1)
        #print "destfile", destfile
        
        #if destination has file of same name        
        if os.path.exists(destfile):
            print "exists"
            if status == "replace":
                os.remove(destfile)
                move(origin, dest)
                print "moved ", file1
            #if status == "skip", don't move file
        else:
            print "doesn't exist"
            move(origin, dest)
            print "moved ", file1

