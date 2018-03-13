import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import csv
from astropy.io import fits
import os.path
from pathlib import Path

'''
Open DR14_Stats_Catalog.csv. Over all visits for a star we will need to:
1. Find the minimum R values: R 51, R 101, R151
2. Find the maximum x-range values
3. Find the minimum R ratios: R 151/R 101 and R 101/R 51
 '''

def matches(x,y,z):
    #x = apogeeID
    #y = parameter in question that you want to find the minimum value of over all visits for a given apogee ID
    match_param_array = []
    match_apogeeid = []
    match_locationid = []
    uniqueID = np.unique(y)
    for i in range(len(uniqueID)):
        newID = np.where(y == uniqueID[i])
        new_array = newID[0]
        new_param_array = x[new_array]
        new_apo = y[new_array]
        small_val = min(new_param_array)
        loc_small_val = np.where(new_param_array == small_val)
        small_loc = loc_small_val[0][0]
        small_param = round(small_val,4)
        #array for small parameters
        match_param_array.append(small_param)
        #array for matching apogee ids and location ids
        match_apogeeid.append(y[small_loc])
        match_locationid.append(z[small_loc])
    return match_locationid,match_apogeeid,match_param_array
    


'''
def matches(xx,y,r51,r101,r151,xr,R1,R2,peak_val):
   # Generate empty lists to hold values of matched APOGEE IDs
    match51 = []
    match101 = []
    match151 = []
    matchxr = []
    matchR1 = []
    matchR2 = []
    matchlocid = []
    matchapoid = []
    matchpeak = []
    #Command for finding unique values (in this case, APOGEE IDs)
    uniqueID = np.unique(y)
    for i in range(len(uniqueID[0:5])):
        newID = np.where(y == uniqueID[i])
        newer = newID[0]
        small = r51[newer] 
        y2 = y[newer]
        x2 = xx[newer]
        peak = peak_val[newer]
        # Take smallest R 51 value of the list found above
        little = min(small)
        loc_of_small = np.where(small == little)
        small_loc = loc_of_small[0][0]
        x = round(little,4)
        match51.append(x)
        matchapoid.append(y2[small_loc])
        matchlocid.append(x2[small_loc])
        matchpeak.append(peak[small_loc])
    # Process above is repeated for other empty lists
    for j in range(len(uniqueID)):
        new = np.where(y == uniqueID[j])
        element = new[0]
        R101 = r101[element]
        lil = min(R101)
        x2 = round(lil,4)
        match101.append(x2)

    for k in range(len(uniqueID)):
        New = np.where(y == uniqueID[k])
        part = New[0]
        R151 = r151[part]
        bit = min(R151)
        x3 = round(bit,4)
        match151.append(x3)

    for p in range(len(uniqueID)):
        mew = np.where(y == uniqueID[p])
        elmnt = mew[0]
        XR = xr[elmnt]
        bit2 = max(XR)
        x4 = round(bit2,4)
        matchxr.append(x4)

    for o in range(len(uniqueID)):
        nID = np.where(y == uniqueID[o])
        news = nID[0]
        s = R1[news]
        l = min(s)
        x5 = round(l,4)
        matchR1.append(x5)

    for q in range(len(uniqueID)):
        mID = np.where(y == uniqueID[q])
        ns = mID[0]
        pico = R2[ns]
        tiny = min(pico)
        x6 = round(tiny,4)
        matchR2.append(x6)
    return match51, match101, match151, matchxr,matchR1,matchR2, matchlocid,matchapoid,matchpeak'''

## Read in DR14 catalog generated by APOGEE_ID.py
filepath2 = 'DR14StatsCatalog.csv'
data_dr14 = pd.read_csv(filepath2)
locationid = data_dr14['LocationID']
apogeeid = data_dr14['ApogeeID']
visits = np.asarray(data_dr14['Visit'])
snr = np.asarray(data_dr14['SNR'])
R51 = np.asarray(data_dr14['log(R51)'])
R101 = np.asarray(data_dr14['log(R101)'])
R151 = np.asarray(data_dr14['log(R151)'])
xranges = np.asarray(data_dr14['log(xr)'])
ratio1 = np.asarray(data_dr14['log(Ratio1)'])
ratio2 = np.asarray(data_dr14['log(Ratio2)'])
peak_value = np.asarray(data_dr14['Peak_value'])

