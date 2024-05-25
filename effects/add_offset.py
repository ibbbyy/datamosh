
params = {
    "offset":
        {
            "type": float,
            "min": 0.0,
            "max": 1.0,
        },
    }

def effect(pixeldata, **kwargs):
    byte_offset = round( kwargs["offset"] * len(pixeldata) );

    for byte_index in range( len(pixeldata) ):
        byte = pixeldata[byte_index];
        offset_index = byte_index +  byte_offset;

        if offset_index < len(pixeldata):
            offset_byte = pixeldata[offset_index];
        else:
            offset_byte = pixeldata[offset_index - len(pixeldata)];

        added_byte = byte + offset_byte;
        result_byte = added_byte % 256;

        pixeldata[byte_index] = result_byte;

    return pixeldata;
