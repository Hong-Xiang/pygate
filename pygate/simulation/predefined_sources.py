from pygate.components import system
from pygate.components import geometry
from pygate.components import source


def predifined_voxelized_source(world, image_file, range_file, position):
    
    src = source.Source(name='voxelized_source', image_file = image_file,
                                                  range_file = range_file, mother=world, position=position)
    return src