#Determines whether proposed condition is in compliance with hydromod by comparing to existing condition.

#Calculate partial duration analysis for San Diego hydromod

# San Diego HMP Manual Ch 6, pg 6-25

# must have 24-hr dry between events
# dry = no rain greater than 0.01 cfs  --> check this against SDHM - cutoff appears to be somewhat arbitrary.
# return a dataset with peak Qs for each event, and the number of peaks.

# ASSUMPTIONS: Q data is continuous, hourly data with no gaps.

import os
import csv
import openpyxl
from openpyxl import Workbook
from Flow_freq import Qprocess   #does flow frequency analysis

path = r'H:\pdata\160817\Calcs\Strmwater\Water Quality\EPA SWMM 5\Original Tory Walker models'

#Existing condition Q out file from EPA SWMM 5
EXdata = 'PRE_DEV_POC-1_QOUT.TXT'

#Proposed condition Q out file from EPA SWMM 5
PRdata = 'POST_DEV_POC-1_QOUT.TXT'


#generate existing flow values in 0.1*Q2 - Q10 to compare to:
EXoutputs = Qprocess(path,EXdata)
EXQcompare = EXoutputs[0]    #comparison bins
EXQ =  EXoutputs[1]

#get list of proposed condition peaks
PRoutputs = Qprocess(path,PRdata)
#PRQcompare = PRoutputs[0]    #not needed for hydromod compliance determination
PRQ = PRoutputs[1]

#2. count number of hours in the flow record that Q exceeds each of the 100 Qs. Do for existing Qs in this script --> sort and then find first exceedance; subtract.

#for each "bin" in existing condition Qcompare, count number of existing and number of proposed that exceed.
EXcomply = []
PRcomply = []
Qfractionlist = []

for Qbin in EXQcompare:
    EXcount = 0
    PRcount = 0

    for qqex in EXQ:
        if qqex > Qbin:
            EXcount +=1
    for qqpr in PRQ:
        if qqpr > Qbin:
            PRcount +=1
    PRcomply.append(PRcount)
    EXcomply.append(EXcount)

    Qfraction = PRcount/EXcount
    Qfractionlist.append(Qfraction)

    if Qfraction > 1.1:
        print "FAIL: PR/EX:", Qfraction


print(Qfractionlist)


#later: sort to make faster, do plot of results





