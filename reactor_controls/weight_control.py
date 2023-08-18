# Weight-controlled valve switches:

import time 
import threading
import serial
import serial.tools.list_ports as ports

from reactor_controls import instrument_controls as ic

#----------------------------------------------------------------------------------------------------------------
# Abiltiy to open/close valves:
def setvalve(ser, pinid, cmd):  # modify for valve opening and closing - 
    ser.write(atob(pinid + ','+ cmd + '\x0D')) 
    return #valveset
#----------------------------------------------------------------------------------------------------------------
# Open/close valves based on weight readings:
def weight_control(portIDV = '/dev/cu.usbmodem2101',portIDW = '/dev/cu.usbmodem2101',runtime=60,checktime=10,wgtlim=25):
    #serial port setup for valves
    serV = serial.Serial(portIDV) 
    serV.baudrate = 9600; serV.timeout = 0.1

    #serial port setup for scale
    serW = serial.Serial(portIDW) 
    serW.baudrate = 9600; serW.timeout = 0.1

    # set initials
    wini=ic.getweight(serW) 
    tini=time.time()
    tstp=time.time()
    ii = 10 # initial pin ID
    jj = 2 # sign
    cmd = True

    print('--> 10 = infuse; 12 = withdraw \n--> starting: port %s : %s and port %s : %s' %(ii,int(cmd),ii+2,int(cmd)))
    setvalve(serV, str(ii), str(int(cmd)))
    setvalve(serV, str(ii+2), str(int(not cmd)))
    # loop pumping over a given time
    while (time.time()-tini)<=runtime: # set run time
        if (time.time()-tstp)>=checktime: # checks weight
            wnow = ic.getweight(serW)
            print('Weight = ', wnow,'; Time =', time.time()-tini,'s')
            if abs(wini-wnow)>=wgtlim: # switches direction after meeting 25g change
                # close the open valve:
                cmd = not cmd
                setvalve(serV, str(ii), str(int(cmd)))
                print('--> set port %s to %s'%(ii,cmd))
                # switch to other valve and open:
                ii+=jj
                cmd = not cmd
                setvalve(serV, str(ii), str(int(cmd)))
                print('--> set port %s to %s'%(ii,cmd))
                jj*=-1
            tstp=time.time()

    # close both when finished
    setvalve(serV, '10', '0')
    setvalve(serV, '12', '0')
    print('Finished at', time.time()-tini,'s')
