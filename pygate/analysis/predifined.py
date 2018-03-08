from .results import *


def gamma_from_csv(csv_filename):
    events = (CSVFile('hits.csv').load()
              .split_by(ColumnNames.Particle)
              .select(ParticleID.Gamma.value)
              .split_by(ColumnNames.Event).drop_keys()
              .map(lambda e: e.to_event()))
    incident_directions = (events.map(lambda e: e.incident_direction())
                           .map(lambda v: v.to_list()).to_list())
    source_postions = (events.map(lambda e: e.source_postions())
                       .map(lambda v: v.to_list()).to_list())

    return
