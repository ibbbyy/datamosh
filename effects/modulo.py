from utils import normalize_byte;

params = {
    "modulo":
        {
            "type": float,
            "min": 10.0,
            "max": 255.0,
        },
    }

def effect(pixeldata, **kwargs):
    modulo = kwargs["modulo"];

    for byte_index in range( len(pixeldata) ):
        byte = pixeldata[byte_index];
        modulated_byte = byte % modulo;
        result_byte = normalize_byte(modulated_byte);
        pixeldata[byte_index] = result_byte;

    return pixeldata;
