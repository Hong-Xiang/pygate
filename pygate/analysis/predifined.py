from .results import *
from dxl.fs import File


def gamma_energy_deposit_distribution(csv_filename, h5_filename):
    events = (CSVFile(csv_filename).load()
              .split_by(ColumnNames.Particle)
              .select(ParticleID.Gamma.value)
              .split_by(ColumnNames.Event).drop_keys()
              .map(lambda e: e.to_event()))

    # incident_directions = (events.map(lambda e: e.incident_direction())
    #    .map(lambda v: v.to_list()).to_list())
    # source_postions = (events.map(lambda e: e.source_postions())
    #    .map(lambda v: v.to_list()).to_list())
    # deposits = events.
    eps = events.map(lambda e: e.energy_deposit_list()).flatten()
    poss = eps.map(lambda ep: ep.position).map(lambda p: p.to_list())
    engs = eps.map(lambda ep: ep.energy)
    rezip = poss.zip(engs).map(lambda t: tuple(list(t[0]) + [t[1]]))
    df = pd.DataFrame(data=np.array(rezip.d), columns=[
                      'x', 'y', 'z', 'energy'])
    df.to_hdf(h5_filename, 'gamma_edep')
    return h5_filename
