from .base import OperationOnFile, RoutineOnDirectory
from dxl.fs import Directory, File
from enum import Enum

from pygate.analysis import predifined as pd


class KEYS:
    SOURCE = 'source'
    TARGET = 'target'
    ANALYSIS = 'analysis'


class AnalysisType(Enum):
    GAMMA_ENERGY_DEPOSIT_DISTRIBUTION = 'gamma_edep'


class OperationAnalysis(OperationOnFile):
    def __init__(self, source_csv_filename, target_h5_filename,
                 analysis_type: AnalysisType=None):
        super().__init__(target_h5_filename)
        self.source_filename = source_csv_filename
        if isinstance(analysis_type, str):
            self.analysis_type = AnalysisType(analysis_type)
        else:
            self.analysis_type = analysis_type

    def source(self, r: RoutineOnDirectory):
        return r.directory.attach_file(self.source_filename)

    def apply(self, r: RoutineOnDirectory):
        source = self.source(r)
        target = self.target(r)
        func_map = {
            AnalysisType.GAMMA_ENERGY_DEPOSIT_DISTRIBUTION: pd.gamma_energy_deposit_distribution
        }
        func_map[self.analysis_type](source.system_path(),
                                     target.system_path())
        return {KEYS.SOURCE: source.path.s,
                KEYS.TARGET: target.path.s,
                KEYS.ANALYSIS: self.analysis_type.value}

    def dryrun(self, r: RoutineOnDirectory):
        source = self.source(r)
        target = self.target(r)
        return {KEYS.SOURCE: source.path.s,
                KEYS.TARGET: target.path.s,
                KEYS.ANALYSIS: self.analysis_type.value}
