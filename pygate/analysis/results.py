from enum import Enum
from functools import reduce
from typing import Tuple

import numpy as np
import pandas as pd
import dask.dataframe as ddf
import dask
from dask.dataframe.groupby import DataFrameGroupBy


class ParticleID(Enum):
    Gamma = 22


class ColumnNames:
    Event = 'eventID'
    Process = 'processName'
    Particle = 'particalID'
    SourceX = 'srcX'
    SourceY = 'srcY'
    SourceZ = 'srcZ'
    X = 'x'
    Y = 'y'
    Z = 'z'
    EnergyDeposit = 'energy'


class ResultBase:
    def __init__(self, data=None):
        self.data = data

    @property
    def d(self):
        return self.data


class Results(ResultBase):
    def __init__(self, data: Tuple[ResultBase]):
        super().__init__(tuple(data))

    def map(self, func) -> 'Results':
        return Results(map(func, self.d))

    def filter(self, func) -> 'Results':
        return Results(filter(func, self.d))

    def call(self, func_name) -> 'Results':
        return Results(map(self.d, lambda x: getattr(x, 'func_name')()))

    def zip(self, r: 'Results'):
        return Results(zip(self.d, r.d))

    def first(self) -> ResultBase:
        return self.d[0]

    def flatten(self) -> 'Results':
        if not isinstance(self.d[0], Results):
            raise TypeError(
                "Flatten requires Results of Results, got {}.".format(type(self.d[0])))
        return Results(tuple(sum([list(d.d) for d in self.d], [])))

    def merge(self) -> ResultBase:
        result = None
        for o in self.d:
            if result is None:
                result = o
            else:
                result = result.merge(o)
        return result

    def to_list(self):
        return list(self.d)

class ResultsDask(ResultBase):
    def map(self, func) -> 'ResultsDask':
        return Results(dask.delayed(map)(func, self.d))
    


class ResultsNamedTuple(ResultBase):
    pass




class ResultsWithKeys(Results):
    def __init__(self, data: Tuple[Tuple[str, ResultBase]]):
        super().__init__(data)

    def drop_keys(self) -> Results:
        return self.map(lambda x: x[1])

    def to_dict(self):
        return {o[0]: o[1] for o in self.d}

    def select(self, key):
        for o in self.d:
            if o[0] == key:
                return o[1]
        raise KeyError("Key {} not found.".format(key))


class ResultsWithUnknownKeys(ResultsDask):
    def select(self, key):
        return DataFrame(self.d.get_group(key))

    def drop_keys(self) -> ResultsDask:
        return self.map(lambda x: x[1])


class Series(ResultBase):
    def __init__(self, series: pd.Series):
        super().__init__(series)

    def columns(self, *cols):
        return (self.d[c] for c in cols)

    def position(self) -> 'Vec3':
        return Vec3(*self.columns(ColumnNames.X,
                                  ColumnNames.Y,
                                  ColumnNames.Z))

    def source_position(self) -> 'Vec3':
        return Vec3(*self.columns(ColumnNames.SourceX,
                                  ColumnNames.SourceY,
                                  ColumnNames.SourceZ))

    def energy_deposit(self) -> float:
        return self.d[ColumnNames.EnergyDeposit]


class DataFrame(ResultBase):
    def __init__(self, dataframe: pd.DataFrame):
        super().__init__(dataframe)

    def first(self, *columns) -> Series:
        return Series(self.d.iloc[0])

    def split_by(self, column: str) -> ResultsWithKeys:
        groups = self.d.groupby(column)
        if isinstance(groups, DataFrameGroupBy):
            return ResultsWithUnknownKeys(groups)
        else:
            return ResultsWithKeys(((k, DataFrame(groups.get_group(k).drop([column], axis=1))) for k in groups.groups))

    def split_row(self) -> Results:
        return Results((Series(self.d.iloc[i]) for i in range(self.d.shape[0])))

    def merge(self, r) -> 'DataFrame':
        if not isinstance(r, DataFrame):
            raise TypeError(
                "Can not merge {} with {}.".format(__class__, type(r)))
        return DataFrame(pd.concat([self.d, r.d], axis=0))

    def to_event(self) -> 'Event':
        if not ColumnNames.Event in self.d.columns:
            return Event(self.d)




class Vec3(ResultBase):
    def __init__(self, x, y=None, z=None):
        super().__init__(np.array([x, y, z]))

    @property
    def x(self) -> float:
        return self.d[0]

    @property
    def y(self) -> float:
        return self.d[1]

    @property
    def z(self) -> float:
        return self.d[2]

    def to_list(self):
        return tuple(self.d)


class EnergyDeposit(ResultBase):
    def __init__(self, position, energy):
        super().__init__((position, energy))

    @property
    def position(self):
        return self.d[0]

    @property
    def energy(self):
        return self.d[1]


class Event(DataFrame):
    def __init__(self, dataframe: pd.DataFrame):
        super().__init__(dataframe)

    def source_position(self) -> Vec3:
        return self.first().source_position()

    def first_position(self) -> Vec3:
        return self.first().position()

    def incident_direction(self) -> Vec3:
        dp = self.first_position().d - self.source_position().d
        return Vec3(*tuple(dp / np.linalg.norm(dp)))

    def energy_deposit_list(self) -> Results:
        return self.split_row().map(lambda s: EnergyDeposit(s.position(), s.energy_deposit()))


class CSVFile(ResultBase):
    def __init__(self, filename: str):
        super().__init__(filename)

    def load(self) -> DataFrame:
        return DataFrame(pd.read_csv(self.d))
