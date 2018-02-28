from ..components.parameter import *


def pet_parameters(acqu=AcquisitionPeriod(),
                              outputs=None,
                              rand=RandomEngine(seed='auto')):
    if outputs is None:
        outputs = [Root('pet',1,1,1,None,1),]
    return Parameter(rand,outputs, acqu)


def optical_parameters(acqu=AcquisitionPrimaries(number=10000),
                                  outputs=None,
                                  rand=RandomEngineMersenneTwister(seed='auto')):
    if outputs is None:
        outputs = [Root('optical', 1, 1, None, 1, None),]
    return Parameter(rand, outputs, acqu)
