import base64
import math
import re
import time

#RESOURCES
SYMBOLS = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nonLettersOrSpacePattern = re.compile('[^A-Z\s]')

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

def genPrimes(n):
    """Generates all primes less than n."""
    if n <= 2: return
    yield 2
    F = [True] * n
    seq1 = range(3, int(math.sqrt(n)) + 1, 2)
    seq2 = range(seq1[-1] + 2, n, 2)
    for p in filter(F.__getitem__, seq1):
        yield p
        for q in range(p * p, n, 2 * p):
            F[q] = False
    for p in filter(F.__getitem__, seq2):
        yield p
            
#CAESAR CIPHER:key is a number like 0 < key < 25
def caesar(mode,message,key):
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
    rep=""
    bestRep=[]
    max=0
    clef=0
    valide=False
    mlen=len(message.split(" "))
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
        elif find >= max:
            max=find
            bestRep.append(translated)
        if find==len(lmot):
            rep=translated
            clef=key
            valide=True
            break
        elif find==mlen:#count words number using only space separator
            rep=translated
            clef=key
            valide=True
            break
        else:
            valide=False
            rep=str(bestRep)
    return rep,clef,valide

#TRANSPOSITION CIPHER: key is a number
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
    mlen=len(message.split(" "))
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
        elif find==mlen:#count words number using only space separator
            rep=translated
            clef=key
            valide=True
            break
        else:
            valide=False
            rep=str(bestRep)
    return rep,clef,valide

#AFFINE CIPHER: key is a number > len(SYMBOLS), not X x len(SYMBOLS)
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
    valide=False
    rep=""
    bestRep=[]
    max=0
    clef=0
    mlen=len(message.split(" "))
    for key in range(len(SYMBOLS) ** 2):
        print(key)
        find=False
        keyA = getKeyParts(key)[0]
        if gcd(keyA, len(SYMBOLS)) != 1:
            continue
        decryptedText = affineCipher("decrypt",message, key)
        translated=decryptedText.lower().strip()
        translated=re.sub("\W"," ",translated)
        translated=re.sub("\s+"," ",translated)
        if re.search("[a-z]{2}",translated):# si pas plus de 2lettres alors il n'y a pas de mots donc ça ne doit pas être bon
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
            elif find==mlen:#count words number using only space separator
                rep=translated
                clef=key
                valide=True
                break
            else:
                valide=False
                rep=str(bestRep)
    return rep,clef,valide

#Vigenere
def vigenere(text,key,operation):
    #1=crypt 2=decrypt
    sortie, i = "", 0
    for caract in text:
        if operation == 1:    #crypt
            sortie = sortie + chr((ord(caract) + ord(key[i])) % 256)
            i = i + 1
            if i > len(key) - 1:
                i = 0
        elif operation == 2:  #decrypt
            sortie = sortie + chr((ord(caract) - ord(key[i])) % 256)
            i = i + 1
            if i > len(key) - 1:
                i = 0
    return sortie


#FREQUENCY ANALYSIS
letterFreq={'e':14.72, 's':7.95, 'a':7.63, 'i':7.53,'t':7.24,'n':7.1,'r':6.55,'u':6.31,'l':5.46,'o':5.38,'d':3.67,'c':3.26,'p':3.02,'m':2.97,'é':1.90,'v':1.63,'q':1.36,'f':1.07,'b':0.90,'g':0.87,'h':0.74,'j':0.55,'à':0.49,'x':0.39,'y':0.31,'è':0.27,'ê':0.23,'z':0.14,'w':0.11,'ç':0.09,'ù':0.06,'k':0.05,'î':0.04,'œ':0.02,'ï':0.01,'ë':0}
lforder="esaitnrulodcpmévqfbghjàxyèêzwçùkîœïë"
import operator

def analyseFreq(message):
    rep=""
    lettreCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    for lettre in message:
        if lettre.upper() in LETTERS:
            lettreCount[lettre.upper()] += 1
    lettreCountSort=sorted(lettreCount, key=lettreCount.get, reverse=True)
    print(lettreCountSort)
    for lettre in message:
        if lettre.upper() in LETTERS:
            it=lettreCountSort.index(lettre.upper())
            rep+=lforder[it]
        else:
            rep+=lettre
    return rep

#OTHER FUNCTIONS
def estimeTemps(algo,message):
    temps=0
    unite="sec"
    message=message.lower().strip()
    message=re.sub("\W"," ",message)
    message=re.sub("\s+"," ",message)
    lmot=message.split(" ")
    if algo=="caesar":
        temps=len(lmot)*3
    elif algo=="transposition":
        temps=len(lmot)*2.5
    elif algo=="affineCipher":
        temps=0
        pos=0
        for numb in genPrimes(len(SYMBOLS)):
            pos+=1
        temps=pos*len(SYMBOLS)
    return temps,unite

def testHack(message):
    listeAlgo=["caesar","transposition","affineCipher"]
    for algo in listeAlgo:
        temps,unite=estimeTemps(algo,cache)
        print("Temps estimé pour test avec "+algo+":"+str(temps)+unite)
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

message="salut, c'est florent"
cache=affineCipher("encrypt",message,778)
print(cache)
testHack(cache)
