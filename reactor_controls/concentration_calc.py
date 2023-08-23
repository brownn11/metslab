# Code to calculate the amount of concentration to be replaced during experiments, based off of weight fluctuations. 
from reactor_controls import instrument_controls as ic

#----------------------------------------------------------------------------------------------------------------
def concentration_calc(Vm,Cn,        # Must define measured metabolic water accumualted and relative concentration. 
                       C1n=0,C2n=0,  # Define for multiple concentrations if needed.
                       Vo=600,Co=1): # Initial volume of the culture and concentration of the nutrients.
    if C1n == 0:
        Vn = Vm/((Cn/Co)*(Vo+Vm)/Vo-1)
        Vr = Vn + Vm
        res = [Vr,Vn]
    else:
        Vn = Vm/((Cn/Co)*(Vo+Vm)/Vo-1)
        Vr = Vn + Vm
        
        V1n = Vn/(1+C1n/C2n)
        V2n = Vn/(1+C2n/C1n)
        
        res = [Vr,Vn,V1n,V2n]
        
    # Results are returned as Vr followed by Vn, and then V1n and V2n if applicable 
    
    return res
#----------------------------------------------------------------------------------------------------------------
# Specifically for 25 and 200X concentrations
def x_25_200(serW,w_ini):

    # Set up some sort of time control here, so that the weight is only checked in-between pumps

    w = ic.getweight(serW)

    if w > w_ini:
        Vm = (w-w_ini)/0.98319 # [cm3]; uses density of water at 60C
        res2 = cc(Vm=Vm, Cn=20, C1n=25, C2n=200)
        print('Vm  =', Vm, 'cm3\nVr  =', res2[0], 'cm3\nVn  =', res2[1], 'cm3\nV1n =', res2[2], 'cm3\nV2n =', res2[3],'cm3')
        pack = [Vm, res2[0], res2[1], res2[2], res2[3]]
    else:
        print('Pass')
        pack = 0
    return pack
#----------------------------------------------------------------------------------------------------------------
