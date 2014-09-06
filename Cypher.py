import base64

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

def fileToText(fileName):#transform file content to string
	text=""
	file=open(fileName,"r")
	for line in file:
		text+=line
	return text

def textToFile(text,fileName):#put string into file
	file=open(fileName,"w")
	file.write(text)
	file.close()

def encode64(text):
	encoded=base64.b64encode(bytes(text,'utf-8'))
	return encoded.decode()

def decode64(encoded):
	text=base64.b64decode(encoded)
	return text.decode()

def crypt(text,key):
	ghost=""
	#vigenere
	#base64
	#vigenere
	#base64
	a=vigenere(text,key,1)
	b=encode64(a)
	c=vigenere(b,key,1)
	ghost=encode64(c)
	return ghost

def decrypt(ghost,key):
	text=""
	a=decode64(ghost)
	b=vigenere(a,key,2)
	c=decode64(b)
	text=vigenere(c,key,2)
	return text

"""
example with some text::
a=crypt("text","key")
print(a)
b=decrypt(a,"key")
print(b)
"""
example with a file:
a=fileToText("fileName.ext")
b=crypt(a,"key")
textToFile(b,"fileNameCrypt.ext")

a=fileToText("fileNameCrypt.ext")
b=decrypt(a)
textToFile(b,"newFile.ext")
"""
