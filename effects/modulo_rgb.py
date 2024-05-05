from utils import split_channels, merge_channels, normalize_byte;

min_ = 10.0;
max_ = 255.0;

params = {
    "red_modulo":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    "green_modulo":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    "blue_modulo":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    }

def effect(pixeldata, **kwargs):
    channel_length = int(len(pixeldata) / 3);
    red, green, blue = split_channels(pixeldata);
    red_modulo = kwargs["red_modulo"];
    green_modulo = kwargs["green_modulo"];
    blue_modulo = kwargs["blue_modulo"];

    for byte_index in range(channel_length):
        red_byte = red[byte_index];
        green_byte = green[byte_index];
        blue_byte = blue[byte_index];

        red[byte_index] = normalize_byte(red_byte % red_modulo);
        green[byte_index] = normalize_byte(green_byte % green_modulo);
        blue[byte_index] = normalize_byte(blue_byte % blue_modulo);

    return merge_channels(red, green, blue);
