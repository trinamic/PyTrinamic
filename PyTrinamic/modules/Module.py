# Created on: 09.08.2019
# Author: LK

from PyTrinamic.features.Feature import Feature
from PyTrinamic.features.FeatureProvider import FeatureProvider
from PyTrinamic.ic.IC import IC

class Module(object):
    def __init__(self, moduleId=1, connection=None, parent=None, submodules=[]):
        self.__motors = []
        self.__moduleId = moduleId
        self.__submodules = []
        self.__connection = connection
        self.__parent = parent
        if(parent):
            self.__connection = parent.getConnection()
        for submodule in submodules:
            self.addSubmodule(submodule)
    def setConnection(self, connection):
        self.__connection = connection
    def setModuleId(self, moduleId):
        self.__moduleId = moduleId
    def getConnection(self):
        return self.__connection
    def getModuleId(self):
        return self.__moduleId
    def addSubmodule(self, submodule):
        if(isinstance(submodule, Module) or isinstance(submodule, IC)):
            self.__submodules.append(submodule)
        else:
            self.__submodules.append(submodule(parent=self))
    def removeSubmodule(self, submodule):
        self.__submodules.remove(submodule)
    def getSubmodules(self):
        return self.__submodules
    def addMotor(self, motor):
        for feature in [f for f in self.__class__.__mro__ if ((self.__class__ != f) and isinstance(f(), Feature) and not isinstance(f(), FeatureProvider))]:
            motor.addFeatureProvider(feature, self, 0, len(self.__motors)) # If new motor gets added, len(self.__motors) increases
        self.__motors.append(motor)
        if(self.__parent):
            self.__parent.addMotor(motor)
    def removeMotor(self, motor):
        self.__motors.remove(motor)
        if(self.__parent):
            self.__parent.removeMotor(motor)
        for i, motor in enumerate(self.__motors):
            motor.setProviderIndex(self, i)
    def getMotors(self):
        return self.__motors
    def hasFeature(self, feature, recursive=False):
        if(isinstance(self, feature)):
            return True
        elif(recursive):
            for submodule in self.getSubmodules():
                if submodule.hasFeature(feature, recursive):
                    return True
        return False
    def hasSubmodule(self, submodule, recursive=False):
        del recursive
        return (submodule in self.getSubmodules())
    def axisParameter(self, strParameter):
        raise NotImplementedError()
    def getAxisParameter(self, commandType, axis, signed=False):
        return self.getConnection().getAxisParameter(commandType, axis, self.getModuleId(), signed)
    def setAxisParameter(self, commandType, axis, value):
        return self.getConnection().setAxisParameter(commandType, axis, value, self.getModuleId())
