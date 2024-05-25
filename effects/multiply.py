
params = {
    "multiple":
        {
            "type": float,
            "min": -5.0,  # You could go beyond these limits, but the output comes out much noisier
            "max": 5.0,
        },
    }

def effect(pixeldata, **kwargs):
    multiple = kwargs["multiple"];

    for byte_index in range( len(pixeldata) ):
        byte = pixeldata[byte_index];
        multiplied_byte = round(byte * multiple);
        result_byte = multiplied_byte % 256;
        pixeldata[byte_index] = result_byte;

    return pixeldata;
