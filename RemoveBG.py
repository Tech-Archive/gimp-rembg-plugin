#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Modified GIMP plugin to remove backgrounds from images
# with an option to process all open images.
# Original author: James Huang <elastic192@gmail.com>
# Modified by: Tech Archive <medium.com/@techarchive>
# Date: 13/9/24

from gimpfu import *
import os
import tempfile
import platform
import subprocess

tupleModel = (
    "u2net",
    "u2net_human_seg",
    "u2net_cloth_seg",
    "u2netp",
    "silueta",
    "isnet-general-use",
    "isnet-anime",
    "sam"
)

def remove_background(image, drawable, asMask, selModel, AlphaMatting, aeValue, make_square):
    removeTmpFile = True
    tdir = tempfile.gettempdir()
    jpgFile = os.path.join(tdir, "Temp-gimp-0000.jpg")
    pngFile = os.path.join(tdir, "Temp-gimp-0000.png")

    image.undo_group_start()
    curLayer = pdb.gimp_image_get_active_layer(image)
    x1, y1 = curLayer.offsets

    # Save the current layer to a temporary JPEG file
    pdb.file_jpeg_save(image, curLayer, jpgFile, jpgFile, 0.95, 0, 1, 0, "", 0, 1, 0, 0)

    # Path to your Python executable where rembg is installed
    pythonExe = "C:\\Users\\adamy\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"

    # Build the rembg command using rembg.cli
    cmd = [
        pythonExe, '-m', 'rembg.cli', 'i', '-m', tupleModel[selModel]
    ]
    if AlphaMatting:
        cmd.extend(['-a', '-ae', str(aeValue)])
    cmd.extend([jpgFile, pngFile])

    # Execute the command and capture output using subprocess.Popen
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            pdb.gimp_message("rembg error:\n" + stderr.decode('utf-8'))
            image.undo_group_end()
            return
    except Exception as e:
        pdb.gimp_message("Failed to execute rembg:\n" + str(e))
        image.undo_group_end()
        return

    # Load the output PNG as a new layer
    if os.path.exists(pngFile):
        newlayer = pdb.gimp_file_load_layer(image, pngFile)
        pdb.gimp_image_add_layer(image, newlayer, 0)
        pdb.gimp_layer_set_offsets(newlayer, x1, y1)

        if asMask:
            # Create and add mask if the option is selected
            mask = pdb.gimp_layer_create_mask(newlayer, ADD_ALPHA_MASK)
            pdb.gimp_layer_add_mask(newlayer, mask)
        else:
            # No mask option selected:
            # Step 1: Remove the original layer
            pdb.gimp_image_remove_layer(image, curLayer)

            # Step 2: Create a new white background layer
            white_bg_layer = pdb.gimp_layer_new(image, image.width, image.height, RGB_IMAGE, "White Background", 100, LAYER_MODE_NORMAL)
            pdb.gimp_drawable_fill(white_bg_layer, WHITE_FILL)

            # Step 3: Ensure the white background is at the bottom, newlayer on top
            pdb.gimp_image_insert_layer(image, white_bg_layer, None, -1)
            pdb.gimp_image_raise_item_to_top(image, newlayer)

            # Step 4: Merge the new transparent layer with the white background
            merged_layer = pdb.gimp_image_merge_down(image, newlayer, CLIP_TO_BOTTOM_LAYER)

            # Ensure visibility of the final merged layer
            pdb.gimp_item_set_visible(merged_layer, True)

        # Step 5: Handle the "Make Square" option
        if make_square:
            # Get the current width and height of the image
            img_width = pdb.gimp_image_width(image)
            img_height = pdb.gimp_image_height(image)

            # Determine the longer side (either width or height)
            max_side = max(img_width, img_height)

            # Resize the canvas to make the image square
            pdb.gimp_image_resize(image, max_side, max_side, (max_side - img_width) // 2, (max_side - img_height) // 2)

        # Step 6: Flatten the image (merge all visible layers)
        pdb.gimp_image_merge_visible_layers(image, CLIP_TO_BOTTOM_LAYER)

    else:
        pdb.gimp_message("Output PNG file was not created.")

    image.undo_group_end()
    gimp.displays_flush()

    # Clean up temporary files
    if removeTmpFile:
        try:
            os.remove(jpgFile)
            os.remove(pngFile)
        except Exception:
            pass

def python_fu_RemoveBG(image, drawable, asMask, selModel, AlphaMatting, aeValue, make_square, process_all_images):
    if process_all_images:
        images = gimp.image_list()
        for img in images:
            drawable = pdb.gimp_image_get_active_layer(img)
            remove_background(img, drawable, asMask, selModel, AlphaMatting, aeValue, make_square)
    else:
        remove_background(image, drawable, asMask, selModel, AlphaMatting, aeValue, make_square)

register(
    "python_fu_RemoveBG",
    "AI Remove image background",
    "Remove image backgrounds using AI with an option to process all open images.",
    "Tech Archive",
    "GPLv3",
    "2023",
    "<Image>/Python-Fu/AI Remove Background...",
    "RGB*, GRAY*",
    [
        (PF_TOGGLE, "asMask", "Use as Mask", True),
        (PF_OPTION, "selModel", "Model", 0, tupleModel),
        (PF_TOGGLE, "AlphaMatting", "Alpha Matting", False),
        (PF_SPINNER, "aeValue", "Alpha Matting Erode Size", 15, (1, 100, 1)),
        (PF_TOGGLE, "make_square", "Make Square", False),
        (PF_TOGGLE, "process_all_images", "Process all open images", False)
    ],
    [],
    python_fu_RemoveBG)

main()
