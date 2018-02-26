from ..components.digitizer import *
from .camera import *

class EcatDigitizer:
    def __init__(self):
        ad = Adder()
        rdr = Readout()
        blur = Blurring(resolution= 0.26, eor = 511.0)
        thres = ThresHolder(value= 250.0)
        uph = UpHolder(value = 750.0)
        ddt = DeadTime(volume = cam.block,t = 3000000.0,mode='paralysable')
        singles = Singles([ad,rdr,blur,thres,uph,ddt])
        
class CylindricalPETDigitizer:
    def __init__(self, cam):
        ad = Adder()
        rdr = Readout()
        blur = Blurring(resolution= 0.26, eor = 511.0)
        thres = ThresHolder(value= 250.0)
        uph = UpHolder(value = 750.0)
        ddt = DeadTime(volume = cam.block,t = )
        singles = Singles([ad, rdr, blur, thres, uph, ddt])