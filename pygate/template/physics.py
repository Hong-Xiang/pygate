import yaml

class CutPair:
    def __init__(self, region=None, cutValue=None):
        self.cutValue = cutValue
        self.region = region
class MaxStep:
    def __init__(self,region = None, maxstepsize = None):
        self.maxstepsize = maxstepsize
        self.region = region
class Physics():
    def __init__(self):
        # self.flag = True
        # self.CutStr = ""
        self.cutPairList = []
        self.maxstepsizeList = []
    def getModelStr(self):
        return(r"/gate/physics/addProcess PhotoElectric" + "\n" 
                +"/gate/physics/processes/PhotoElectric/setModel StandardModel" + "\n" 
                +r"/gate/physics/addProcess Compton" + "\n" 
                +r"/gate/physics/processes/Compton/setModel StandardModel" + "\n" 
                +r"/gate/physics/addProcess RayleighScattering" + "\n" 
                +r"/gate/physics/processes/RayleighScattering/setModel PenelopeModel" + "\n" 
                +r"/gate/physics/addProcess ElectronIonisation" + "\n" 
                +r"/gate/physics/processes/ElectronIonisation/setModel StandardModel e-" + "\n" 
                +r"/gate/physics/processes/ElectronIonisation/setModel StandardModel e+" + "\n" 
                +r"/gate/physics/addProcess Bremsstrahlung" + "\n" 
                +r"/gate/physics/processes/Bremsstrahlung/setModel StandardModel e-" + "\n" 
                +r"/gate/physics/processes/Bremsstrahlung/setModel StandardModel e+" + "\n" 
                +r"/gate/physics/addProcess PositronAnnihilation" + "\n" 
                +r"/gate/physics/addProcess MultipleScattering e+"+"\n"
                +r"/gate/physics/addProcess MultipleScattering e-"+"\n"
               # +r"/gate/physics/addProcess eMultipleScattering" + "\n" 
               # +r"/gate/physics/processes/eMultipleScattering/setGeometricalStepLimiterType e- distanceToBoundary" + "\n" 
               # +r"/gate/physics/processes/eMultipleScattering/setGeometricalStepLimiterType e+ distanceToBoundary" + "\n" 
               # +r"/gate/physics/addProcess RadioactiveDecay" + "\n" 
               # +r"/gate/physics/addAtomDeexcitation" + "\n" 
                +r"/gate/physics/processList Enabled" + "\n" 
                +r"/gate/physics/processList Initialized" + "\n" )

    def addCutPair(self,item):
        if item.cutValue is None or item.region is None:
            pass
        else:
            self.cutPairList.append(item)

    def addMaxStep(self,item):
        if item.maxstepsize is None or item.region is None:
            pass
        else:
            self.maxstepsizeList.append(item)

    def getMacStr(self):
        fmt1 = r"/gate/physics/Gamma/SetCutInRegion {0}  {1}"+" mm\n"
        fmt2 = r"/gate/physics/Electron/SetCutInRegion {0}  {1}"+" mm\n"
        fmt3 = r"/gate/physics/Positron/SetCutInRegion {0}  {1}"+" mm\n"

        fmt4 = r"/gate/physics/SetMaxStepSizeInRegion {0} {1}" +" mm\n"
        Str = ""
        for item in self.cutPairList:
            Str += fmt1.format(item.region,item.cutValue)
            Str += fmt2.format(item.region,item.cutValue)
            Str += fmt3.format(item.region,item.cutValue)
        for item in self.maxstepsizeList:
            Str += fmt4.format(item.region,item.maxstepsize)
        return (self.getModelStr()+Str)

# if __name__ == '__main__':
#     phy = Physics()
#     phy.addCutPair(CutPair(region = 'level1', cutValue = 10 ))
#     print(phy.getMacStr())
#     with open('physics.yml', 'w') as fout:
#         yaml.dump(phy, fout)

        


