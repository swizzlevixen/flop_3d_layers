#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Takes the sliced output from PrusaSlicer, intended for the Prusa SL1,
and flops the images for proper printing through NanoDLP to a Wanhao D7.

(c) 2019 Mark Boszko
"""

import logging
import sys
import os
import tempfile
import zipfile
from PIL import Image
from progressbar import ProgressBar

# Logging Setup
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.ERROR)


# Outline of what we need to do:
# Take command line input of the name of the zip file with images
def flop_3d_layers(file_path):
    """
    Process the original file into a flopped version
    :param file_path: The original SLA slice file.
    :return:
    """
    # Create a temporary work folder
    with tempfile.TemporaryDirectory() as temp_path:
        logger.debug("Created temporary directory: " + temp_path)

        # Extract the original file into the working folder
        zip_ref = zipfile.ZipFile(file_path)
        zip_ref.extractall(temp_path)
        zip_ref.close()

        # Process the images and save into a new zip file
        walk_and_process(temp_path)
        zip_and_save(temp_path, file_path)


def walk_and_process(directory):
    """Walk all language subfolders, and rename the files
    with the language code and the hardware / app information
    :param directory: path to the temp folder with all images
    :return: none
    """
    print("Processing images...")
    pbar = ProgressBar()
    for folderName, subfolders, filenames in os.walk(directory):
        logger.debug("CURRENT FOLDER " + folderName)

        # Wrap the filenames array in pbar() to show a progress bar as we work through them
        for filename in pbar(filenames):
            logger.debug("FILE INSIDE    " + folderName + ": " + filename)
            name, extension = os.path.splitext(filename)
            if extension == ".png":
                image_path = os.path.join(folderName, filename)
                flop_image(image_path)
            else:
                logger.debug(">>> Processing OTHER: " + filename)


def flop_image(image_path):
    """
    Flop (horizontal mirror) the image
    :param image_path: The image to edit
    :return:
    """
    # logger.debug("flop_image: " + image_path)
    image_obj = Image.open(image_path)
    flop_image = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
    flop_image.save(image_path)
    # flop_image.show()


def zip_and_save(temp_path, file_path):
    """
    Re-zip the files with the original name + "_flop"
    :param temp_path: The temp dir with the flopped images
    :param file_path: The original zip file
    :return:
    """
    filename, file_extension = os.path.splitext(file_path)
    new_zip_filename = filename + "_flop.zip"
    zip_file = zipfile.ZipFile(new_zip_filename, "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(temp_path):
        for file in files:
            zip_file.write(os.path.join(root, file), file)
    zip_file.close()
    print(f"Output complete to {new_zip_filename}")


if __name__ == "__main__":

    # Check to see what command line arguments we got
    logger.debug("Arguments: " + str(len(sys.argv)))
    logger.debug("List: " + str(sys.argv))

    if len(sys.argv) < 2:
        logger.error("To few arguments, please specify a filename")

    # Look for "-f" so that we can accept either "-f" or "--force"
    # TODO: If we add more features, this should move to a proper argparse method
    if len(sys.argv) > 2 and "-f" in sys.argv[2]:
        force = True
    else:
        force = False

    # Assume that the first arg is the path to the slice file
    file_path = sys.argv[1]
    logger.debug("File path: " + str(file_path))

    # Cursory check to see if this is the right file type
    filename, file_extension = os.path.splitext(file_path)
    logger.debug("Filename: " + filename)
    logger.debug("File extension: " + file_extension)

    if file_extension == ".sl1" or file_extension == ".zip" or force == True:
        logger.debug("Valid file to process.")
        flop_3d_layers(file_path)
