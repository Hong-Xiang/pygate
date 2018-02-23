from . import camera
from . import phantom 
from . import source
from . import digitizer
from . import physics
from . import geometry

from fs.osfs import OSFS
import os
import yaml

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
        fmt = (r"/gate/output/{0}/enable" + "\n"
               + r"/gate/output/{0}/setFileName  {1}" + "\n")
        return fmt.format(self.outType, self.fileName)


class FlagPair:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Root(DataOut):
    def __init__(self, fileName, flagList=[FlagPair('Hit', 0), FlagPair('Singles', 1), FlagPair('Coincidences', 1)]):
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


class Sino(DataOut):
    def __init__(self, fileName, inputDataName, tangCrystalBlurring=1.8, axialCrystalBlurring=1.8, radialBins=None, rawFlag='true', delayFlag=1, scatterFlag=1):
        super(Sino, self).__init__(outType='sinogram', fileName=fileName)
        self.inputDataName = inputDataName
        self.tangCrystalBlurring = tangCrystalBlurring
        self.axialCrystalBlurring = axialCrystalBlurring
        self.radialBins = radialBins
        self.rawFlag = rawFlag
        self.delayFlag = delayFlag
        self.scatterFlag = scatterFlag

    def getMacStr(self):
        mac = ''
        mac += super(Sino, self).getMacStr()
        fmt1 = r"/gate/output/sinogram/setTangCrystalBlurring {0} mm" + "\n"
        fmt2 = r"/gate/output/sinogram/setAxialCrystalBlurring {0} mm" + "\n"
        fmt3 = r"/gate/output/sinogram/RawOutputEnable true" + "\n"
        fmt4 = r"/gate/output/sinogram/StoreDelayeds" + "\n"
        fmt5 = r"/gate/output/sinogram/StoreScatters" + "\n"
        fmt6 = r"/gate/output/sinogram/setInputDataName {0}" + "\n"
        if self.tangCrystalBlurring is not None:
            mac += fmt1.format(self.tangCrystalBlurring)
        if self.axialCrystalBlurring is not None:
            mac += fmt2.format(self.axialCrystalBlurring)
        mac += fmt3.format()
        if self.delayFlag is not None:
            mac += fmt4.format()
        if self.scatterFlag is not None:
            mac += fmt5.format()
        mac += fmt6.format(self.inputDataName)
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
                 runTime=RunTime(), worldSize=geometry.Vec3(100, 100, 100), randEngine=RandomEngine()):
        self.name = name
        self.cam = cam
        self.phan = phan
        self.src = src
        self.digi = digi
        self.phy = phy
        self.dataOutList = []
        self.runTime = runTime
        self.worldSize = worldSize
        self.randEngine = randEngine

    def addDataout(self, item):
        if item is not None:
            self.dataOutList.append(item)

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
               + self.getComMac() + self.randEngine.getMacStr())
        for item in self.dataOutList:
            mac += item.getMacStr()
        mac += self.runTime.getMacStr() + startFmt
        return mac

    def generateYaml(self):
        with open(self.name + '.yml', 'w') as fout:
            yaml.dump(self, fout)

    def generateMacs(self):
        # currPath = os.getcwd()
        # if(os.path.exists("SimuMacs")):
        #     with OSFS('.') as fs:
        #         fs.removetree('SimuMacs')
                # os.rmdir('SimuMacs')
        # else:
        # if(not os.path.exists("SimuMacs")):
        #     os.mkdir('SimuMacs')
        # with open(os.getcwd() + '/SimuMacs/camera.mac', 'w') as file_object:
        #     file_object.write(self.cam.getMacStr())
        # file_object.close()
        subroot = ''
        # subroot = '/SimuMacs'
        file_object = open(os.getcwd() + subroot + '/camera.mac', 'w')
        file_object.write(self.cam.getMacStr())
        file_object.close()

        file_object = open(os.getcwd() + subroot + '/phantom.mac', 'w')
        file_object.write(self.phan.getMacStr())
        file_object.close()

        file_object = open(os.getcwd() + subroot + '/physics.mac', 'w')
        file_object.write(self.phy.getMacStr())
        file_object.close()

        file_object = open(os.getcwd() + subroot + '/digitizer.mac', 'w')
        file_object.write(self.digi.getMacStr())
        file_object.close()

        file_object = open(os.getcwd() + subroot + '/source.mac', 'w')
        file_object.write(self.src.getMacStr())
        file_object.close()

        file_object = open(os.getcwd() + subroot + '/main.mac', 'w')
        file_object.write(self.getMacStr())
        file_object.close()


