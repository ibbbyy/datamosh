params = {
    "distance":
        {
            "type": int,
            "min": 1,
            "max": 10,
        },
    }

def effect(pixeldata, **kwargs):
    distance = kwargs["distance"];
    original_pixeldata = pixeldata[:];

    for byte_index in range( len(pixeldata) ):
        local_bytes = original_pixeldata[ byte_index-distance : byte_index+distance ];
        result_byte = sum(local_bytes) % 256;
        pixeldata[byte_index] = result_byte;

    return pixeldata;