#Send parameters to function "matches"
dr14 = matches(R51,apogeeid,locationid)
dr14_locationid = dr14[0]
dr14_apogeeid = dr14[1]
dr14_R51 = dr14[2]
r101 = matches(R101,apogeeid,locationid)
dr14_R101= r101[2]
r151 = matches(R151,apogeeid,locationid)
dr14_R151 = r151[2]
xr = matches(xranges,apogeeid,locationid)
dr14_xr = xr[2]
ratio_1 = matches(ratio1,apogeeid,locationid)
dr14_R1 = ratio_1[2]
ratio_2 = matches(ratio2,apogeeid,locationid)
dr14_R2 = ratio_2[2]
peaks = matches(peak_value,apogeeid,locationid)
dr14_peakval = peaks[2]

#Construct a .csv file to hold smallest R, R ratios, and max x-ranges
cols = ['LocationID', 'ApogeeID']
df = pd.DataFrame(columns = cols)
df['LocationID'] = dr14_locationid
df['ApogeeID'] = dr14_apogeeid
#add HJD info to output table
df['log(R51)'] = dr14_R51
df['log(R101)'] = dr14_R101
df['log(R151)'] = dr14_R151
df['log(xr)'] = dr14_xr
df['log(Ratio1)'] = dr14_R1
df['log(Ratio2)'] = dr14_R2
df['Peak_value'] = dr14_peakval
df.to_csv('DR14_SmallR_LargeXR.csv')

'''
#Read in the file that contains the smallest R, R ratios, and the largest max x-range. (called DR14_SmallR_LargeXR.csv )
filename = 'DR14_SmallR_LargeXR.csv'
data = pd.read_csv(filename)
dr14_locationid = np.asarray(data['LocationID'])
dr14_apogeeid = np.asarray(data['ApogeeID'])
dr14_r51 = np.asarray(data['log(R51)'])
dr14_r101 = np.asarray(data['log(R101)'])
dr14_r151 = np.asarray(data['log(R151)'])
dr14_ratio1 = np.asarray(data['log(Ratio1)'])
dr14_ratio2 = np.asarray(data['log(Ratio2)'])
dr14_xr = np.asarray(data['log(xr)'])
dr14_peak_value = np.asarray(data['Peak_value'])

#Read in the training set binaries 
filepath = 'TrainingSet_Binaries.csv'
openfile = pd.read_csv(filepath)
bin_locID = openfile['LocationID']
bin_apoID = openfile['ApogeeID']
bin_R51 = np.asarray(openfile['log(R51)'])
bin_R101 = np.asarray(openfile['log(R101)'])
bin_R151 = np.asarray(openfile['log(R151)'])
bin_XRange = np.asarray(openfile['log(xr)'])
bin_Ratio1 = np.asarray(openfile['log(Ratio1)'])
bin_Ratio2 = np.asarray(openfile['log(Ratio2)'])
bin_snr = np.asarray(openfile['SNR'])
bin_visit = np.asarray(openfile['Visit'])
bin_peakval = np.asarray(openfile['Peak_value'])

#Send these through the 'matches' function to retrieve the smallest R, R ratios, and maximum x-range
#Send parameters to function "matches"
tsb = matches(R51,apogeeid,locationid)
tsb_locationid = tsb[0]
tsb_apogeeid = tsb[1]
tsb_R51 = tsb[2]
tsbr101 = matches(bin_R101,bin_apoID,bin_locID)
tsb_R101= tsbr101[2]
tsbr151 = matches(bin_R151,bin_apoID,bin_locID)
tsb_R151 = tsbr151[2]
tsbxr = matches(bin_XRange,bin_apoID,bin_locID)
tsb_xr = tsbxr[2]
ratio_1 = matches(bin_Ratio1,bin_apoID,bin_locID)
tsb_R1 = tsbratio_1[2]
tsbratio_2 = matches(bin_Ratio2,bin_apoID,bin_locID)
tsb_R2 = tsbratio_2[2]
tsbpeaks = matches(bin_peakval,bin_apoID,bin_locID)
tsb_peakval = tsbpeaks[2]


#Generate histograms to find the number of most densely populated region
# XR vs R101
plt.figure(figsize=(8,8))
plt.hist2d(dr14_xr,dr14_R101,bins=(50,50), norm=colors.LogNorm(),cmap=plt.cm.BuPu)
plt.colorbar()
plt.scatter(tsb_xr,tsb_R101,s=8,marker='^',facecolor='None',edgecolor='black',label='Training Set Binaries')
plt.xlabel('max log(x-range)',fontsize=15)
plt.ylabel('min log($R_{101}$)',fontsize=15)
plt.legend(loc='upper left')
#plt.xlim(-1,0.2)
#plt.ylim(0,1.6)
plt.savefig('hist2d(XR_vs_R101).pdf',dpi=800)
plt.show()'''
