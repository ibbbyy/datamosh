
params = {
    "multiple":
        {
            "type": float,
            "min": 1.0,
            "max": 10.0,
        },
    "noisy":
        {
            "type": bool,
        },
    }

def effect(pixeldata, **kwargs):
    multiple = kwargs["multiple"];
    noisy = kwargs["noisy"];

    for byte_index in range( len(pixeldata) ):
        byte = pixeldata[byte_index];
        multiplied_byte = round(byte * multiple);
        
        if noisy or multiplied_byte <= 255:
            result_byte = multiplied_byte % 256;
            pixeldata[byte_index] = result_byte;

    return pixeldata;
