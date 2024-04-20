from utils import split_channels, merge_channels, normalize_byte;

min_ = 0.0;
max_ = 1.0;

params = {
    "red_offset":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    "green_offset":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    "blue_offset":
        {
            "type": float,
            "min": min_,
            "max": max_,
        },
    }

def divide_offset(byte, offset_index, channel):
    if offset_index < len(channel):
        offset_byte = channel[offset_index];
    else:
        offset_byte = channel[offset_index - len(channel)];

    # Avoiding division by zero errors.
    if byte == 0:
        byte = 1;
    if offset_byte == 0:
        offset_byte = 1;

    if byte < offset_byte:
        divided_byte = offset_byte / byte;
    else:
        divided_byte = byte / offset_byte;

    # Bringing the image to a more normal brightness
    result_byte = normalize_byte(divided_byte);

    return result_byte;

def effect(pixeldata, **kwargs):
    channel_length = int(len(pixeldata) / 3);

    red, green, blue = split_channels(pixeldata);

    red_offset = round(channel_length * kwargs["red_offset"]);
    green_offset = round(channel_length * kwargs["green_offset"]);
    blue_offset = round(channel_length * kwargs["blue_offset"]);

    red_original = red[:];
    green_original = green[:];
    blue_original = blue[:];

    for byte_index in range(channel_length):
        red_byte = red[byte_index];
        blue_byte = blue[byte_index];
        green_byte = green[byte_index];

        red_offset_index = byte_index + red_offset;
        green_offset_index = byte_index + green_offset;
        blue_offset_index = byte_index + blue_offset;

        red[byte_index] = divide_offset(red_byte, red_offset_index, red_original);
        green[byte_index] = divide_offset(green_byte, green_offset_index, green_original);
        blue[byte_index] = divide_offset(blue_byte, blue_offset_index, blue_original);

    return merge_channels(red, green, blue);

