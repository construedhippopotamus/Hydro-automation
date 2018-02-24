#Calculate partial duration analysis for San Diego hydromod

# San Diego HMP Manual Ch 6, pg 6-25

# must have 24-hr dry between events
# dry = no rain greater than 0.01 cfs  --> check this against SDHM - cutoff appears to be somewhat arbitrary.
# return a dataset with peak Qs for each event, and the number of peaks.

# ASSUMPTIONS: Q data is continuous, hourly data with no gaps.
# input data format:

from datetime import datetime
import os
import csv

path = r'C:\Users\Pizzagirl\Documents\programming\python\hydro_work'
indata = 'short.csv'
low = 0.01
sep = 24  #24hr between events

time = []
Q = []
Qpart = []
dry = 24  #number of dry hours - start at 24 to catch first event, which can occur at hr = 0
peak = 0
peaklist = []

os.chdir(path)

with open(indata, 'r') as f:
    csvreader = csv.reader(f, delimiter = ',')
    for row in csvreader:
        try:
            time.append(row[2][-5:])
            Q.append(float(row[3]))
        except ValueError:
            #print("can't convert to float:", row)
            pass

series = list(zip(time, Q))  #just need Qs if data is hourly, but leave for now.
#print (series)


for event in series:
    if event[1] < low:
        dry+= 1   #Count dry hour
    if event[1] > low:
        #print("dry", dry)
        if dry >= 24:  #new event
            peaklist.append(peak)  # append peak from last event
        else:   #same event because less than 24 dry hours have passed
            if event[1] > peak:
                peak = event[1]
        dry = 0  #reset dry hours


peaklist.append(peak)  #peak from last event
del(peaklist[0])

print(peaklist)


