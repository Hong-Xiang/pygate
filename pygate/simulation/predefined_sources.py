from pygate.components.source import *

# voxelized gamma(back to back) source


def voxelized_gamma(position, src_name='voxelized_gamma', read_table='act_range.dat', read_file='act.h33'):
    p = ParticleGamma()
    ang = AngularISO()
    v = Voxelized('act_range.dat', 'act.h33', position=position)
    src = Source(name=src_name, particle=p, angle=ang, shape=v)
    src_list = SourceList([src, ])
    return src_list

# voxelized


def voxelized_F18(position, src_name='voxelized_F18', read_table='act_range.dat', read_file='act.h33'):
    p = ParticlePositron()
    ang = AngularISO()
    v = Voxelized('act_range.dat', 'act.h33', position)
    src = Source(src_name, p, angle=ang, shape=v)
    src_list = SourceList([src, ])
    return src_list


def cylinder_source(position = Vec3(0,0,0), src_name='cylinder_source', cylinder=None,
                               activity=None, particle=None, angle = None):
    
    if cylinder is None:
        cylinder = Cylinder(5, 5, 'Volume')
    if activity is None:
        activity = 10000
    if particle is None:
        particle = ParticleGamma()
    if angle is None:
        angle = AngularISO()
    src = Source(src_name,particle,activity,angle,cylinder,position)
    src_list = SourceList([src,])
    return src_list

def plane_source(position = Vec3(0,0,0), src_name = 'plane_source', rectangle = None, activity =None, particle = None, angle = None):
    if rectangle is None:
        rectangle = Rectangle([15,15])
    if activity is None:
        activity = 1000
    if particle is None:
        particle = ParticleGamma(back2back=False)
    if angle is None:
        angle = AngularISO([90,90,0,0]) # default to the positive x direction.
    src = Source(src_name,particle,activity,angle,rectangle,position)
    src_list = SourceList([src,])
    return src_list

def sphere_source(position = Vec3(0,0,0), src_name = 'sphere_source',sphere = None, activity =None, particle = None, angle = None):
    if sphere is None:
        sphere = Sphere(0.1,dimension = 'Volume')
    if activity is None:
        activity = 1000
    if particle is None:
        particle = ParticleGamma(back2back=False)
    if angle is None:
        angle = AngularISO([90,90,0,0]) # default to the positive x direction.
    src = Source(src_name,particle,activity,angle,sphere,position)
    src_list = SourceList([src,])
    return src_list