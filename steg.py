import sys
import os
from PIL import Image
import platform 
import getopt
from encryptor import Encryptor
import base64
from base64 import decodestring

encoding = "utf-8"

platform = platform.system()

def usage():
    print("[???] Usage: python3 steg.py PathToImage Message PathToOutFile")
    print("[???] Example: python3 steg.py myImage.png \"This is a secret message\" outFile.png")
    print("[???] Remember to place your message in \" \" if it is more than one word")
    print()
    print("[1] Go to helper\n")
    print("[2] Exit\n")
    option = input("Enter your option: ")
    
    if option == '1':
        helper()
    elif option == '2':
        print("Goodbye!\n")
        sys.exit(0)
    else:
        clearScreen()
        print()
        print("[!!!] Sorry Your Option Was Not Recognized!\n")
        usage()

def mesToBinary(message):
    
    global encoding

    binary = []

    for i in message:
        binary.append(format(ord(i), '08b'))

    return binary

def fileToBinaryString(binary):

    binaryString = []

    for i in binary:
        binaryString.append(format(ord(i), '08b'))
    return binaryString

def getPixelData(image):
   
    pixels = list(image.getdata())
    width, height = image.size

    return pixels, width, height

def modifyPixel(pixel, message):
  
    data = message
    lenData = len(data)
    imageData = iter(pixel)
    print(lenData)
    print(data[0][0])
    for i in range(lenData):

        #Extract 3 pixels at a time
        pixel = [value for value in imageData.__next__()[:3] + imageData.__next__()[:3] + imageData.__next__()[:3]]

        #Value is 1 for odd and 0 for even

        for j in range(0,8):
            if (data[i][j]=='0') and (pixel[j]% 2 != 0):

                if(pixel[j] % 2 != 0):
                    pixel[j] -= 1
            elif(data[i][j] == '1') and (pixel[j] % 2 == 0):
                pixel[j] -= 1

        #Eith pixel of each set tells whether or not there is more of the
        # messge, this idea was stolen from geeksforgeeks

        if (i == lenData - 1):
            if(pixel[-1] % 2 == 0):
                pixel[-1] -= 1
        else:
            if(pixel[-1] % 2 != 0):
                pixel[-1] -= 1

        pixel = tuple(pixel)
        yield pixel[0:3]
        yield pixel[3:6]
        yield pixel[6:9]


def writeImage(image, data, totalPixels):
    width = image.size[0]
    (x,y) = (0,0)
    pixelsWritten = 0

    for pixel in modifyPixel(image.getdata(),data):

        image.putpixel((x,y),pixel)
        if(x == width -1):
            x = 0
            y+=1
        else:
            x+=1
        pixelsWritten+=1
        print("%d out of %d pixels written" % (pixelsWritten, totalPixels))
        clearScreen()
 
    print("%d out of %d total pixels were modified" % (pixelsWritten, totalPixels))

def encode(imgPath, message, outFile):

    image = Image.open(imgPath)

    pixels, width, height = getPixelData(image)

    outImg = image.copy()
    
    message = mesToBinary(message)
    writeImage(outImg,message, len(pixels))
    
    outImg.save(outFile, str(outFile.split(".")[1].upper()))

def decode(imgPath):

    image = Image.open(imgPath,'r')
    data = ''
    imageData = iter(image.getdata())

    while(True):
        pixels = [value for value in imageData.__next__()[:3] + imageData.__next__()[:3] + imageData.__next__()[:3]]

        #binary string
        binString = ''
        
        for i in pixels[:8]:
            if (i % 2 == 0):
                binString += '0'
            else: 
                binString += '1'

        data += chr(int(binString,2))
        if (pixels[-1]% 2 != 0):
            #return data
            break

    return data

def encodeFile(imgPath,inputFile,outFile):
    image = Image.open(imgPath)

    pixels, width, height = getPixelData(image)

    outImg = image.copy()

    with open(inputFile,mode='rb') as file:
        encodingString = base64.b64encode(file.read())

    binary = mesToBinary(encodingString.decode())
    writeImage(outImg,binary, len(pixels))
    
    outImg.save(outFile, str(outFile.split(".")[1].upper()))

def decodeFile(imgPath,outFile):
    
    image = Image.open(imgPath,'r')
    data = ''
    imageData = iter(image.getdata())
    while(True):
        pixels = [value for value in imageData.__next__()[:3] + imageData.__next__()[:3] + imageData.__next__()[:3]]

        #binary string
        binString = ''
        
        for i in pixels[:8]:
            if (i % 2 == 0):
                binString += '0'
            else: 
                binString += '1'

        data += chr(int(binString,2))
        if (pixels[-1]% 2 != 0):
            #return data
            break
   
    with open(outFile, 'wb') as file:
        file.write(decodestring(data.encode()))


def helper():
    clearScreen()

    print("[---] Welcome To Image Encryptor Helper [---]\n\n")
    print("[1] Help\n")
    print("[2] Encrypt Image\n")
    print("[3] Decrypt Image\n")
    print("[4] Encrypt File Inside Image\n")
    print("[5] Decrypt File Inside Image\n")
    print("[6] Exit\n")

    option = input("Enter your Option:")
    
    if option == '1':
        clearScreen()
        usage()
    elif option == '2':
        imgPath = input("Enter the file path to the image: ")
        print()
        message = input("Enter the message you want to encrypt: ")
        print()
        outFile = input("Enter the name of the resulting image: ")

        encode(imgPath,message,outFile)
    elif option == '3':
        imgPath =input("Enter the file path to the image you want to decrypt: ")
        print(decode(imgPath))
    elif option == '4':
        imgPath = input("Enter the file path to the image: ")
        print()
        inputFile = input("Enter the file path to the file: ")
        print()
        outFile = input("Enter the name of the resulting image: ")
    
        encodeFile(imgPath,inputFile,outFile)
    elif option == '5':
        imgPath =input("Enter the file path to the image you want to decrypt: ")
        print()
        outFile = input("Enter the file path to the outfile you want to create: ")
    
        decodeFile(imgPath,outFile)
    elif option == '6':
        print("Goodbye!\n")
        sys.exit(0)
    else:
        clearScreen()
        print("Sorry That Option Was Not Recognized Try Again\n")
        helper()

def clearScreen():
    if platform == "Linux":
        os.system('clear')
    elif platform == "Windows":
        os.system('cls')
    else:
        print("\n")
     

def main():

    if len(sys.argv) == 1:
        helper()
    elif len(sys.argv) > 3:
        imgPath = sys.argv[1]
        message = sys.argv[2]
        outFile = sys.argv[3]
        encode(imgPath,message,outFile)
    elif len(sys.argv) == 2:
        imgPath = sys.argv[1]
        print(decode(imgPath))
    else:
        print("else")
        usage()

main()
