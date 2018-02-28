from ..components.digitizer import *
from ..components.geometry import *


def ecat_digitizer(dtvolume,
                   rdr=None, blur=None,
                   thres=None, uph=None,
                   ddt=None, coin=None,
                   coin_delay=None,
                   coin_chain=None):
    ad = Adder()
    if rdr is None:
        rdr = Readout(depth=1)
    if blur is None:
        blur = Blurring(resolution=0.26, eor=511.0)
    if thres is None:
        thres = ThresHolder(value=250.0)
    if uph is None:
        uph = UpHolder(value=750.0)
    if ddt is None:
        ddt = DeadTime(volume=dtvolume, t=3000.0, mode='paralysable')
    singles = Singles([ad, rdr, blur, thres, uph, ddt])
    if coin is None:
        coin = CoincidenceSorter(window=10, offset=0)
    if coin_delay is None:
        coin_delay = CoincidenceSorter(name='delay', window=10, offset=500, is_define_name=True, is_explicit_insert=True)
    if coin_chain is None:
        coin_chain = CoincidencesChain(
            input1=coin, input2=coin_delay, name='finalCoinc', use_priority='True')
    digitizer = [singles, coin, coin_delay, coin_chain]
    return digitizer

def cylindricalPET_digitizer(rdr=None, blur=None,
                             thres=None, uph=None, 
                             coin=None, coin_delay=None):
    ad = Adder()
    if rdr is None:
        rdr = Readout(depth=1)
    if blur is None:
        blur = Blurring(resolution=0.26, eor=511.0)
    if thres is None:
        thres = ThresHolder(value=250.0)
    if uph is None:
        uph = UpHolder(value=650.0)
    singles = Singles([ad, rdr, blur, thres, uph])
    if coin is None:
        coin = CoincidenceSorter(window=10)
    if coin_delay is None:
        coin_delay = CoincidenceSorter(name='delay', window=10, offset=500,is_define_name=True, is_explicit_insert=False)
    digitizer = [singles, coin, coin_delay]
    return digitizer


def optical_digitizer(rdr = None):
    ad_op = AdderOptical()
    rdr = Readout(depth=1)
    singles = Singles([ad_op, rdr])
    digitizer = [singles,]
    return digitizer


def spect_digitizer(blur = None, spblur = None, thres = None, uph = None):
    raise NotImplementedError
