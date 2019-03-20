import click
import yaml

def kernel(config):
#    from pygate.predefined.simulations import  simulation, PredefinedSimulations
    from pygate.predefined.sources import Vec3
    from pygate.predefined._sources import plane_source
    from pygate.predefined._cameras import opticalsystem,optical_surfaces
    from pygate.predefined.parameters import optical_gamma
    from pygate.predefined.physics import optical_physics,gamma_physics
    from pygate.predefined.digitizers import optical_digitizer
    from pygate.components.geometry.volume import Box
    from pygate.components.geometry import Geometry
    from pygate.components.source import Rectangle
    from pygate.components.simulation import Simulation
    
    if config is not None:
        with open(config) as fin:
            c = yaml.load(fin)
    else:
        c = {}
        
    crystal_size=Vec3(*(list(c.get('crystal_size',(30.0,30.0,10.0)))+['mm']))
    crystal_position=Vec3(*(list(c.get('crystal_position',(0.0,0.0,5)))+['mm']))
    crystal_material=c.get('crystal_material','LYSO')
    pixel_size=Vec3(*(list(c.get('pixel_size',(3.0,3.0,1.0)))+['mm']))
    pixel_position=Vec3(*(list(c.get('pixel_position',(0.0,0.0,0.5)))+['mm']))
    source_size=c.get('source_size',[150, 150])
    source_position=Vec3(*(list(c.get('source_position',(0.0,0.0,12.0)))+['cm']))
    nb_primaries=c.get('nb_primaries',1e3)
    opt=c.get('opt','n')
#decide if there are optical physics
    if opt in ['n', 'N']:
        physics=gamma_physics(())
    elif opt in ['y', 'Y']:
        physics=optical_physics(())
    
    world=Box('world',Vec3(15,15,15,'cm'))
    box=Box('OpticalSystem',Vec3(5.0,5.0,5.0,'cm'),position=Vec3(0.0,0.0,0.0,'mm'),material='Air',mother=world)
    crystal=Box('crystal',crystal_size,position=crystal_position,material=crystal_material,mother=box)
    pixel=Box('pixel',pixel_size,position=pixel_position,material='G4_SILICON_DIOXIDE',mother=box)
    cam=opticalsystem(world,
                      box=box,
                      crystal=crystal,
                      rcp=None,
                      pixel=pixel)
    phan=()
    surf=optical_surfaces(cam)
    geo=Geometry(world,cam,phan,surf)
    src=plane_source(position=source_position,
                     src_name='plane_source',
                     rectangle=Rectangle(source_size),
                     activity=100,)
#                     particle=None)
#                     angle=AngularISO([0,360,0,360]))
    mac = Simulation(geo,
                     physics,
                     digitizers=optical_digitizer(),
                     source=src,
                     parameter=optical_gamma(nb_primaries=nb_primaries)).render()

    return mac

@click.command()
@click.option('--config', '-c', help="mac maker config.", default="makemac.yml")
@click.option('--output', '-o', help="output mac filename", default="main1.mac")
def cli(config, output):
    content = kernel(config)
    with open(output, 'w') as fout:
        print(content, file=fout)

if __name__ == '__main__':
    cli()