
params = {
    "exponent":
        {
            "type": float,
            "min": 1.0,
            "max": 1.5,  # Beyond these limits output is too noisy.
        },
    "noisy":
        {
            "type": bool,
        },
    }

def effect(pixeldata, **kwargs):
    exponent = kwargs["exponent"];
    noisy = kwargs["noisy"];

    for byte_index in range( len(pixeldata) ):
        byte = pixeldata[byte_index];

        if byte == 0:
            continue  # Skip
        
        multiplied_byte = round(byte ** exponent);
        
        if noisy or multiplied_byte <= 255:
            result_byte = multiplied_byte % 256;
            pixeldata[byte_index] = result_byte;

    return pixeldata;
