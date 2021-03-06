#!/usr/bin/env python3
'''
Turn a motor without feedback in open loop mode

Created on 08.01.2021

@author: ED
'''

import PyTrinamic, time
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.referencedesigns.TMC4671_LEV.TMC4671_LEV_REF import TMC4671_LEV_REF

PyTrinamic.showInfo()

" please select your CAN adapter "
#myInterface = ConnectionManager("--interface pcan_tmcl").connect()
myInterface = ConnectionManager("--interface kvaser_tmcl").connect()

module = TMC4671_LEV_REF(myInterface)
module.showModuleInfo()
motor = module.motor(0)

"""
    Define all motor configurations for the TMC4671-LEV-REF.

    The configuration is based on our standard BLDC motor (QBL4208-61-04-013-1024-AT).
    If you use a different motor be sure you have the right configuration setup otherwise the script may not work.
"""

" motor configuration "
motor.setMotorPolePairs(4)
motor.setMaxTorque(2000)
motor.showConfiguration()

" open loop configuration "
motor.openLoop.setOpenLoopTorque(1000)
motor.openLoop.showConfiguration()

" motion settings "
motor.linearRamp.setMaxVelocity(2000)
motor.linearRamp.setAcceleration(1000)
motor.linearRamp.setRampEnabled(1)
motor.linearRamp.showConfiguration()

" set commutation mode to open loop "
motor.commutationSelection.setMode(motor.ENUM.COMM_MODE_OPENLOOP)
motor.commutationSelection.showConfiguration()

print("Starting motor...")
motor.rotate(1000)
time.sleep(3);

print("Changing motor direction...")
motor.rotate(-1000)
time.sleep(6);

print("Stopping motor...")
motor.rotate(0)
time.sleep(3);

" power of "
motor.commutationSelection.setMode(motor.ENUM.COMM_MODE_DISABLED)

myInterface.close()
print("\nReady.")
