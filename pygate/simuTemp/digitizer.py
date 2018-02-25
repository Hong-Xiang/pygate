import yaml


class AttrPair:
    def __init__(self, value=None, fmtstr=None):
        self.value = value
        self.fmtstr = fmtstr


class DigiModule:
    moduleList = ['distributions', 'adder', 'adderCompton', 'readout',
                  'blurring', 'crystalBlurring', 'localBlurring', 'intrinsicResolutionBlurring ', 'quantumEfficiency ', 'calibration', 'crosstalk',
                  'thresholder', 'upholder', 'timeResolution', 'spBlurring', 'noise', 'localEffciency', 'buffer',
                  'deadtime']

    def __init__(self, moduleType=None, chainName=None):
        if moduleType in DigiModule.moduleList:
            self.moduleType = moduleType
        self.chainName = chainName
        self.attrList = []

    def makeAttrList(self):
        newFmt = r"/gate/digitizer/{0}/insert {1}" + "\n"
        self.addAttr(AttrPair(self.chainName, newFmt.format(
            self.chainName, self.moduleType)))

    def addAttr(self, attrItem):
        self.attrList.append(attrItem)

    def getMacStr(self):
        self.makeAttrList()
        mac = ""
        for item in self.attrList:
            if item.value is not None:
                mac += item.fmtstr
        return mac

    def getMeStr(self):
        fmt = r"/gate/digitizer/{0}/{1}"
        return fmt.format(self.chainName, self.moduleType)


# class Distributions(DigiModule):
#     def __init__(self):
#         pass


class Adder(DigiModule):
    def __init__(self, chainName=None):
        super(Adder, self).__init__(moduleType='adder', chainName=chainName)


class AdderCompton(DigiModule):
    def __init__(self, chainName=None):
        super(AdderCompton, self).__init__(
            moduleType='adderCompton', chainName=chainName)


class Readout(DigiModule):
    def __init__(self, chainName=None, policy='TakeEnergyCentroid', depth=1):
        super(Readout, self).__init__(
            moduleType='readout', chainName=chainName)
        self.policy = policy
        self.depth = depth

    def makeAttrList(self):
        super(Readout, self).makeAttrList()
        fmt1 = self.getMeStr() + r"/setPolicy {0} " + "\n"
        fmt2 = self.getMeStr() + r"/setDepth  {0} " + "\n"
        self.attrList.append(AttrPair(self.policy, fmt1.format(self.policy)))
        self.attrList.append(AttrPair(self.depth, fmt2.format(self.depth)))


class Blurring(DigiModule):
    def __init__(self, chainName=None, law = None, res=0.15, eor=511, slope=None):
        super(Blurring, self).__init__(
            moduleType='blurring', chainName=chainName)
        self.law = law
        self.resolution = res
        self.eor = eor
        self.slope = slope

    def makeAttrList(self):
        super(Blurring, self).makeAttrList()
        fmt1 = self.getMeStr() + r"/setLaw {0}" + "\n"
        fmt2 = self.getMeStr() + r"/setResolution {0}" + "\n"
        fmt3 = self.getMeStr() + r"/setEnergyOfReference {0} keV" + " \n"
        fmt4 = self.getMeStr() + r"/setSlope {0}  1/keV" + "\n"
        self.attrList.append(AttrPair(self.law, fmt1.format(self.law)))
        self.attrList.append(
            AttrPair(self.resolution, fmt2.format( self.resolution)))
        self.attrList.append(
            AttrPair(self.eor, fmt3.format( self.eor)))
        self.attrList.append(
            AttrPair(self.slope, fmt4.format( self.slope)))


class CrystalBlurring(DigiModule):
    def __init__(self, chainName=None, resWindow=[0, 1], qe=1, eor=511):
        super(CrystalBlurring, self).__init__(
            moduleType='crystalBlurring', chainName=chainName)
        self.resWindow = resWindow
        self.qe = qe
        self.eor = eor

    def makeAttrList(self):
        super(CrystalBlurring, self).makeAttrList()
        fmt1 = self.getMeStr() + r"/setCrystalResolutionMin {0}" + "\n" + self.getMeStr(
        ) + r"/setCrystalResolutionMax {1}" + "\n"
        fmt2 = self.getMeStr() + r"/setCrystalQE {0} " + " \n"
        fmt3 = self.getMeStr() + r"/setEnergyOfReference {0}  keV" + "\n"

        self.attrList.append(AttrPair(self.resWindow, fmt1.format(
            self.resWindow[0], self.resWindow[1])))
        self.attrList.append(AttrPair(self.qe, fmt2.format(self.qe)))
        self.attrList.append(AttrPair(self.eor, fmt3.format(self.eor)))