# if __name__ == '__main__':


class MacMaker:
    @classmethod
    def make_mac(cls, config):
        if not isinstance(config, (list, tuple)):
            config = [config]
        for f in config:
            with open(f) as fin:
                simu = yaml.load(fin)
                simu.generateMacs()

    @classmethod
    def make_yml(cls, yml_filename):
        # Camera
        # c1 = geometry.Cylinder(name='ecat', Rmax=85,
        #                        Rmin=59, Height=10, material='Air')
        # # print (b1.getMacStr())
        # b1 = geometry.Box(name='block', position=geometry.Vec3(
        #     69.0, 0.0, 0.0), size=geometry.Vec3(20, 30, 3), material='Air')
        # b2 = geometry.Box(name='crystal', size=geometry.Vec3(
        #     20, 1, 1), material='LYSO')
        # c1.addChild(b1)
        # b1.addChild(b2)
        # cbr1 = geometry.RingRepeater(volume=b1.name, number=10)
        # cbr2 = geometry.CubicRepeater(volume=b2.name, scale=geometry.Vec3(
        #     1, 30, 3), repeatVector=geometry.Vec3(0, 1, 1))
        # sys = camera.Ecat()
        # sys.attachSystem(itemList=[b1.name, b2.name])

        # # create the camera and construt it
        # camera1 = camera.Camera(name='cam1', system=sys)
        # camera1.addGeo(c1)
        # camera1.addGeo(cbr2)
        # camera1.addGeo(cbr1)
        # camera1.addCrystalSD(b2.name)

        # HRRT
        hrrt_c1 = geometry.Cylinder(
            name='cylindricalPET', Rmax=254.5, Rmin=234.5, Height=253.5, material='Air')
        hrrt_head = geometry.Box(name='block', position=geometry.Vec3(
            244.5, 0, 0), size=geometry.Vec3(20, 175.68, 253.5), material='Air')
        hrrt_module = geometry.Box(name='module', position=geometry.Vec3(
            0, 0, 0), size=geometry.Vec3(20, 19, 19), material='Air')
        hrrt_crystal = geometry.Box(name='crystal', position=geometry.Vec3(
            0, 0, 0), size=geometry.Vec3(20, 2, 2), material='LYSO')

        hrrt_c1.addChild(hrrt_head)
        hrrt_head.addChild(hrrt_module)
        hrrt_module.addChild(hrrt_crystal)

        hrrt_cbr2 = geometry.CubicRepeater(volume=hrrt_crystal.name, scale=geometry.Vec3(
            1, 8, 8), repeatVector=geometry.Vec3(0, 2.375, 2.375))
        hrrt_cbr1 = geometry.CubicRepeater(volume=hrrt_module.name, scale=geometry.Vec3(
            1, 9, 13), repeatVector=geometry.Vec3(0, 19.52, 19.52))
        hrrt_rr = geometry.RingRepeater(volume=hrrt_head.name, number=8)

        sys = camera.CylindericalPET()
        sys.attachSystem(itemList=['block', 'module', 'void', 'crystal'])
        camera1 = camera.Camera(name='cam1', system=sys)
        camera1.addGeo(hrrt_c1)
        camera1.addGeo(hrrt_cbr2)
        camera1.addGeo(hrrt_cbr1)
        camera1.addGeo(hrrt_rr)
        camera1.addCrystalSD(hrrt_crystal.name)
        ############################################################

        # phantom
        # c1 = geometry.Cylinder(
        #     mother='world', name='NEMACylinder', Rmax=82, Rmin=56, Height=5)
        # # print (b1.getMacStr())
        # # b1 = geometry.Box(mother=c1.name, name='', position=geometry.Vec3(
        # #     66.5, 0.0, 0.0), size=geometry.Vec3(20, 44, 5))
        # # c1.addChild(b1)

        # phantom = phantomModule.Phantom(name='phantom1')
        # phantom.addGeo(c1)
        # phantom.addPhantomSD(b1)

        pv1 = geometry.ImageRegularParamerisedVolume(
            mother='world', name='hof_heart', imagefile='heart_atn_phantom.h33', rangefile='range_atten_brain.dat', position=geometry.Vec3(0, 0, 0))
        phantom1 = phantom.Phantom(name='phantom1')
        phantom1.addGeo(pv1)
        phantom1.addPhantomSD(pv1)

        ##################################################

        # source
        src1 = source.VoxelizedSrcItem(name='voxel_heart')
        src1.addSrcModule(source.Voxelized(readtable='activity_range_brain.dat',
                                           readfile='heart_act_phantom.h33', position=geometry.Vec3(-38.4, -38.4, -0.15)))
        #src1 = source.SrcItem(name='src1')
        src1.addSrcModule(source.Particle(paticleType='gamma'))
        src1.addSrcModule(source.Angular(ang=[90, 90, 0, 360]))
        # src1.addSrcModule(Rectangle(halfSize = [10,20]))
        # src1.addSrcModule(source.Cylinder(
        #     dimension='Volume', halfz=10, radius=10))
        # src1.addSrcModule(source.Placement(
        #     placement=geometry.Vec3(10, 10, 10)))

        src = source.Source()
        src.addSourceItem(src1)
        ##################################################

        # digitizer
        sc = digitizer.SingleChain()
        a = digitizer.Adder()
        r = digitizer.Readout(depth=1)
        sc.addModule(a)
        sc.addModule(r)
        sc.addModule(digitizer.Blurring(res=0.10, eor=511))
        # sc.addModule(digitizer.CrystalBlurring())
        sc.addModule(digitizer.ThresHolder(holdvalue=250))
        sc.addModule(digitizer.UpHolder(holdvalue=750))
        # sc.addModule(digitizer.TimeResolution())
        # sc.addModule(digitizer.SpBlurring())
        sc.addModule(digitizer.DeadTime(dtVolume='block', deadtime=3000))
        coin1 = digitizer.CoinSorter(window=10, offset=0)
        coin2 = digitizer.CoinSorter(name='delay', window=10, offset=500)
        conichain1 = digitizer.CoinChain(
            name='finalcoin', inputList=[coin1.name, coin2.name], usePriority='true')
        # conichain1.addModule(digitizer.DeadTime(dtVolume='crystal'))
        # conichain1.addModule(digitizer.Buffer())
        digi = digitizer.Digitizer()
        digi.addModule(sc)
        digi.addModule(coin1)
        digi.addModule(coin2)
        digi.addModule(conichain1)
        #####################################################

        # physics
        phy = physics.Physics()
        phy.addCutPair(physics.CutPair(region='crystal', cutValue=0.1))
        phy.addCutPair(physics.CutPair(region=pv1.name, cutValue=0.1))
        phy.addMaxStep(physics.MaxStep(region=pv1.name, maxstepsize=0.01))

        simu = SimuApp(name=yml_filename, cam=camera1, phan=phantom1,
                       src=src, digi=digi, phy=phy, randEngine=RandomEngine())

        dataout1 = Root(fileName='testroot')
        dataout2 = Sino(fileName='testsino', inputDataName='finalcoin')

        simu.addDataout(dataout1)
        simu.addDataout(dataout2)
        # print(simu.getMacStr())
        # simu.generateMacs()
        simu.generateYaml()




if __name__ == '__main__':
    MacMaker.make_yml('test')

