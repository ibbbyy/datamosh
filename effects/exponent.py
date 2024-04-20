
params = {
    "exponent":
        {
            "type": float,
            "min": 1.0,
            "max": 1.5,  # Beyond these limits output is too noisy.
        },
    }

def effect(pixeldata, **kwargs):
    exponent = kwargs["exponent"];

    for byte_index in range( len(pixeldata) ):
        byte = pixeldata[byte_index];
        if byte == 0:
            result_byte = byte;
        else:
            multiplied_byte = round(byte ** exponent);
            result_byte = multiplied_byte % 255;
        pixeldata[byte_index] = result_byte;

    return pixeldata;