class ThresHolder(DigiModule):
    def __init__(self, chainName=None, holdvalue=250):
        super(ThresHolder, self).__init__(
            moduleType='thresholder', chainName=chainName)
        self.holdvalue = holdvalue

    def makeAttrList(self):
        super(ThresHolder, self).makeAttrList()
        fmt1 = self.getMeStr() + r"/setThreshold {0} keV" + "\n"
        self.attrList.append(
            AttrPair(self.holdvalue, fmt1.format(self.holdvalue)))


class UpHolder(DigiModule):
    def __init__(self, chainName=None,  holdvalue=750):
        super(UpHolder, self).__init__(
            moduleType='upholder', chainName=chainName)
        self.holdvalue = holdvalue

    def makeAttrList(self):
        super(UpHolder, self).makeAttrList()
        fmt1 = self.getMeStr() + r"/setUphold {0} keV" + "\n"
        self.attrList.append(
            AttrPair(self.holdvalue, fmt1.format(self.holdvalue)))


class TimeResolution(DigiModule):
    def __init__(self, chainName=None, res=1):
        super(TimeResolution, self).__init__(
            moduleType='timeResolution', chainName=chainName)
        self.resolution = res

    def makeAttrList(self):
        super(TimeResolution, self).makeAttrList()
        fmt1 = self.getMeStr() + r"/setTimeResolution {0}  ns" + "\n"
        self.attrList.append(
            AttrPair(self.resolution, fmt1.format(self.resolution)))


class SpBlurring(DigiModule):
    def __init__(self, chainName=None, res=2):
        super(SpBlurring, self).__init__(
            moduleType='spBlurring', chainName=chainName)
        self.resolution = res

    def makeAttrList(self):
        super(SpBlurring, self).makeAttrList()
        fmt1 = self.getMeStr() + r"/setSpresolution {0}  mm" + "\n"
        self.attrList.append(
            AttrPair(self.resolution, fmt1.format(self.resolution)))

class Buffer(DigiModule):
    def __init__(self, chainName = None, bufferSize =  None, readFreq = None, mode = None):
        super(Buffer, self).__init__(moduleType= 'buffer',chainName = chainName)
        self.bufferSize = bufferSize
        self.readFreq = readFreq
        self.mode = mode
    def makeAttrList(self):
        super(Buffer, self).makeAttrList()
        fmt1 = self.getMeStr() + r"/setBufferSize {0}  B" +"\n"
        fmt2 = self.getMeStr() + r"/setReadFrequency  {0}  MHz" +"\n"
        fmt3 = self.getMeStr() + r"/setMode {0}" +"\n"

        self.attrList.append(AttrPair(self.bufferSize,fmt1.format(self.bufferSize)))
        self.attrList.append(AttrPair(self.readFreq, fmt2.format(self.readFreq)))
        self.attrList.append(AttrPair(self.mode,fmt3.format(self.mode)))

class DeadTime(DigiModule):
    def __init__(self, dtVolume,deadtime, chainName=None, deadMode=None,  bufferSize=None, bufferMode=None):
        super(DeadTime, self).__init__(
            moduleType='deadtime', chainName=chainName)
        self.deadtime = deadtime
        self.deadMode = deadMode
        # if dtVolume is None:
        #     print("DeadTime: no Dead time volume")
        self.dtVolume = dtVolume
        self.bufferSize = bufferSize
        self.bufferMode = bufferMode

    def makeAttrList(self):
        super(DeadTime, self).makeAttrList()
        fmt0 = self.getMeStr() + r"/setDeadTime {0} ns" + "\n"
        fmt1 = self.getMeStr() + r"/setMode {0}" + "\n"
        fmt2 = self.getMeStr() + r"/chooseDTVolume {0}" + "\n"
        fmt3 = self.getMeStr() + r"/setBufferSize {0} MB" + "\n"
        fmt4 = self.getMeStr() + r"/setBufferMode {0} " + "\n"

        self.attrList.append(
            AttrPair(self.deadtime, fmt0.format(self.deadtime)))
        self.attrList.append(
            AttrPair(self.deadMode, fmt1.format(self.deadMode)))
        self.attrList.append(
            AttrPair(self.dtVolume, fmt2.format(self.dtVolume)))
        self.attrList.append(
            AttrPair(self.bufferSize, fmt3.format(self.bufferSize)))
        self.attrList.append(
            AttrPair(self.bufferMode, fmt4.format(self.bufferMode)))


