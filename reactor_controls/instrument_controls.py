# File of all basic instrument controls:
import time 
import threading
import serial
import serial.tools.list_ports as ports
# --------------------------------------------------------------------------------
# General serial definitions:
def portlist():
    com_ports = list(ports.comports())  
    for i in com_ports:
        print(i.device)  # returns available ports
    
def btoa(bstr): #returns an ascii string from a bytes object
    btoadat = bstr.decode('ascii')
    return btoadat

def atob(strb): #returns a bytes object from an ascii string
    atobdat = strb.encode('ascii')
    return atobdat
# --------------------------------------------------------------------------------
# Actual instrument controls:
def pumpread(ser, pumpid, cmd): # interacts with the pump
    t_ini=(time.time())
    ser.open()
    ser.write(atob(str(pumpid) + str(cmd) + '\x0D'))
    pumpdat = btoa(ser.read_until(b'\x03',100))
    ser.close()
    return pumpdat[1:-1]

def getweight(ser): # interacts with the Ohaus balance
    ser.open()
    ser.write(b'P\r\n')
    weight=float(btoa(ser.read_until(b'\r\n',100)).split()[0]) #print time, too
    ser.close()
    return weight

def mfcread(ser, mfcid): # returns data from mass flow controllers as ascii strings
    ser.open()
    #reads until \r character or nn bytes or timeout s, whichever comes first
    ser.write(atob(mfcid + '\x0D'))
    mfcreaddat = btoa(ser.read_until(b'\x0D',100))
    ser.close()
    return mfcreaddat

def setvalve(ser, pinid, cmd):  # interacts with solenoid valves for opening and closing using an Arduino computer
    # pinid = solenoid ID
    # cmd = True/False = Open/Close
    ser.write(atob(pinid + ','+ cmd + '\x0D')) 
    return #valveset

# servers will need to be defined in the following format:
    # ser = serial.Serial('/dev/cu.usbserial-10') # port name can be found using 'portlist'
    # ser.baudrate = 19200; serP.timeout=0.1
    # ser.close()
