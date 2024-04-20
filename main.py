# External modules
from PIL import Image;
# Internal modules
import utils;
# Builtins
import sys;
from mmap import mmap;
import tempfile;
import os;
from importlib import import_module;
import random;
from time import time;


def process_image(inputpath, outputpath, effectname, params={}):
    # Loading effect
    effect = import_module(f"effects.{effectname}");

    # Validating parameters and randomizing missing parameters
    if len(params) > len(effect.params):
        raise ValueError("Too many parameters");

    elif len(params) <= len(effect.params):
        for param_name in effect.params.keys():
            # Randomizing parameters not specified
            if param_name not in params.keys():
                param_type = effect.params[param_name]["type"];
                if param_type in (int, float):
                    param_min = effect.params[param_name]["min"];
                    param_max = effect.params[param_name]["max"];

                if param_type == float:
                    params[param_name] = random.uniform(param_min, param_max);
                elif param_type == int:
                    params[param_name] = random.randint(param_min, param_max);
                elif param_type == bool:
                    params[param_name] = random.choice((True, False));

    # Clamping paramaters
    for param_name in params.keys():
        param_type = effect.params[param_name]["type"];
        if param_type in (int, float):
            param_value = params[param_name];
            param_min = effect.params[param_name]["min"];
            param_max = effect.params[param_name]["max"];
            param_value = utils.clamp(param_value, param_min, param_max);
            params[param_name] = param_value;

    print(f"INPUT:  {inputpath}");
    print(f"OUTPUT: {outputpath}");
    print(f"EFFECT: {effectname}");
    print("PARAMETERS:");
    print(str(params)[1:-1].replace(", ", "\n").replace(" ", "\t"));

    # Converting to bitmap
    with Image.open(inputpath) as im:
        temp_bitmap = tempfile.TemporaryFile();
        im.save(temp_bitmap, "bmp");

    # Creating a memory map of the bitmap file
    memorymap = mmap(temp_bitmap.fileno(), 0);
    headerlength = memorymap[10];

    # Grabbing the pixel data and assigning it to it's own memory map
    pixeldata_bytearray = memorymap[headerlength:];
    pixeldata_mmap = mmap(-1, len(pixeldata_bytearray));
    pixeldata_mmap.write(pixeldata_bytearray);

    start_time = time();  # Timing effect time

    # Applying the effect
    pixeldata_mmap = effect.effect(pixeldata_mmap, **params);

    end_time = time();
    elapsed_seconds = round(end_time - start_time, 2);
    print(f"Effect finished processing in {elapsed_seconds} seconds.");

    start_time = time();  # Timing save time

    # Adding pixel data back to main memory map
    memorymap[headerlength:] = pixeldata_mmap[:];
    memorymap.flush();

    # Saving result
    with Image.open(temp_bitmap) as im:
        im.save(outputpath);

    end_time = time();
    elapsed_seconds = round(end_time - start_time, 2);
    print(f"Saved to file in {elapsed_seconds} seconds.");

if __name__ == "__main__":
    # Defaults
    inputpath = "coolbunny.jpeg";
    outputpath = "output.png";
    count = 1;
    effectname = "";
    params = {};

    # Iterating through commandline arguments
    # TODO: Use the builtin module for handling this. This was just a quick hack
    for a in range(len(sys.argv)):
        argument = sys.argv[a];

        if argument in ["-i", "--input"]:
            inputpath = sys.argv[a + 1];
        elif argument in ["-o", "--output"]:
            outputpath = sys.argv[a + 1];
        elif argument in ["-c", "--count"]:
            count = int(sys.argv[a + 1]);
            if count <= 0:
                count = 1;
        elif argument in ["-e", "--effect"]:
            effectname = sys.argv[a + 1];
            effect = import_module(f"effects.{effectname}");
        elif argument in ["-p", "--params"]:
            # Getting the amount of parameters that have been specified
            # TODO: add logic to this so it's not necessary that this has to be the final argument.
            param_num = ( len(sys.argv) - (a + 1) ) / 2;

            # Converting param_num to integer. If this fails that means there was an uneven amount of parameter names to values.
            # Most commonly this is caused by improper formatting.
            # The format should be the parameter name and then the parameter value.
            # For example, -p offset 0.5
            try:
                param_num = int(param_num);
            except ValueError:
                raise ValueError("Invalid parameters");

            # Iterating through parameters
            for p in range(param_num):
                param_name = sys.argv[a+1 + (p*2)];
                param_value = sys.argv[a+2 + (p*2)];
                param_type = effect.params[param_name]["type"];
                # Converting to correct type
                param_value = utils.convert_to_type(param_value, param_type);
                params[param_name] = param_value;

    original_outputpath = outputpath;
    original_params = params.copy();
    original_effectname = effectname;

    for c in range(count):
        # Refreshing any params that need to be randomized
        params = original_params.copy();

        # Allowing for multiple output images
        if c > 0:
            print("-"*50);
            splitext = os.path.splitext(original_outputpath);
            outputpath = splitext[0] + str(c) + splitext[1];

        # Randomizing effect if not specified
        if not original_effectname:
            effects_list = os.listdir("effects");  # Grabbing all effects
            # Removing the file extension (.py) from each effect
            for i in range( len(effects_list) ):
                splitext = os.path.splitext(effects_list[i])
                effect_name = splitext[0];
                effects_list[i] = effect_name;
            effectname = random.choice(effects_list);  # Choosing effect

        process_image(inputpath, outputpath, effectname, params);

