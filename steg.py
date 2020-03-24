import sys
import os
from PIL import Image
import platform 
import getopt

encoding = "UTF-8"

platform = platform.system()

def usage():
    print("usage")

def mesToBinary(message):
    global encoding

    print(message)

    binary = []

    for i in message:
        binary.append(format(ord(i), '08b'))
    
    return binary


def getPixelData(image):
   
    pixels = list(image.getdata())
    width, height = image.size

    print("Width: %d Height: %d" % (width,height))
    print(len(pixels))
    print(pixels[0])
    print(pixels[0][0])

    return pixels, width, height

def modifyPixel(pixel, message):
  
    data = mesToBinary(message)
    lenData = len(data)
    imageData = iter(pixel)
    for i in range(lenData):

        #Extract 3 pixels at a time
        pixel = [value for value in imageData.__next__()[:3] + imageData.__next__()[:3] + imageData.__next__()[:3]]

        #Value is 1 for odd and 0 for even

        for j in range(0,8):
            print(len(pixel))
            print(j)
            print(data)
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
        if platform == "Linux":
            os.system("clear")
        elif platform == "Windows":
            os.system("cls")

def encode(imgPath, message, outFile):

    image = Image.open(imgPath)

    pixels, width, height = getPixelData(image)

    outImg = image.copy()

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
            return data

def main():

    if not len(sys.argv[1:]):
        usage()

    if len(sys.argv) > 2:
        imgPath = sys.argv[1]
        message = sys.argv[2]
        outFile = sys.argv[3]
        encode(imgPath,message, outFile)
    else:
        imgPath = sys.argv[1]
        print(decode(imgPath))


'''
    #Read command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:m:t:o:", ["help=","path=","message=","type=","outFile="])
    except getopt.GetoptError as err:
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-p", "--path"):
            imgPath = a
        elif o in ("-m", "--message"):
            message = a
        elif o in ("-t", "--type"):
            if o == "encode" or o == "e":
                encode = True
            elif o == "decode" or o == "d":
                decode == True
            else: 
                usage()
        elif o in ("-o", "--outFile"):
            outFile = a
'''


'''
    if encode and decode:
        print("[!!!] Error cannot encode and dcode at the same time!")
        usage()
    elif encode:
        encode(imgPath, binary)
    elif decode:
       print(decode(imgPath))
'''

main()
