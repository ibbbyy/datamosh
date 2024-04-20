from utils import normalize_byte;

params = {
    "offset":
        {
            "type": float,
            "min": 0.5,
            "max": 1.0,
        },
    "divide_order":
        {
            "type": bool,
        },
    "offset_order":
        {
            "type": bool,
        },
    }

def effect(pixeldata, **kwargs):
    byte_offset = round( kwargs["offset"] * len(pixeldata) );
    divide_order = kwargs["divide_order"];
    offset_order = kwargs["offset_order"];

    for byte_index in range( len(pixeldata) ):
        byte = pixeldata[byte_index];
        if offset_order:
            offset_index = byte_index + byte_offset;

            if offset_index < len(pixeldata):
                offset_byte = pixeldata[offset_index];
            else:
                offset_byte = pixeldata[offset_index - len(pixeldata)];
        else:
            offset_index = byte_index - byte_offset;

            if offset_index >= 0:
                offset_byte = pixeldata[offset_index];
            else:
                offset_byte = pixeldata[offset_index + len(pixeldata)];

        # Avoiding division by zero errors.
        if byte == 0:
            byte = 1;
        if offset_byte == 0:
            offset_byte = 1;

        if divide_order:
            divided_byte = offset_byte / byte;
        else:
            divided_byte = byte / offset_byte;

        # Bringing the image to a more normal brightness
        result_byte = normalize_byte(divided_byte);

        pixeldata[byte_index] = result_byte;

    return pixeldata;
