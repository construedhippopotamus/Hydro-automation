#Calculate partial duration analysis for San Diego hydromod

# San Diego HMP Manual Ch 6, pg 6-25

# must have 24-hr dry between events
# dry = no rain greater than 0.01 cfs  --> check this against SDHM - cutoff appears to be somewhat arbitrary.
# return a dataset with peak Qs for each event, and the number of peaks.

# ASSUMPTIONS: Q data is continuous, hourly data with no gaps.


# NOTE: Tory Walkers did this differently from the manual - they got the peak within a 25hr period.

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

#HMP manual way of determining series:

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

print("HMP peak:", peaklist)


#Tory walkers way of determining peaks:
def TWmethod(series):
    peakTW = 0
    peaklistTW = []
    ii = 0

    for ii in range(0, len(series)):
        #print (series[ii][1])
        if series[ii][1] > peakTW:
            peakTW = series[ii][1]
            #print("test peak:", peakTW)

            #check if next 12 values are decreasing:
            if series[ii + 1][1] < series[ii][1]:
                max1 = max([zz[1] for zz in series[1+ii : 12+ii]])
                if max1 < peakTW:
                    peaklistTW.append(peakTW)
        ii += 1

    print ("Tory Walker Peaks", peaklistTW)

    return(peaklistTW)


#Calculate flow frequencies for San Diego hydromod

# San Diego HMP Manual Ch 6, pg 6-25

#1. sort values large to small
#2. Flow frequency with Cunnane Eqn: Probability = P = (i-0.4)/(n+0.2)
#   i = Position of the peak whose probability is desired
#   n = number of years analyzed = 1-10 = 10

# ASSUMPTIONS: number of peaks analyzed MUST be less than or equal to n.

#sort Q list

def break1(list, sorted):
    num = len(list)
    mid = int(num/2)

    #print("list", list, "len", num, "mid", mid)
    if mid >=1:
        left = list[:mid]
        right = list[mid:]
        #print("L", left, "R", right)

        break1(left, sorted)
        break1(right, sorted)

    else:
       return sort1(list, sorted)



#sort largest to smallest
def sort1(list, sorted):

    if list[0] >= sorted[0]:
        sorted.insert(0, list[0])

    if list[0] < sorted[0]:
        sorted.append(list[0])

    return sorted

#initialize and call:
sorted = [0]
#list = [1,2,3,4,5,6,7,8,9,9, 9.2]
break1(peaklist, sorted)

#delete last element - it is a zero I had to add for comparison.
print("FINAL RESULT", sorted[:-1])


#Calculate flow frequencies for San Diego hydromod

# San Diego HMP Manual Ch 6, pg 6-25

#1. sort values large to small
#2. Flow frequency with Cunnane Eqn: Probability = P = (i-0.4)/(n+0.2)
#   i = Position of the peak whose probability is desired
#   n = number of years analyzed = 1-10 = 10

# ASSUMPTIONS: number of peaks analyzed MUST be less than or equal to n.

n = 10 #years
list = [10, 9, 8, 7,6,5,4,3,2,1]

for i in range(0, len(list)):
    P = ((i+1)-0.4) / (n+0.2)
    #print (P)



#NOTE:  The way this is currently set up, there will be more peaks than n, which doesn't work...
# not sure what to do.



