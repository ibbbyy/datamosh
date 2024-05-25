from utils import split_channels, merge_channels;

min_ = -5.0;
max_ = 5.0;

params = {
    "red_multiplier":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    "green_multiplier":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    "blue_multiplier":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    }

def effect(pixeldata, **kwargs):
    channel_length = int(len(pixeldata) / 3);
    red, green, blue = split_channels(pixeldata);
    red_multiplier = kwargs["red_multiplier"];
    green_multiplier = kwargs["green_multiplier"];
    blue_multiplier = kwargs["blue_multiplier"];

    for byte_index in range(channel_length):
        red_byte = red[byte_index];
        blue_byte = blue[byte_index];
        green_byte = green[byte_index];

        red[byte_index] = round(red_byte * red_multiplier) % 256;
        green[byte_index] = round(green_byte * green_multiplier) % 256;
        blue[byte_index] = round(blue_byte * blue_multiplier) % 256;

    return merge_channels(red, green, blue);
