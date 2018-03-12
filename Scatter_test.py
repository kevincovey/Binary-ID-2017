import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import corner
from matplotlib import colors
#from matplotlib.ticker import PercentFormatter


def snr_rec(snr,locationID,apogeeID,R51,R101,R151,Ratio1,Ratio2,xranges,visit):
    # Create new lists to be turned into arrays if they pass the SNR > 10 resuirement
    snr = snr
    locationid = []
    apogeeid = []
    r51 = []
    r101 = []
    r151 = []
    R1 = []
    R2 = []
    vis = []
    xr = []

    # Create new lists to only hold objects if they pass the SNR > 10 resuirement
    for i in range(len(locationID)):
        if snr[i] > 10:
            locationid.append(locationID[i])
            apogeeid.append(apogeeID[i])
            r51.append(R51[i])
            r101.append(R101[i])
            r151.append(R151[i])
            R1.append(ratio1[i])
            R2.append(ratio2[i])
            vis.append(visit[i])
            xr.append(xranges[i])

    LocID = np.array(locationid)
    ApoID = np.array(apogeeid)
    R_51 = np.array(r51)
    R_101 = np.array(r101)
    R_151 = np.array(r151)
    ratio_1 = np.array(R1)
    ratio_2 = np.array(R2)
    x_ranges = np.array(xr)
    return LocID, ApoID, R_51, R_101, R_151, x_ranges, ratio_1, ratio_2,vis

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
## Read in list of IDL identified training set binaries
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

''' 
Apply the first cut: visits of a star must have SNR > 10
'''
kcBins = snr_rec(bin_snr,bin_locID,bin_apoID,bin_R51,bin_R101,bin_R151,bin_XRange,bin_Ratio1,bin_Ratio2,bin_visit)
kcapoid = kcBins[0]
kclocid = kcBins[1]
kcR51 = kcBins[2]
kcR101 = kcBins[3]
kcR151 = kcBins[4]
kcXR = kcBins[5]
kcR1 = kcBins[6]
kcR2 = kcBins[7]

dr14 = snr_rec(snr,apogeeid,locationid,R51,R101,R151,xranges,ratio1,ratio2,visits)
dr14apoid = dr14[0]
dr14locid = dr14[1]
dr14R51 = dr14[2]
dr14R101 = dr14[3]
dr14R151 = dr14[4]
dr14XR = dr14[5]
dr14R1 = dr14[6]
dr14R2 = dr14[7]
dr14vis = dr14[8]

#Generate .csv file that holds a star's smallest R, R ratios, and the maximum x-ranges. 
# In addition, report the visit that held all this information
'''cols = ['LocationID', 'ApogeeID']
df = pd.DataFrame(columns = cols)
df['LocationID'] = dr14locid
df['ApogeeID'] = dr14apoid
df['Visit'] = dr14vis

#add HJD info to output table
df['log(R51)'] = dr14R51
df['log(R101)'] = dr14R101
df['log(R151)'] = dr14R151
df['log(xr)'] = dr14XR
df['log(Ratio1)'] = dr14R1
df['log(Ratio2)'] = dr14R2
df.to_csv('DR14SmallR_LargeXR.csv')'''

#This was used to generate the scatter plots that were too large to open in an email
def scatter_plots(x,y):
    ## Generate Scatter plots for the DR14 population with the IDL training set binaries we had identified overlapped.
    # Make plot for x-range vs  R101/R51 (R2)
    plt.scatter(dr14XR, dr14R2, s=6, label='DR14')
    plt.scatter(kcXR, kcR2,s=6,marker='^', label = 'Training Set Binaries')
    plt.ylabel('log(R101/R51)')
    plt.xlabel('log(x-range)')
    plt.legend(loc='lower right')
    plt.savefig('DR14vsTSB_XRvsR2.pdf')
    #plt.show()


    #Make plot for R51 vs R101/R51 (R2)
    plt.scatter(dr14R51, dr14R2, s=6, label='DR14')
    plt.scatter(kcR51, kcR2,s=6,marker='^', label = 'Training Set Binaries',color='orange')
    plt.ylabel('log(R101/R51)')
    plt.xlabel('log(R51)')
    plt.legend(loc='lower right')
    plt.savefig('DR14vsTSB_R51vsR2.pdf')
    #plt.show()


    #Make plot for R101 vs R151/R101 (R1)
    plt.scatter(dr14R101, dr14R1, s=6, label='DR14')
    plt.scatter(kcR101, kcR1,s = 6, marker='^', label = 'Training Set Binaries')
    plt.ylabel('log(R151/R101)')
    plt.xlabel('log(R101)')
    plt.legend(loc='lower right')
    plt.savefig('DR14vsTSB_R101vsR1.pdf',dpi=700)
    #plt.show()

    #Make plot for x-ranges vs R151/R101 (R1)
    plt.scatter(dr14XR, dr14R1, s=6, label='DR14')
    plt.scatter(kcXR, kcR1,s=6,marker='^', label = 'Training Set Binaries')
    plt.ylabel('log(R151/R101)')
    plt.xlabel('log(x-ranges')
    plt.legend(loc='lower right')
    plt.savefig('DR14vsTSB_XRvsR1.pdf',dpi=700)
    #plt.show()

    #Make plot for R151 vs R51
    plt.scatter(dr14R151, dr14R51, s=6, label='DR14')
    plt.scatter(kcR151, kcR51,s=6, marker='^', label = 'Training Set Binaries')
    plt.ylabel('log(R51)')
    plt.xlabel('log(R151)')
    plt.legend(loc='lower right')
    plt.savefig('DR14vsTSB_R151vsR51.pdf',dpi=700)
    #plt.show()
    return 

# Make 2D histograms and overlay scatter plot training set binaries on the histogram
plt.figure(figsize=(8,8))
#Overplot the training set binaries by scatter plot
plt.scatter(dr14XR,dr14R2,s=6,marker='^',label='DR14 Stars')
#Corner is the package that generates the 2D histogram
corner.hist2d(kcXR,kcR2,bins=150,plot_contours=True,fill_contours=True,smooth=1.2,plot_datapoints=True)
plt.xlabel('max log(x-range)',fontsize=15)
plt.ylabel('min log($R_{101}/R_{51}$)',fontsize=15)
plt.legend(loc='lower right')
plt.ylim(-1,0.2)
plt.xlim(-1,0.2)
plt.savefig('dr14vsTSB(XR_vs_R2).pdf',dpi=800,bbox='tight')
plt.show()


'''#Generate histograms to find the number of most densely populated region
# XR vs R101
plt.figure(figsize=(8,8))
plt.hist2d(dr14XR,dr14R101,bins=(50,50), norm=colors.LogNorm(),cmap=plt.cm.BuPu)
plt.colorbar()
plt.scatter(kcXR,kcR101,s=8,marker='^',facecolor='None',edgecolor='black',label='Training Set Binaries')
plt.xlabel('max log(x-range)',fontsize=15)
plt.ylabel('min log($R_{101}$)',fontsize=15)
plt.legend(loc='upper left')
#plt.xlim(-1,0.2)
#plt.ylim(0,1.6)
plt.savefig('Hist2d(XR_vs_R101).pdf',dpi=800)
plt.show()'''