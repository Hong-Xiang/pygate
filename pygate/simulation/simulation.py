import camera
import physics_template as phy
from ..components import parameter as para

from ..components import ObjectWithTemplate
from ..components.simulation import *

from predefined_cameras import*
from predefined_digitizers import*
from predefined_physics import*




if __name__ == '__main__':
    sys = CylindricalPET()
    cam = Predifined_CylindricalPET()
    phy = pet_physics()
    
