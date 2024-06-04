from mmap import mmap;
from time import time;


def convert_to_type(value, data_type):
    """
    Converts a string value to given data_type
    """

    if data_type == str:
        return value;

    elif data_type == int:
        return int(value);

    elif data_type == float:
        return float(value);

    elif data_type == bool:
        if value.lower() in ("true", "t", "y", "yes", "1"):
            return True;
        elif value.lower() in ("false", "f", "n", "no", "0"):
            return False;
        else:
            raise ValueError(
                f"""Could not determine boolean value of {value} typed {original_type}\n
                    Try entering a value like 'false' or 'true'."""
                    );

    else:
        raise ValueError("Unsupported data type");


def normalize_byte(byte):
    """
    Multiplies smaller bytes to be bigger.
    """
    if byte <= 10:
        byte *= 25.5;
    elif byte <= 100:
        byte *= 2.55;
    byte = round(byte);
    return byte;


# ------------------ RGB Channel functions ------------------
#
# Known bug:
# Some images do not get properly split, this is because for some reason they have a fourth channel.
# Not sure why they have a fourth channel if its a bitmap image -- something to look into later.
# Unsure how to implement a fix fort this or how to work this into existing effects.

def split_channels(pixelarray):
    """
    Splits the pixelarray into three separate red, green, and blue pixel arrays.
    """
    start_time = time();  # Timing the function

    channel_length = int(len(pixelarray) / 3);

    red_length = channel_length;
    green_length = channel_length;
    blue_length = channel_length;

    # ------------------------------------------------------
    # I have no idea why but some images have a remainder
    remainder = len(pixelarray) % 3;  

    if remainder > 0:
        blue_length += 1;
        if remainder > 1:
            green_length += 1;
            if remainder > 2:
                red_length += 1;
    # ------------------------------------------------------
    
    red_channel = mmap(-1, red_length);
    green_channel = mmap(-1, green_length);
    blue_channel = mmap(-1, blue_length);

    red_channel[:] = pixelarray[2::3];
    green_channel[:] = pixelarray[1::3];
    blue_channel[:] = pixelarray[0::3];

    end_time = time();  # Timing the function
    elapsed_seconds = round(end_time - start_time, 2);
    print(f"Split channels from pixelarray in {elapsed_seconds} seconds.");

    return red_channel, green_channel, blue_channel;


def merge_channels(red_channel, green_channel, blue_channel):
    """
    Merges three red, green, and blue pixelarrays into one RGB pixelarray.
    """
    start_time = time();  # Timing the function

    red_index = 0;
    green_index = 0; 
    blue_index = 0;

    pixelarray_length = len(red_channel) + len(green_channel) + len(blue_channel);

    pixelarray = mmap(-1, pixelarray_length);

    pixelarray[2::3] = red_channel[:];
    pixelarray[1::3] = green_channel[:];
    pixelarray[0::3] = blue_channel[:];

    end_time = time();  # Timing the function
    elapsed_seconds = round(end_time - start_time, 2);
    print(f"Merged channels to pixelarray in {elapsed_seconds} seconds.");

    return pixelarray;
