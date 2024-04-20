from utils import split_channels, merge_channels

min_ = 1.0;
max_ = 1.5;  # Beyond these limits output is too noisy.

params = {
    "red_exponent":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    "green_exponent":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    "blue_exponent":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    }

def effect(pixeldata, **kwargs):
    channel_length = int(len(pixeldata) / 3);
    red, green, blue = split_channels(pixeldata);
    red_exponent = kwargs["red_exponent"];
    green_exponent = kwargs["green_exponent"];
    blue_exponent = kwargs["blue_exponent"];

    for byte_index in range(channel_length):
        red_byte = red[byte_index];
        blue_byte = blue[byte_index];
        green_byte = green[byte_index];

        red[byte_index] = round(red_byte ** red_exponent) % 255;
        green[byte_index] = round(green_byte ** green_exponent) % 255;
        blue[byte_index] = round(blue_byte ** blue_exponent) % 255;

    return merge_channels(red, green, blue);
