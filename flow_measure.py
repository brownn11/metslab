#!/usr/bin/env python
# coding: utf-8
import numpy as np
import serial
import glob 
import time
import datetime
from time import strftime, localtime

import flow_real as fr
import read_ms as rm
import instrument_controls as ic

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
    flow = fr.flow_real(flow_meas,['CH4','H2','CO2','CO'],xs)
    
    print('Output:',flow*xs[0],'ccm of CH4 as of %s'%path[87:108])
    return flow*xs[0]

