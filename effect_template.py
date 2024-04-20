params = {
    "variable":
        {
            "type": int,
            "min": 0,
            "max": 100,
        },
    }

def effect(pixeldata, **kwargs):
    variable = kwargs["variable"];

    for byte_index in range( len(pixeldata) ):
        byte = pixeldata[byte_index];
        result_byte = byte;
        pixeldata[byte_index] = result_byte;

    return pixeldata;
