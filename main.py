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


def validate_image_path(path):
    dirname, filename = os.path.split(path);
    extension = os.path.splitext(filename)[1]

    # Making sure image format is supported
    if extension.lower() not in Image.registered_extensions().keys():
        raise ValueError(f"'{extension.replace('.', '')}' is not a supported image format");

    # Creates a directory if one is specified and does not exist
    if dirname:
        if not os.path.exists(dirname):
            os.mkdir(dirname);

def parse_args(args):
    return_values = {
        "inputpath": None,
        "outputpath": None,
        "count": None,
        "effectname": None,
        "params": {},
        }

    for a in range(len(args)):
        argument = args[a];

        # Input/Output
        if argument in ("-i", "--input"):
            inputpath = args[a + 1];
            validate_image_path(inputpath);

            return_values["inputpath"] = inputpath;

        elif argument in ("-o", "--output"):
            outputpath = args[a + 1];
            validate_image_path(outputpath);

            return_values["outputpath"] = outputpath;

        # Count
        elif argument in ("-c", "--count"):
            try:
                count = int(args[a + 1]);
            except ValueError:  # Giving a more descriptive error.
                raise ValueError(f"Count (-c) expected integer, not '{count}'")
            if count <= 0:
                count = 1;

            return_values["count"] = count;

        # Effect
        elif argument in ("-e", "--effect"):
            effectname = args[a + 1];
            # Validating effect exists
            try:
                effect = import_module(f"effects.{effectname}");
            except ModuleNotFoundError:
                raise ValueError(f"Invalid effect '{effectname}'. Make sure it is located in the effects folder and you are not including the file extension.")

            return_values["effectname"] = effectname;

        # Parameters
        elif argument in ("-p", "--params") and effectname:
            arguments_left = args[a+1:];
            valid_param_names = effect.params.keys()

            for a_ in range( len(arguments_left) ):
                arg = arguments_left[a_];

                # Looking for a valid name
                if not a_ % 2:
                    if arg in valid_param_names:
                        param_name = arg;
                    else:
                        # Exiting loop if argument is different argument.
                        if arg.startswith("-"):
                            break;
                        else:
                            print(f"WARNING: {arg} was not recongnized as a valid parameter and will be skipped.");
                            param_name = None;

                # Looking for a valid value
                else:
                    # Skipping invalid parameters
                    if param_name == None:
                        # Exiting loop if argument is different argument.
                        if arg.startswith("-") and not arg[1:].isdigit():
                            break;
                        continue;

                    param_type = effect.params[param_name]["type"];

                    try:
                        if param_type == int:
                            converted_value = int(arg);
                        elif param_type == float:
                            converted_value = float(arg);
                        elif data_type == bool:
                                if arg.lower() in ("true", "tru", "tr", "t", "y", "yes", "1"):
                                    converted_value = True;
                                elif arg.lower() in ("false", "fals", "fal", "fa" "f", "n", "no", "0"):
                                    converted_value = False;
                                else:  # Not a valid boolean as far as can be interpreted.
                                    raise ValueError();
                        # If the argument does not fit into any valid types we raise an error
                        else:
                            raise ValueError();

                    except ValueError:
                        raise ValueError(f"Parameter '{param_name}' expects value to be typed as {param_type}, but {arg} could not be converted to {param_type}.");
                        continue;

                    return_values["params"][param_name] = converted_value;

    return return_values;


if __name__ == "__main__":
    default_values = {
        "inputpath": "coolbunny.jpeg",
        "outputpath": "output.png",
        "count": 1,
        "effectname": "",
    }

    # Parsing commandline arguments
    parsed_arguments = parse_args(sys.argv);

    # Setting any unset arguments to their default
    for arg_name in parsed_arguments.keys():
        if parsed_arguments[arg_name] == None:
            parsed_arguments[arg_name] = default_values[arg_name];

    for c in range(parsed_arguments["count"]):
        # Refreshing any parameters that need to be randomized
        params = parsed_arguments["params"].copy();

        # Allowing for multiple output images
        if c > 0:
            print("-"*50);
            splitext = os.path.splitext(parsed_arguments["outputpath"]);
            outputpath = splitext[0] + str(c) + splitext[1];
        else:
            outputpath = parsed_arguments["outputpath"];

        # Randomizing effect if not specified
        if not parsed_arguments["effectname"]:
            effects_list = os.listdir("effects");  # Grabbing all effects

            # Removing the file extension (.py) from each effect
            effects_list = [os.path.splitext(effect)[0] for effect in effects_list];

            effectname = random.choice(effects_list);  # Randomizing effect from effects_list
        else:
            effectname = parsed_arguments["effectname"]

        process_image(parsed_arguments["inputpath"], outputpath, effectname, params);

