from pygate.components import system
from pygate.components import geometry
from pygate.components import phantom


def predifined_voxelized_phantom(world, image_file, range_file, position):
    phan = geometry.ImageRegularParamerisedVolume(name='voxelized_phantom', image_file = image_file,
                                                  range_file = range_file, mother=world, position=position)
    return phan
