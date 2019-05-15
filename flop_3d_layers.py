import logging
import sys
import os
import zipfile
import PIL


# Logging Setup
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


# Outline of what we need to do:
# Take command line input of the name of the zip file with images
def flop_3d_layers(file_path):
    slicefiles = zipfile.ZipFile(file_path)



# Unzip into a temp directory
# Get an array of all of the images
# One by one:
# - Load the image
# - Flop the image
# - Save the image
# Re-zip the files with the original name + "_flop"
# unless we get command line input with a different output name
# delete the unzipped temp files


if __name__ == "__main__":
    logger.debug("Arguments: " + str(len(sys.argv)))
    logger.debug("List: " + str(sys.argv))

    if len(sys.argv) < 2:
        logger.error("To few arguments, please specify a filename")

    # Look for "-f" so that we can also accept "--force"
    if len(sys.argv) > 2 and "-f" in sys.argv[2]:
        force = True
    else:
        force = False

    file_path = sys.argv[1]
    logger.debug("File path: " + str(file_path))

    filename, file_extension = os.path.splitext(file_path)
    logger.debug("Filename: " + filename)
    logger.debug("File extension: " + file_extension)

    if file_extension == ".sl1" or file_extension == ".zip" or force == True:
        logger.debug("Valid file to process.")
        flop_3d_layers(file_path)