class SingleChain:
    def __init__(self, name=None, input=None):
        if name is None:
            self.name = 'Singles'
            self.input = None
        else:
            self.name = name
            if input is None:
                self.input = 'Singles'
            else:
                self.input = input
        self.moduleList = []

    def addModule(self, item=None):
        if item is None:
            pass
        else:
            item.chainName = self.name
            self.moduleList.append(item)

    def getMacStr(self):
        mac = ""
        if self.name == 'Singles':
            pass
        else:
            fmt1 = r"/gate/digitizer/name {0}" + "\n"
            fmt2 = r"/gate/digitizer/insert SingleChain" + "\n"
            fmt3 = r"/gate/digitizer/{0}/setInputName {1}" + "\n"
            mac += fmt1.format(self.name) + fmt2.format() + \
                fmt3.format(self.name, self.input)
        for item in self.moduleList:
            mac += item.getMacStr()
        return mac





class CoinSorter:
    def __init__(self, name = None, inputName = None, window = None, minSectorDifference = None,
                 offset = None, depth = None, allPulsesOpenCoincGate = None, multipolicy = None):
        if name is None:
            self.name = 'Coincidences'
        else:
            self.name = name
        self.inputName = inputName
        self.window = window
        self.minSectorDifference = minSectorDifference
        self.offset = offset
        self.depth = depth
        self.allPulsesOpenCoincGate = allPulsesOpenCoincGate
        self.multipolicy = multipolicy
        self.attrList = []
   
    def makeAttrList(self):
        if self.name == 'Coincidences':
            pass
        else:            
            nameFmt = r"/gate/digitizer/name {0}" + "\n"
            insertFmt = r"/gate/digitizer/insert coincidenceSorter " + "\n"
            self.addAttr(AttrPair(self.name, nameFmt.format(self.name)+insertFmt.format()))
        fmt0 = self.getMeStr()+r"/addInputName {0}"
        fmt1 = self.getMeStr()+r"/setWindow {0}  ns" +"\n"
        fmt2 = self.getMeStr()+r"/minSectorDifference {0}" +"\n"
        fmt3 = self.getMeStr()+r"/setOffset {0}  ns" +"\n"
        fmt4 = self.getMeStr()+r"/setDepth {0}" +"\n"
        fmt5 = self.getMeStr()+r"/allPulsesOpenCoincGate {0}" + "\n"
        fmt6 = self.getMeStr()+r"/setMultiplePolicy {0}" + "\n"

        self.addAttr(AttrPair(self.inputName,fmt0.format(self.name,self.inputName)))
        self.addAttr(AttrPair(self.window,fmt1.format(self.window)))
        self.addAttr(AttrPair(self.minSectorDifference,fmt2.format(self.minSectorDifference)))
        self.addAttr(AttrPair(self.offset,fmt3.format(self.offset)))
        self.addAttr(AttrPair(self.depth,fmt4.format(self.depth)))
        self.addAttr(AttrPair(self.allPulsesOpenCoincGate,fmt5.format(self.allPulsesOpenCoincGate)))
        self.addAttr(AttrPair(self.multipolicy,fmt6.format(self.multipolicy)))        

    def addAttr(self, attrItem):
        self.attrList.append(attrItem)

    def getMacStr(self):
        self.makeAttrList()
        mac = ""
        for item in self.attrList:
            if item.value is not None:
                mac += item.fmtstr
        return mac

    def getMeStr(self):
        fmt = r"/gate/digitizer/{0}"
        return fmt.format(self.name)


class CoinChain:
    def __init__(self, name = None, inputList = None, usePriority = None):
        if name is None:
            print("No CoinChain name! CoinChain:__init__() \n")
        else:
            self.name = name
        if inputList is None:
            self.inputList = []
        else:
            self.inputList = inputList
        self.moduleList = []
        self.usePriority = usePriority
    def addInput(self, item):
        if item is not None:
            self.inputList.append(item)
   

    def addModule(self, item=None):
        if item is not None:
            item.chainName = self.name
            self.moduleList.append(item)

    def getMacStr(self):
        mac = ""
        if self.name is None:
            pass
        else:
            fmt1 = r"/gate/digitizer/name {0}" + "\n"
            fmt2 = r"/gate/digitizer/insert coincidenceChain" + "\n"
            mac += fmt1.format(self.name) + fmt2.format()
        fmt3 = r"/gate/digitizer/{0}/addInputName {1}" + "\n"
        for item in self.inputList:
            mac += fmt3.format(self.name,item)     
        for item in self.moduleList:
            mac += item.getMacStr()
        if self.usePriority is not None:
            fmt4 = r"/gate/digitizer/{0}/usePriority true"
            mac += fmt4.format(self.name)
        return mac


class Digitizer:
    def __init__(self):
        self.moduleList = []
    
    def addModule(self, module):
        self.moduleList.append(module)

    def getMacStr(self):
        mac =""
        for item in self.moduleList:
            mac += item.getMacStr()
        return mac


# if __name__ == '__main__':


#     # print(digi.getMacStr())

# with open('digitizer.yml', 'w') as fout:
#     yaml.dump(digi, fout)
