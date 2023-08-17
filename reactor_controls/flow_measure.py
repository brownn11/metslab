# Reads output of mass spectrometer instrument:
import numpy as np
import serial
import glob 
import time
import datetime
from time import strftime, localtime
import scipy.constants as constants 
import pandas as pd
import os

import instrument_controls as ic
#----------------------------------------------------------------------------------------------------------------
# Basic compound properties (viscosity in gaseous phase at 25C [micropoise]):
comp = {'H2' : {'v' : 89.153, 'm' : 2.016},
       'CO2' : {'v' : 149.332, 'm' : 44.009},
       'CO' : {'v' : 176.473, 'm' : 28.0101},
       'CH4' : {'v' : 111.852, 'm' : 16.04},
       'H2O' : {'v' : 130, 'm' : 18.0153},
       'N2' : {'v' : 178.12, 'm' : 14.007},
       'O2' : {'v' : 204.591, 'm' : 15.999},
       'Ar' : {'v' : 225.593, 'm' : 39.948}}
#----------------------------------------------------------------------------------------------------------------
# Returns the composition of gas from the mass spectrometer (focused on CH4, H2, CO2, and CO):
def read_ms(path):
    ms_dat = pd.read_csv(r'%s'%path, skiprows=28) # opens up a Hiden Analytical mass spectrometry .csv data file:
    CH4 = ms_dat.iloc[len(ms_dat)-1,10]/100
    H2 = ms_dat.iloc[len(ms_dat)-1,11]/100
    CO2 = ms_dat.iloc[len(ms_dat)-1,12]/100
    CO = ms_dat.iloc[len(ms_dat)-1,13]/100

    return [CH4,H2,CO2,CO] # [ccm]
#----------------------------------------------------------------------------------------------------------------
# Calculate the viscosity of a mixture of similar weight gases:
def v_mix(aa,xs):
    vs,ms=[],[]
    for ii in aa:
        vs.append(comp[ii]['v'])
        ms.append(comp[ii]['m'])
    vs=np.array(vs)
    xs=np.array(xs)
    ms=np.array(ms)
    mix = np.sum(vs*xs*np.sqrt(ms))/np.sum(xs*np.sqrt(ms))
    return mix
#----------------------------------------------------------------------------------------------------------------
# Calculate real flow rate, adjust for temperature:
def flow_correction(Q_meas,aa,xs,visc_sel=184.918,T=298.15):
    # Q_meas = measured flow rate via MFC
    # aa = list of compound names
    # xs = list of compound compositions
    # visc_sel = selected viscosity of air
    # T=25C stp
    visc_act = v_mix(aa,xs)
    if T!=298.15:
        visc_sel *= np.sqrt(T/298.15)
        visc_act *= np.sqrt(T/298.15)
    Q = Q_meas*(visc_sel/visc_act)
    return Q  # units of input flow rate
#----------------------------------------------------------------------------------------------------------------
# Calculate real output of CH4 based on most recent MS file output:
def flow_real(ser):
    flow_meas = float(ic.mfcread(ser, 'F')[18:25]) # tentatively should work 
    
    # get current time in file name format to find the most recent MS export
    dt = strftime("%m-%d-%Y", localtime())[1:] # [1:] gets rid of the 0 before the month for singular digit months (i.e. '07' for July)
    tm = strftime(" %H-%M-%S %p", localtime())
    
    path_now = r'C:\Users\MetsLab\Documents\Hiden Analytical\QGA 2.0\Reports & Exports\composition_calc ' + dt + tm +'.csv'
    path_glob = glob.glob(r'C:\Users\MetsLab\Documents\Hiden Analytical\QGA 2.0\Reports & Exports\composition_calc ' + dt + '*.csv')
    # **note: the MS export must be from the current day**
    
    # find the MS export with the smallest difference in export time to now
    t_diff=np.zeros(len(path_glob))
    for ii in range(len(path_glob)):
        if path_now[106:108] == path_glob[ii][106:108]: # check if in AM or PM
            dec_now = '%s%s'%(float(path_now[100:102])/60,str(float(path_now[103:105])/60)[2:])
            dec_glob = '%s%s'%(float(path_glob[ii][100:102])/60,str(float(path_glob[ii][103:105])/60)[2:])
            t_now = float(path_now[97:99]) + float(dec_now)
            t_glob = float(path_glob[ii][97:99]) + float(dec_glob)
            t_diff[ii] = t_now-t_glob
        else: 
            hr_now = float(path_now[97:99])+12
            dec_now = '%s%s'%(float(path_now[100:102])/60,str(float(path_now[103:105])/60)[2:])
            dec_glob = '%s%s'%(float(path_glob[ii][100:102])/60,str(float(path_glob[ii][103:105])/60)[2:])
            t_now = hr_now + float(dec_now)
            t_glob = float(path_glob[ii][97:99]) + float(dec_glob)
            t_diff[ii] = t_now-t_glob
    path = path_glob[np.argmin(t_diff)]
    
    # get concentration percentiles and calculate real flow
    xs = rm.read_ms(path)
    flow = flow_correction(flow_meas,['CH4','H2','CO2','CO'],xs)
    
    print('Output:',flow*xs[0],'ccm of CH4 as of %s'%path[87:108])
    return flow*xs[0]
#----------------------------------------------------------------------------------------------------------------
