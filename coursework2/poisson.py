import random as rnd
import matplotlib.pyplot as plt
import numpy as np
import math

def get_spike_train(rate,big_t,tau_ref):

    if 1<=rate*tau_ref:
        print("firing rate not possible given refractory period f/p")
        return []


    exp_rate=rate/(1-tau_ref*rate)

    spike_train=[]

    t=rnd.expovariate(exp_rate)

    while t< big_t:
        spike_train.append(t)
        t+=tau_ref+rnd.expovariate(exp_rate)

    return spike_train



def fanoFactor(spikeTrain, timePeriod, totalTime):
    numberOfBins = int(totalTime/timePeriod)
    spikePeriodBins = [0]*numberOfBins
    for spike in spikeTrain:
        binNumber = spike  // timePeriod
        spikePeriodBins[int(binNumber)] += 1

    mean = len(spikeTrain) / numberOfBins

    varianceSum = 0
    for bin in spikePeriodBins:
        varianceSum  += (bin - mean) ** 2

    variance = varianceSum / numberOfBins
    fanoFactorReturn = variance / mean

    return fanoFactorReturn

def calcInterspikeIntervals(spikeTrain):
    intervals = []
    for intervalNumber in range(1, len(spikeTrain)):
        interval = spikeTrain[intervalNumber] - spikeTrain[intervalNumber - 1]
        intervals.append(interval)
    return intervals

def calculateCV(intervals):
    cvMean = sum(intervals)/len(intervals)

    cvVarianceSum = 0
    for i in range(len(intervals)):
        cvVarianceSum += (intervals[i] - cvMean) ** 2
    cvVariance = cvVarianceSum / len(intervals)

    CV = math.sqrt(cvVariance)/cvMean
    return CV




Hz=1.0
sec=1.0
ms=0.001

rate=15.0 *Hz
tau_ref=5*ms

big_t=5*sec

spike_train=get_spike_train(rate,big_t,tau_ref)

#print(len(spike_train)/big_t)

#print(spike_train)
firingRate = 35
refractoryPeriods = [0, 5]
fanoFactorWindows = [10, 50, 100]
time = 1000*sec

print("----------------------\n\nQuestion 1\n\n------------------------\n")



for refractoryPeriod in refractoryPeriods:
    for fanoFactorWindow in fanoFactorWindows:
        tau = refractoryPeriod * ms
        spikeTrain = get_spike_train(firingRate, time, tau)
        window = fanoFactorWindow * ms
        fanoFactorResult = fanoFactor(spikeTrain, window, time)
        print("Refractory Period: ", refractoryPeriod)
        print("Window: ", window)
        print("Fano Factor: ", fanoFactorResult)

        interspikeIntervals = calcInterspikeIntervals(spikeTrain)
        CV = calculateCV(interspikeIntervals)

        print("Coefficient of Variation:", CV, "\n")


print("\n\n----------------------\n\nQuestion 2\n\n------------------------\n")

def load_data(filename,T):

    data_array = [T(line.strip()) for line in open(filename, 'r')]

    return data_array


#spikes=[int(x) for x in load_data("rho.dat")]
spikes=load_data("rho.dat",int)

spikeTrain = []

for idx, spike in enumerate(spikes):
    if(spike == 1):
        spikeTrain.append(idx*2*ms)

spikeIntervals = calcInterspikeIntervals(spikeTrain)
CV = calculateCV(spikeIntervals)
print("Coefficient of Variation:", CV)

for fanoFactorWindow in fanoFactorWindows:
    fanoFactorResult = fanoFactor(spikeTrain, fanoFactorWindow*ms, 20*60)
    print("Fano Factor for ", fanoFactorWindow*ms, "ms: ", fanoFactorResult)



print("\n\n----------------------\n\nQuestion 3\n\n------------------------\n")

#stimulus=[float(x) for x in load_data("stim.dat")]
stimulus=load_data("stim.dat",float)

averages=[]
totalTime = 20*60
windowTime = 100*ms
totalWindows =  totalTime / windowTime/2
for window in range(int(totalWindows)):
    spikeStimulus = []
    start = window * 50
    length = 50
    for indiSpike in range(length):
        if(spikes[indiSpike + start] == 1):
            spikeStimulus.append(stimulus[indiSpike + start])
    if(len(spikeStimulus) == 0):
        averages.append(0)
    else:
        averageStimulus = sum(spikeStimulus)/ len(spikeStimulus)
        averages.append(averageStimulus)

xaxis = np.linspace(0, totalTime, totalWindows)
plt.plot(xaxis, averages, )

plt.savefig('averageStimulus.png')
