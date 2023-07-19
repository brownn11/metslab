# Weight-controlled valve switches

import time 
import threading
import serial
import serial.tools.list_ports as ports

# Basic definitions:
def print_ports():
    com_ports = list(ports.comports())  # create a list of com ['COM1','COM2']
    for i in com_ports:
        print(i.device)  # returns 'COMx'
def btoa(bstr): #returns an ascii string from a bytes object
    btoadat = bstr.decode('ascii')
    return btoadat
def atob(strb): #returns a bytes object from an ascii string
    atobdat = strb.encode('ascii')
    return atobdat

# Specialized definitions:
def getweight(ser): # interacts with the Ohaus balance
    ser.open()
    ser.write(b'P\r\n')
    weight=float(btoa(ser2.read_until(b'\r\n',100)).split()[0]) #print time, too
    ser.close()
    return weight

def setvalve(ser, pinid, cmd):  # modify for valve opening and closing - 
    ser.write(atob(pinid + ','+ cmd + '\x0D')) 
    return #valveset

def weight_control(portIDV = '/dev/cu.usbmodem2101',portIDW = '/dev/cu.usbmodem2101',runtime=60,checktime=10,wgtlim=25):
    #serial port setup for valves
    serV = serial.Serial(portIDV) 
    serV.baudrate = 9600; serV.timeout = 0.1

    #serial port setup for scale
    serW = serial.Serial(portIDW) 
    serW.baudrate = 9600; serW.timeout = 0.1

    # set initials
    wini=getweight(serW) 
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
            print('Weight = ', wnow,'; Time =', time.time()-tini,'s')
            if abs(wini-getweight(serW))>=wgtlim: # switches direction after meeting 25g change
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