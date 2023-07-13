import numpy as np
import scipy.constants as constants 

# write compound properties (viscosity in gaseous phase at 25C [micropoise]):
comp = {'H2' : {'v' : 89.153, 'm' : 2.016},
       'CO2' : {'v' : 149.332, 'm' : 44.009},
       'CO' : {'v' : 176.473, 'm' : 28.0101},
       'CH4' : {'v' : 111.852, 'm' : 16.04},
       'H2O' : {'v' : 130, 'm' : 18.0153},
       'N2' : {'v' : 178.12, 'm' : 14.007},
       'O2' : {'v' : 204.591, 'm' : 15.999},
       'Ar' : {'v' : 225.593, 'm' : 39.948}}

# viscosity of a mixture of similar weight gases:
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

# calculate real flow rate, adjust for temperature:
def flow_real(Q_meas,aa,xs,visc_sel=184.918,T=298.15):
    # selected viscosity for air, T = 25C as standard 
    visc_act = v_mix(aa,xs)
    if T!=298.15:
        visc_sel *= np.sqrt(T/298.15)
        visc_act *= np.sqrt(T/298.15)
    Q = Q_meas*(visc_sel/visc_act)
    return Q  # units of input flow rate

