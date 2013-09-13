#!/usr/bin/python3.2

import time
import random

# Learning rate:
# Lower  = slower
# Higher = less precise
rate=.2

# Create random weights
inWeight=[random.uniform(0, 1), random.uniform(0, 1)]

# Start neuron with no stimuli
inNeuron=[0.0, 0.0]

# Learning table (or gate)
learningTable =[[0.0, 0.0, 0.0]]
learningTable+=[[0.0, 1.0, 1.0]]
learningTable+=[[1.0, 0.0, 1.0]]
learningTable+=[[1.0, 1.0, 1.0]]

testTable =[[0, 0]]
testTable+=[[0, 1]]
testTable+=[[1, 0]]
testTable+=[[1, 1]]

# Calculate response from neural input
def outNeuron(midThresh):
    global inNeuron, inWeight
    s=inNeuron[0]*inWeight[0] + inNeuron[1]*inWeight[1]
    if s>midThresh:
        return 1.0
    else:
        return 0.0

# Display results of learningTable
def display(out, real):
        if out == real:
            print(str(out)+" should be "+str(real)+" ***")
        else:
            print(str(out)+" should be "+str(real))

def learn(learningTable):
    g=0
    while g<50:
        # Loop through each lesson in the learning table
        for i in range(len(learningTable)):
            # Stimulate neurons with learningTable input
            inNeuron[0]=learningTable[i][0]
            inNeuron[1]=learningTable[i][1]
            # Adjust weight of neuron #1
            # based on feedback, then display
            out = outNeuron(2)
            inWeight[0]+=rate*(learningTable[i][2]-out)
            #display(out, learningTable[i][2])
            # Adjust weight of neuron #2
            # based on feedback, then display
            out = outNeuron(2)
            inWeight[1]+=rate*(learningTable[i][2]-out)
            #display(out, learningTable[i][2])
            # Delay
            #time.sleep(1)
        g=g+1

def test(testTable):
    print("Resultats")
    for i in range(len(testTable)):
        inNeuron[0]=testTable[i][0]
        inNeuron[1]=testTable[i][1]
        out = outNeuron(2)
        print(out)
#        time.sleep(1)                                

learn(learningTable)
test(testTable)
