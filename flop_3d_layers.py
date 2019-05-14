import os
import PIL

# Outline of what we need to do:
# Take command line input of the name of the zip file with images
# Unzip into a temp directory
# Get an array of all of the images
# One by one:
# - Load the image
# - Flop the image
# - Save the image
# Re-zip the files with the original name + "_flop"
# unless we get command line input with a different output name