
params = {
    "intensity":
        {
            "type": float,
            "min": 0.0,
            "max": 1.0,
        },
    }

def effect(pixeldata, **kwargs):
    intensity = kwargs["intensity"];

    for byte_index in range( len(pixeldata) ):
        byte = pixeldata[byte_index];
        overflow_byte = byte + round(255*intensity);
        result_byte = overflow_byte % 255;
        pixeldata[byte_index] = result_byte;

    return pixeldata;
