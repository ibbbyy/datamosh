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
    "noisy":
        {
            "type": bool,
        },
    }

def effect(pixeldata, **kwargs):
    channel_length = int(len(pixeldata) / 3);
    red, green, blue = split_channels(pixeldata);

    red_multiplier = kwargs["red_multiplier"];
    green_multiplier = kwargs["green_multiplier"];
    blue_multiplier = kwargs["blue_multiplier"];
    
    noisy = kwargs["noisy"];

    for byte_index in range(channel_length):
        red_byte = red[byte_index];
        blue_byte = blue[byte_index];
        green_byte = green[byte_index];

        red_multiplied_byte = round(red_byte * red_multiplier);
        green_multiplied_byte = round(green_byte * green_multiplier);
        blue_multiplied_byte = round(blue_byte * blue_multiplier);

        if noisy or red_multiplied_byte <= 255:
            red[byte_index] = red_multiplied_byte % 256;
        if noisy or green_multiplied_byte <= 255:
            green[byte_index] = green_multiplied_byte % 256;
        if noisy or blue_multiplied_byte <= 255:
            blue[byte_index] = blue_multiplied_byte % 256;

    return merge_channels(red, green, blue);
