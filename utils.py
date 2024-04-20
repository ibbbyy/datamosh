from mmap import mmap;
from time import time;

def convert_to_type(value, data_type):
    if data_type == int:
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
    if byte <= 10:
        byte *= 25.5;
    elif byte <= 100:
        byte *= 2.55;
    byte = round(byte);
    return byte;

def clamp(value, min_, max_):
    if value < min_:
        return min_;
    elif value > max_:
        return max_;
    else:
        return value;

def split_channels(pixelarray):
    start_time = time();  # Timing the function

    channel_length = int(len(pixelarray) / 3);
    red_channel = mmap(-1, channel_length);
    green_channel = mmap(-1, channel_length);
    blue_channel = mmap(-1, channel_length);

    for byte_index in range( len(pixelarray) ):
        byte = pixelarray[byte_index].to_bytes(1, "big");
        match byte_index % 3:
            case 2:  # Red
                red_channel.write(byte);
            case 1:  # Green
                green_channel.write(byte);
            case 0:  # Blue
                blue_channel.write(byte);

    end_time = time();
    elapsed_seconds = round(end_time - start_time, 2);
    print(f"Split channels from pixelarray in {elapsed_seconds} seconds.");

    return red_channel, green_channel, blue_channel;

def merge_channels(red_channel, green_channel, blue_channel):
    start_time = time();  # Timing the function

    red_index = green_index = blue_index = 0;
    pixelarray_length = len(red_channel) + len(green_channel) + len(blue_channel);
    pixelarray = mmap(-1, pixelarray_length);

    for byte_index in range(pixelarray_length):
        match byte_index % 3:
            case 2:  # Red
                byte = red_channel[red_index].to_bytes(1, "big");
                red_index += 1;
            case 1:  # Green
                byte = green_channel[green_index].to_bytes(1, "big");
                green_index += 1;
            case 0:  # Blue
                byte = blue_channel[blue_index].to_bytes(1, "big");
                blue_index += 1;
        pixelarray.write(byte);

    end_time = time();
    elapsed_seconds = round(end_time - start_time, 2);
    print(f"Merged channels to pixelarray in {elapsed_seconds} seconds.");

    return pixelarray;
