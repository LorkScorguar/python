#!/usr/bin/python

import time

def init():
    tmax=0
    fichier=open('temps.txt','r')
    for ligne in fichier:
        tmp=ligne.strip().split(';')
        if int(tmp[len(tmp)-1]) > tmax:
            tmax=int(tmp[len(tmp)-1])    
    fichier.close()
    return tmax

def run(tmax):
    j=0
    k=0
    while k < tmax:
        fichier=open('temps.txt','r')
        m=1
        for ligne in fichier:
            tmp=ligne.strip().split(';')
            for i in range(len(tmp)):
                if tmp[i]==str(j):
                    print(tmp[i])
                    if i%2==0:
                        print("go "+str(m))
                    else:
                        print("stop "+str(m))
            m=m+1
        j=j+1
        k=k+1
        time.sleep(1)
        fichier.close()

tmax=init()
run(tmax)
