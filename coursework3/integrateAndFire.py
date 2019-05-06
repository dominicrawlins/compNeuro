import numpy as np
import matplotlib.pyplot as plt
import random

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
    if(currentVoltage > voltageThreshold):
        currentVoltage = leakPotential


xaxis = np.linspace(0, timeSample, timeSample/timeStep)
plt.figure(num=None, figsize=(15,8))
plt.plot(xaxis, voltageSamples, label="Neuron")
plt.legend(loc='upper center', bbox_to_anchor=(0, 0.9, 0.15, 0.2), mode = "expand", shadow=False, ncol = 2, fontsize=14)
plt.xlabel("Time (s)", fontsize=14)
plt.ylabel("Membrane Potential (mV)", fontsize=14)
plt.xticks(np.arange(0, 1.1, 0.1), fontsize=12)
plt.yticks(fontsize=12)


plt.savefig('fireAndIntegrate.png')


############
#Question 2
############

ESyn = [0, -80]
fileNames = ["excitatorySynapses.png", "inhibitorySynapses.png"]

for q in range(2):
    tauM = 20*ms
    leakPotential = -70
    resetVoltage = -80
    voltageThreshold = -54
    RmIe = 18 #membrance resitance * injected current

    #synapses
    tauS = 10*ms
    maxStrength = 0.15 #gs
    P = 0.5


    #a) assume synapses are excitatory with Es = 0
    currentVoltage = []
    for i in range(2):
        currentVoltage.append(random.randint(resetVoltage, voltageThreshold))


    voltageSamples = np.zeros((int(timeSample/timeStep), 2))
    ISyn = np.zeros((2))
    dVdT = np.zeros((2))

    gsyn = 0.15

    s = [0,0]

    for time in range(int(timeSample/timeStep)):
        for i in range(2):
            voltageSamples[time][i] = currentVoltage[i]
            ISyn[i] = gsyn * s[abs(i-1)] * (ESyn[q] - currentVoltage[i])
            dVdT[i] = ((leakPotential - currentVoltage[i] + RmIe + ISyn[i]) / tauM) * ms
            currentVoltage[i] += dVdT[i]
            s[i] -= (s[i] * ms) / tauS
            if(currentVoltage[i] > voltageThreshold):
                currentVoltage[i] = resetVoltage
                s[i] += P

    plt.clf()
    xaxis = np.linspace(0, timeSample, timeSample/timeStep)
    plt.figure(num=None, figsize=(15,8))
    plt.plot(xaxis, voltageSamples[:, 0], label='Neuron A')
    plt.plot(xaxis, voltageSamples[:, 1], label='Neuron B')
    plt.legend(loc='upper center', bbox_to_anchor=(0, 0.9, 0.35, 0.2), mode = "expand", shadow=False, ncol = 2, fontsize=14)
    plt.xlabel("Time (s)", fontsize=14)
    plt.ylabel("Membrane Potential (mV)", fontsize=14)
    plt.xticks(np.arange(0, 1.1, 0.1), fontsize=12)
    plt.yticks(fontsize=12)


    plt.savefig(fileNames[q])
