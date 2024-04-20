
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

        underflow_byte = byte - round(255*intensity);
        overflow_byte = byte + round(255*intensity);

        underflow = underflow_byte < 0;
        overflow = overflow_byte > 255;

        if underflow and not overflow:
            result_byte = underflow_byte % 255;
        elif overflow and not underflow:
            result_byte = overflow_byte % 255;
        else:
            result_byte = (underflow_byte + overflow_byte) % 255;

        pixeldata[byte_index] = result_byte;

    return pixeldata;
