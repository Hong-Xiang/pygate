from . import camera
from . import phantom as phantomModule
from . import source
from . import digitizer
from . import physics
from . import geometry

import yaml
from fs.osfs import OSFS
import os


class RunTime:
    def __init__(self,  endTime=1, timeSlice=1, startTime=0):
        self.endTime = endTime
        self.timeSlice = timeSlice
        self.startTime = startTime

    def getMacStr(self):
        fmt = (r"/gate/application/setTimeSlice  {0} s" + "\n"
               + r"/gate/application/setTimeStart  {1} s" + "\n"
               + r"/gate/application/setTimeStop  {2} s" + "\n")
        return fmt.format(self.timeSlice, self.startTime, self.endTime)


class DataOut:
    OutList = ["ascii", "binary", "root", "sinogram"]

    def __init__(self, outType, fileName):
        self.outType = outType
        self.fileName = fileName

    def getMacStr(self):
        fmt = (r"/gate/output/{0} enable" + "\n"
               + r"/gate/output/{0}/setFileName  {1}" + "\n")
        return fmt.format(self.outType, self.fileName)


class FlagPair:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Root(DataOut):
    def __init__(self, fileName, flagList=[FlagPair('Hit', 0), FlagPair('Singles', 0), FlagPair('Coincidences', 0)]):
        super(Root, self).__init__(outType='root', fileName=fileName)
        self.flagList = flagList

    def addFlag(self, item):
        self.flagList.append(item)

    def getMacStr(self):
        mac = ""
        mac += super(Root, self).getMacStr()
        fmt = r"/gate/output/root/setRoot{0}Flag    {1}" + "\n"
        for item in self.flagList:
            mac += fmt.format(item.name, item.value)
        return mac


class RandomEngine:
    engineList = ['JamesRandom', 'Ranlux64', 'MersenneTwister']

    def __init__(self, name='JamesRandom', seed='default'):
        self.name = name
        self.seed = seed

    def getMacStr(self):
        fmt = (r"/gate/random/setEngineName {0}" + "\n"
               + r"/gate/random/setEngineSeed {1}" + "\n")
        return fmt.format(self.name, self.seed)


class SimuApp:
    def __init__(self, name='simu1', cam=None, phan=None, src=None, digi=None, phy=None,
                 dataOut=None, runTime=RunTime(), worldSize=geometry.Vec3(100, 100, 100), randEngine=RandomEngine()):
        self.name = name
        self.cam = cam
        self.phan = phan
        self.src = src
        self.digi = digi
        self.phy = phy
        self.dataOut = dataOut
        self.runTime = runTime
        self.worldSize = worldSize
        self.randEngine = randEngine

    def getComMac(self):
        mac = ""
        camFmt = r"/control/execute camera.mac" + "\n"
        phanFmt = r"/control/execute phantom.mac" + "\n"
        phyFmt = r"/control/execute physics.mac" + "\n"
        initFmt = r"/gate/run/initialize" + "\n"
        digiFmt = r"/control/execute digitizer.mac" + "\n"
        srcFmt = r"/control/execute source.mac" + "\n"
        mac = camFmt + phanFmt + phyFmt + initFmt + digiFmt + srcFmt
        return mac

    def getMacStr(self):
        mac = ""
        materdbFmt = r"/gate/geometry/setMaterialDatabase    ./GateMaterials.db" + "\n"
        worldFmt = (r"/gate/world/geometry/setXLength  {0} cm" + "\n"
                    + r"/gate/world/geometry/setYLength  {1} cm" + "\n"
                    + r"/gate/world/geometry/setZLength  {2} cm" + "\n")

        startFmt = r"/gate/application/startDAQ" + "\n"

        mac = (materdbFmt + worldFmt.format(self.worldSize.x, self.worldSize.y, self.worldSize.z)
               + self.getComMac() + self.randEngine.getMacStr() + self.dataOut.getMacStr() + self.runTime.getMacStr() + startFmt)
        return mac

    def generateYaml(self):
        with open(self.name + '.yml', 'w') as fout:
            yaml.dump(self, fout)

    def generateMacs(self):
        # currPath = os.getcwd()
        if(os.path.exists("SimuMacs")):
            with OSFS('.') as fs:
                fs.removetree('SimuMacs')
                # os.rmdir('SimuMacs')
        # else:
        os.mkdir('SimuMacs')
        with open(os.getcwd() + '/SimuMacs/camera.mac', 'w') as file_object:
            file_object.write(self.cam.getMacStr())
        # file_object.close()

        file_object = open(os.getcwd() + '/SimuMacs/phantom.mac', 'w')
        file_object.write(self.cam.getMacStr())
        file_object.close()

        file_object = open(os.getcwd() + '/SimuMacs/physics.mac', 'w')
        file_object.write(self.phy.getMacStr())
        file_object.close()

        file_object = open(os.getcwd() + '/SimuMacs/digitizer.mac', 'w')
        file_object.write(self.digi.getMacStr())
        file_object.close()

        file_object = open(os.getcwd() + '/SimuMacs/source.mac', 'w')
        file_object.write(self.src.getMacStr())
        file_object.close()

        file_object = open(os.getcwd() + '/SimuMacs/main.mac', 'w')
        file_object.write(self.getMacStr())
        file_object.close()


