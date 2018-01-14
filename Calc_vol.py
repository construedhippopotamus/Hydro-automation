# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 05:52:56 2018

@author: Jenny

Calculate hydromodification volume for subarea data using San Bernardino Water Quality Manual equations and python pandas.

1. pivot table for each lot
2. look up CN from LU and soil
3. area weighted CN for each lot
4. eqns

order rows: 1. type 2. subarea

https://swcarpentry.github.io/python-novice-gapminder/08-data-frames/

"""
import os
import csv
import pandas
import numpy as np

#subarea data
data = "C:\Users\Pizzagirl\Documents\programming\python\B_data.csv"

df = pandas.read_csv(data, index_col=0)

#NEED to specificy agg function, or it will default to avg or something else undesirable!!!
pivot = pandas.pivot_table(df, index = ["Type", "SOIL", "LAND USE"], aggfunc=np.sum)

#need "to_records" to keep format and index
df2 = pandas.DataFrame(pivot.to_records())

#dictionary for LU lookup table
lookup = {
    "LU": ["Desert Brush Poor (20%)", "Desert Brush Fair (40%)", "Commercial", "Public Park"],
    "A" : [67, 64, 95, 17],
    "B" : [67, 64, 95, 36],
    "C" : [75, 72, 95, 50],
    "D" : [-1, -1, -1, -1]
        }

CNtable = pandas.DataFrame( data = lookup )
CNtable.set_index(['LU'], inplace=True)

CNlist = []
for index, row in df2.iterrows():
    LU1 = row['LAND USE']
    soil = row['SOIL']
    
    CN = CNtable.loc[LU1][soil]
    #assigning data to CN column from list didn't work
    CNlist.append(CN)
    
df2['CN'] = CNlist
df2['CN*A'] = df2['CN']*df2['AREA']
              
#print df2
#get sum of areas and CNavg for each lot
pivot2 = pandas.pivot_table(df2, index = ["Type"], aggfunc=np.sum)

df3 = pandas.DataFrame(pivot2.to_records())

df3['CNavg'] = df3['CN*A']/df3['AREA']
df3.set_index(['Type'], inplace=True)

print df3

#Equations
df3['S'] = 1000/df3['CNavg'] - 10
df3['Ia'] = 0.2* df3['S']



#precip values
P2 = 1.09
P10 = 1.24

#2yr volume
df3['V2'] = df3['AREA']/12 *((P2 - df3['Ia'])**2) / (P2 - df3['Ia']+df3['S']) 
df3['V10'] = df3['AREA']/12 *((P10 - df3['Ia'])**2) / (P10 - df3['Ia']+df3['S'])

print df3

#Export to excel
writer = pandas.ExcelWriter('C:\Users\Pizzagirl\Documents\programming\python\processed.xlsx')
df3.to_excel(writer,'Sheet1')

print "done"
"""
NOTES

#check - "type" should be index
#print df.index

#to print individual columns, do df.columnname
#print df.Ap

#to print an attribute of a piece of data. "B-1" retrieves all data for B-1,
# "land use" is optional and returns just landuse.
#print df.loc["road"]
#print df.loc["road", "LAND USE"]

"""





