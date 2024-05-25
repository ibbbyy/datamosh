from math import sqrt;
from utils import normalize_byte;

prime_numbers = (2, 3, 5, 7, 11, 13);

params = {
    "new_value":
        {
            "type": int,
            "min": 0,
            "max": 255,
        },
    "normalize":
        {
            "type": bool,
        },
    }

def effect(pixeldata, **kwargs):
    new_value = kwargs["new_value"];
    normalize = kwargs["normalize"];

    for byte_index in range( len(pixeldata) ):
        byte = pixeldata[byte_index];
        if normalize:
            byte = normalize_byte(byte);
        if sqrt(byte) in prime_numbers:
            byte = new_value;
        pixeldata[byte_index] = byte;

    return pixeldata;
