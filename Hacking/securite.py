import time
import re
import math


def gcd(a, b):
    # Return the GCD of a and b using Euclid's Algorithm
    while a != 0:
        a, b = b % a, a
    return b

def findModInverse(a, m):
    # Returns the modular inverse of a % m, which is
    # the number x such that a*x % m = 1
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def caesar(mode,message,key):
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    translated = ''
    message = message.upper()
    for symbol in message:
        if symbol in LETTERS:
            num = LETTERS.find(symbol) # get the number of the symbol
            if mode == 'encrypt':
                num = num + key
            elif mode == 'decrypt':
                num = num - key
            if num >= len(LETTERS):
                num = num - len(LETTERS)
            elif num < 0:
                num = num + len(LETTERS)
            translated = translated + LETTERS[num]
        else:
            translated = translated + symbol
    return translated.lower()


def caesarBruteForce(message):
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    rep=""
    bestRep=[]
    max=0
    clef=0
    valide=False
    for key in range(len(LETTERS)):
        find=0
        translated = ''
        for symbol in message.upper():
            if symbol in LETTERS:
                num = LETTERS.find(symbol) # get the number of the symbol
                num = num - key
                if num < 0:
                    num = num + len(LETTERS)
                translated = translated + LETTERS[num]
            else:
                translated = translated + symbol
        translated=translated.lower().strip()
        translated=re.sub("\W"," ",translated)
        translated=re.sub("\s+"," ",translated)
        lmot=translated.split(" ")
        for mot in lmot:
            dico=open("dico-fr.txt","r")
            for mo in dico:
                if mot.strip()==mo.strip():
                    find=find+1
                    break
            dico.close()
        if find > max:
            max=find
            clef=key
            bestRep=[translated]
        elif find >=max:
            max=find
            bestRep.append(translated)
        if find==len(lmot):
            rep=translated
            clef=key
            valide=True
            break
        else:
            valide=False
            rep=str(bestRep)
    return rep,clef,valide

def transposition(mode,message,key):
    rep=""
    if mode == "encrypt":
        ciphertext = [''] * key
        for col in range(key):
            pointer = col
            while pointer < len(message):
                ciphertext[col] += message[pointer]
                pointer += key
        rep=''.join(ciphertext)
    else:
        numOfColumns = math.ceil(len(message) / key)
        numOfRows=key
        numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)
        plaintext = [''] * numOfColumns
        col=0
        row=0
        for symbol in message:
            plaintext[col] += symbol
            col += 1 
            if (col == numOfColumns) or (col == numOfColumns - 1 and row >=numOfRows - numOfShadedBoxes):
                col = 0
                row += 1
        rep=''.join(plaintext)
    return rep

def transpositionBruteForce(message):
    valide=False
    rep=""
    bestRep=[]
    max=0
    clef=0
    for key in range(1, len(message)):
        find=False
        translated = transposition("decrypt",message,key)
        translated=translated.lower().strip()
        translated=re.sub("\W"," ",translated)
        translated=re.sub("\s+"," ",translated)
        lmot=translated.split(" ")
        for mot in lmot:
            dico=open("dico-fr.txt","r")
            for mo in dico:
                if mot.strip()==mo.strip():
                    find=find+1
                    break
            dico.close()
        if find > max:
            max=find
            clef=key
            bestRep=[translated]
        elif find >=max:
            max=find
            bestRep.append(translated)
        if find==len(lmot):
            rep=translated
            clef=key
            valide=True
            break
        else:
            valide=False
            rep=str(bestRep)
    return rep,clef,valide


SYMBOLS = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""


def getKeyParts(key):
    keyA = key // len(SYMBOLS)
    keyB = key % len(SYMBOLS)
    return (keyA, keyB)

def checkKeys(keyA, keyB, mode):
    if (keyA == 1 or keyB == 0) and mode == 'encrypt':
        print("The affine cipher will be weak. It won't encrypt it")
        quit(0)
    if keyA < 0 or keyB < 0 or keyB > len(SYMBOLS) - 1:
        print('Key A must be greater than 0 and Key B must be between 0 and %s.' % (len(SYMBOLS) - 1))
        quit(0)
    if gcd(keyA, len(SYMBOLS)) != 1:
        print('Key A (%s) and the symbol set size (%s) are not relatively prime. Choose a different key.' % (keyA, len(SYMBOLS)))
        quit(0)

def affineCipher(mode,message,key):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, mode)
    rep = ""
    modInverseOfKeyA = findModInverse(keyA, len(SYMBOLS))
    for symbol in message:
        if symbol in SYMBOLS:
            symIndex = SYMBOLS.find(symbol)
            if mode=="encrypt":
                rep += SYMBOLS[(symIndex * keyA + keyB) % len(SYMBOLS)]
            else:
                rep += SYMBOLS[(symIndex - keyB) * modInverseOfKeyA % len(SYMBOLS)] 
        else:
            rep += symbol # just append this symbol unencrypted
    return rep

def affineCipherBruteForce(message):
    return ""

def estimeTemps(algo,message):
    temps=0
    message=message.lower().strip()
    message=re.sub("\W"," ",message)
    message=re.sub("\s+"," ",message)
    lmot=message.split(" ")
    if algo=="caesar":
        temps=len(lmot)*2.5
    elif algo=="transposition":
        temps=len(lmot)*2
    elif algo=="affineCipher":
        temps=0
    return temps

def testHack(message):
    listeAlgo=["caesar","transposition","affineCipher"]
    for algo in listeAlgo:
        temps=estimeTemps(algo,cache)
        print("Temps estimé pour test avec "+algo+":"+str(temps)+"sec")
        depart=time.clock()
        fct=algo+"BruteForce(cache)"
        hack,key,valide=eval(fct)
        fin=time.clock()
        if valide:
            break
        else:
            print("Echec avec "+algo+" en "+str(math.floor(fin-depart))+"sec")
            continue
    print("\n========================\nPar brute force("+str(math.floor(fin-depart))+"sec):"+hack+"\nen utilisant "+algo+" avec la clef: "+str(key)+"\n========================\n")
    
message="comment ça va"
#cache=caesar("encrypt",message,3)
#testHack(cache)
