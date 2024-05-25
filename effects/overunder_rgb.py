from utils import split_channels, merge_channels

min_ = 0.0;
max_ = 1.0;

params = {
    "red_intensity":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    "green_intensity":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    "blue_intensity":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    }

def overunder(byte, intensity):
    underflow_byte = byte - round(255*intensity);
    overflow_byte = byte + round(255*intensity);

    underflow = underflow_byte < 0;
    overflow = overflow_byte > 255;

    if underflow and not overflow:
        result_byte = underflow_byte % 256;
    elif overflow and not underflow:
        result_byte = overflow_byte % 256;
    else:
        result_byte = (underflow_byte + overflow_byte) % 256;

    return result_byte;


def effect(pixeldata, **kwargs):
    channel_length = int(len(pixeldata) / 3);
    red, green, blue = split_channels(pixeldata);
    red_intensity = kwargs["red_intensity"];
    green_intensity = kwargs["green_intensity"];
    blue_intensity = kwargs["blue_intensity"];

    for byte_index in range(channel_length):
        red_byte = red[byte_index];
        blue_byte = blue[byte_index];
        green_byte = green[byte_index];

        red[byte_index] = overunder(red_byte, red_intensity);
        green[byte_index] = overunder(green_byte, green_intensity);
        blue[byte_index] = overunder(blue_byte, blue_intensity);

    return merge_channels(red, green, blue);
