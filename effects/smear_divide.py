from utils import split_channels, merge_channels, normalize_byte;

min_ = 0;
max_ = 40;

params = {
    "red_distance":
        {
            "type": int,
            "min": min_,
            "max": max_,
        },
    "green_distance":
        {
            "type": int,
            "min": min_,
            "max": max_,
        },
    "blue_distance":
        {
            "type": int,
            "min": min_,
            "max": max_,
        },
    }

def smear(pixeldata, distance):

    last_byte = 1;
    byte_index = 0;

    while byte_index < len(pixeldata):

        byte = pixeldata[byte_index];
        
        if byte == 255 or byte == 0:
            byte_index += 1;
            continue;

        if byte in pixeldata[byte_index + 1 : byte_index + distance]:

            for i in range(distance):

                index = i+1;

                if pixeldata[byte_index + index] == byte:

                    new_byte = round(byte / last_byte);

                    pixeldata[byte_index : byte_index + index] = new_byte.to_bytes(1, "big") * index;

                    byte_index = byte_index + index;
                    
                    if byte != 0:
                        last_byte = byte;
                    else:
                        last_byte = 1;

                    break;

        else:
            byte_index += 1;

    return pixeldata;

def effect(pixeldata, **kwargs):
    red, green, blue = split_channels(pixeldata);
    red_distance = kwargs["red_distance"];
    green_distance = kwargs["green_distance"];
    blue_distance = kwargs["blue_distance"];

    red = smear(red, red_distance);
    green = smear(green, green_distance);
    blue = smear(blue, blue_distance);

    return merge_channels(red, green, blue);