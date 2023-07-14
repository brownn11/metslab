import pandas as pd
import os

def read_ms(path):
    # Get composition of gas in the mass spectrometer: 
    ms_dat = pd.read_csv(r'%s'%path, skiprows=28) # opens up a Hiden Analytical mass spectrometry .csv data file:
    CH4 = ms_dat.iloc[len(ms_dat)-1,10]/100
    H2 = ms_dat.iloc[len(ms_dat)-1,11]/100
    CO2 = ms_dat.iloc[len(ms_dat)-1,12]/100
    CO = ms_dat.iloc[len(ms_dat)-1,13]/100

    return [CH4,H2,CO2,CO] # [ccm]