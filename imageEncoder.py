#text to image and image to text encoder and decoder
#parker sorenson
#6/30/17
import math
import argparse
from PIL import Image, ImageDraw
import random as rand

#use a seeded random seed

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="the file to encode or decode")
    parser.add_argument("seed", type=float, help="the seed for the random algorithm")
    return parser

def createPixel(n, seed):
    rand.seed(seed)
    r = n
    rand.seed(None)
    x = rand.randint(0,512)
    g = math.floor(rand.random()*x) % 256
    b = math.floor(rand.random()*x) % 256
    return((r,g,b))

def encode(file,seed):
    tList = []
    with open(file, 'r') as f:
        data = f.read()
        for c in data:
            t = createPixel(ord(c),seed)
            tList.append(t)
    imgDim = math.ceil(math.sqrt(len(tList)))
    size  = (imgDim,imgDim)
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    
    counter = 0
    for i in range(imgDim):
        for j in range(imgDim):
            if counter >= len(tList):
                draw.point((j,i), fill=(0,0,0))
            else:
                draw.point((j,i), fill=tList[counter])
            counter += 1    
    img.save(file[:-3] + 'png')

def decode(file, seed):
    img = Image.open(file)
    pixels = list(img.getdata())
    charList = []
    rand.seed(seed)
    ogSeed = rand.random()
    
    for pixel in pixels:
        charList.append(chr(pixel[0])) 
    return ''.join(charList)

def main():
    parser = createParser()
    file = parser.parse_args().file
    seed = parser.parse_args().seed
    
    if file.endswith('.txt'):
        encode(file,seed)
    elif file.endswith('.png'):
        print(decode(file,seed))
    else:
        print('Please enter a proper file format')
        
if __name__ == '__main__':
    main()
