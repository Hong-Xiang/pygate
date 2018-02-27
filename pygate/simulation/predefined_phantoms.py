from pygate.components.geometry.volume import *
from pygate.components.geometry.phantom import Phantom


def voxelized_phantom(world, image_file = 'phan.h33', range_file = 'mat_range.dat', position = None):
    
    iv = ImageRegularParamerisedVolume(name='voxelized_phantom', image_file = image_file,
                                                  range_file = range_file, mother=world, position=position)
    phan = Phantom([iv,])
    return phan
