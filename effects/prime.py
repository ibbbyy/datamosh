prime_numbers = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251);

params = {
    "new_value":
        {
            "type": int,
            "min": 0,
            "max": 255,
        },
    }

def effect(pixeldata, **kwargs):
    new_value = kwargs["new_value"];

    for byte_index in range( len(pixeldata) ):
        byte = pixeldata[byte_index];
        if byte in prime_numbers:
            byte = new_value;
        pixeldata[byte_index] = byte;

    return pixeldata;
