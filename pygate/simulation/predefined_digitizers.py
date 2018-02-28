from ..components.digitizer import *
from .predefined_cameras import *

def ecat_digitizer(cam):
    ad = Adder()
    rdr = Readout(depth=1)
    blur = Blurring(resolution= 0.26, eor = 511.0)
    thres = ThresHolder(value= 250.0)
    uph = UpHolder(value = 750.0)
    ddt = DeadTime(volume = cam.block,t = 3000.0,mode='paralysable')
    singles = Singles([ad,rdr,blur,thres,uph,ddt])
    
    coin = CoincidenceSorter(window=10,offset=0)
    coin_delay = CoincidenceSorter(window=10,offset=500)

    coin_chain = CoincidencesChain(input1 = coin, input2 = coin_delay,name = 'finalCoinc',use_priority='True')
    digitizer = [singles,coin,coin_delay,coin_chain]
    return digitizer
        
def cylindricalPET_digitizer():
    ad = Adder()
    rdr = Readout(depth=1)
    blur = Blurring(resolution= 0.26, eor = 511.0)
    thres = ThresHolder(value= 250.0)
    uph = UpHolder(value = 650.0)
    singles = Singles([ad, rdr, blur, thres, uph])
    coin = CoincidenceSorter(window= 10)
    coin_delay = CoincidenceSorter(name='delay',window=10,offset=500)
    digitizer = [singles,coin,coin_delay]
    return digitizer

def optical_digitizer():
    ad_op = AdderOptical()
    rdr = Readout(depth=1)
    singles = Singles(ad_op,rdr)
    digitizer = [singles]
    return digitizer

def spect_digitizer():
    pass
