from ..components.parameter import *


def pet_parameters(acqu=AcquisitionPeriod(),
                              outputs=[],
                              rand=RandomEngine(seed='auto')):
    if outputs is None:
        outputs = [Root('pet',1,1,1,0,1),]
    return Parameter(rand,acqu,outputs)


def optical_parameters(acqu=AcquisitionPrimaries(number=100),
                                  outputs=[],
                                  rand=RandomEngineMersenneTwister(seed='auto')):
    if outputs is None:
        outputs = [Root('optical', 1, 1, 0, 1, 0),]
    return Parameter(rand, acqu, outputs)
