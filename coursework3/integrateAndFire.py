import numpy as np
import matplotlib.pyplot as plt

#############
# Question 1
#############

ms = 0.001
s = 1


tauM = 10*ms
leakPotential = -70  #EL / Vr
voltageThreshold = -40  #Vt
membraneResistance = 10  #Rm
injectedCurrent = 3.1  #Ie


currentVoltage = leakPotential

#Tm dVdT = El - V + Rm Ie



voltageSamples = []
timeSample = 1*s
timeStep = 1*ms

for time in range(int(timeSample/timeStep)):
    voltageSamples.append(currentVoltage)
    dVdT = ((leakPotential - currentVoltage + (membraneResistance * injectedCurrent)) / tauM) * ms
    currentVoltage += dVdT
    print("current voltage: ", currentVoltage)
    print("dVdT: ", dVdT)
    if(currentVoltage > voltageThreshold):
        currentVoltage = leakPotential


xaxis = np.linspace(0, timeSample, timeSample/timeStep)
plt.plot(xaxis, voltageSamples, )


plt.savefig('fireAndIntegrate.png')