# if __name__ == '__main__':
def make_yml(yml_filename):
    # Camera
    c1 = geometry.Cylinder(name='ecat', Rmax=82, Rmin=56, Height=5)
    # print (b1.getMacStr())
    b1 = geometry.Box(name='block', position=geometry.Vec3(
        66.5, 0.0, 0.0), size=geometry.Vec3(20, 44, 5))
    b2 = geometry.Box(name='crystal', size=geometry.Vec3(20, 2, 2))
    c1.addChild(b1)
    b1.addChild(b2)
    cbr1 = geometry.CubicRepeater(volume=b2.name, scale=geometry.Vec3(
        1, 20, 1), repeatVector=geometry.Vec3(0, 2.2, 0))
    sys = camera.Ecat()
    sys.attachSystem(itemList=[b1.name, b2.name])

    # create the camera and construt it
    camera1 = camera.Camera(name='cam1', system=sys)
    camera1.addGeo(c1)
    camera1.addGeo(cbr1)
    camera1.addCrystalSD(b2.name)
    ############################################################

    # phantom
    c1 = geometry.Cylinder(
        mother='world', name='NEMACylinder', Rmax=82, Rmin=56, Height=5)
    # print (b1.getMacStr())
    # b1 = geometry.Box(mother=c1.name, name='', position=geometry.Vec3(
    #     66.5, 0.0, 0.0), size=geometry.Vec3(20, 44, 5))
    # c1.addChild(b1)

    phantom = phantomModule.Phantom(name='phantom1')
    phantom.addGeo(c1)
    phantom.addPhantomSD(b1)
    ##################################################

    # source
    src1 = source.SrcItem(name='src1')
    src1.addSrcModule(source.Particle(paticleType='gamma'))
    src1.addSrcModule(source.Angular(ang=[90, 90, 0, 360]))
    # src1.addSrcModule(Rectangle(halfSize = [10,20]))
    src1.addSrcModule(source.Cylinder(dimension='Volume', halfz=10, radius=10))
    src1.addSrcModule(source.Placement(placement=geometry.Vec3(10, 10, 10)))

    src = source.Source()
    src.addSourceItem(src1)
    ##################################################

    # digitizer
    sc = digitizer.SingleChain()
    a = digitizer.Adder()
    r = digitizer.Readout()
    sc.addModule(a)
    sc.addModule(r)
    sc.addModule(digitizer.Blurring())
    sc.addModule(digitizer.CrystalBlurring())
    sc.addModule(digitizer.ThresHolder())
    sc.addModule(digitizer.UpHolder())
    sc.addModule(digitizer.TimeResolution())
    sc.addModule(digitizer.SpBlurring())
    sc.addModule(digitizer.DeadTime(dtVolume = 'crystal'))
    coin1 = digitizer.CoinSorter(window=20)
    coin2 = digitizer.CoinSorter(name='LowCoin', window=10)
    conichain1 = digitizer.CoinChain(name='finalcoin', inputList=['coin1', 'coin2'])
    conichain1.addModule(digitizer.DeadTime(dtVolume = 'crystal'))
    conichain1.addModule(digitizer.Buffer())
    digi = digitizer.Digitizer()
    digi.addModule(sc)
    digi.addModule(coin1)
    digi.addModule(coin2)
    digi.addModule(conichain1)
    #####################################################

    # physics
    phy = physics.Physics()
    phy.addCutPair(physics.CutPair(region='crystal', cutValue=10))
    phy.addCutPair(physics.CutPair(region=c1.name, cutValue=10))

    simu = SimuApp(name=yml_filename, cam=camera1, phan=phantom, src=src1, digi=digi, phy=phy, randEngine=RandomEngine(),
                   dataOut=Root(fileName='test'))
    # print(simu.getMacStr())
    # simu.generateMacs()
    simu.generateYaml()
# if __name__ == "__main__":

#     f = open('simu1.yml', 'r')
#     simu = yaml.load(f)
#     simu.generateMacs()



def make_mac(config):
    with open(config) as fin:
        simu = yaml.load(fin)
        simu.generateMacs()
