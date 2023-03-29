# Take file as input and take the bits. Make a video from all the bits (1920x1080) and save it as output.mp4 where every pixel is 3 bits (RGB)
import sys
import os
from PIL import Image
import cv2
import numpy

size = 360, 240
new_size = 720, 480
pixels_per_frame = size[0] * size[1]
framerate = 10
bits_per_color = 3
padding = [i for i in range(0,64)]

# Read the file
file = open(sys.argv[1], "rb")
data = file.read()
file.close()

# Convert the data to bits
bits = []
for byte in data:
    for i in range(7, -1, -1):
        bits.append((byte >> i) & 1)

bits = padding + bits + padding
        
# For every pixel, take 3 bits and make a color
pixels = [(bits[index]*255, bits[index + 1]*255, bits[index + 2]*255) for index in range(0, len(bits), bits_per_color)]

# Make frames from the pixels
images = []
for i in range(0, len(pixels), pixels_per_frame):
    image = Image.new("RGB", size)
    image.putdata(pixels[i:i+pixels_per_frame])
    image = image.resize(new_size, Image.NEAREST)
    images.append(image)
    print("Frame " + str(i/pixels_per_frame) + " of " + str(len(pixels)/pixels_per_frame), end="\r")

# Save the frames as a video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter("output.mp4", fourcc, framerate, new_size)
for image in images:
    video.write(cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR))

video.release()

