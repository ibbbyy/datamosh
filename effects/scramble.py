from math import ceil;
import random;
from sys import maxsize;

params = {
    "chunk_size":
        {
            "type": float,
            "min": 0.0,
            "max": 1.0,
        },
    "offset":
        {
            "type": float,
            "min": 0.0,
            "max": 1.0,
        },
    "seed":
        {
            "type": int,
            "min": -maxsize,
            "max": maxsize,
        },
    }

def effect(pixeldata, **kwargs):
    chunk_size = kwargs["chunk_size"] * 0.5;
    offset = kwargs["offset"];
    random.seed(kwargs["seed"]);
    
    chunk_size = round( len(pixeldata) * chunk_size );
    chunk_num = ceil( len(pixeldata) / chunk_size );

    chunk_list = [];
    chunk_end = round(len(pixeldata) * offset);  # Our start position

    for chunk_index in range( chunk_num ):
        chunk_start = chunk_end;

        chunk_list.append({});  # hehe pussy
        chunk_list[chunk_index]["start"] = chunk_start;

        chunk_end += chunk_size;

        if chunk_end < len(pixeldata):
            chunk_list[chunk_index]["data"] = pixeldata[chunk_start:chunk_end];
        else:
            chunk_end = chunk_end - len(pixeldata);
            chunk_list[chunk_index]["data"] = pixeldata[chunk_start:] + pixeldata[:chunk_end];

        chunk_list[chunk_index]["end"] = chunk_end;

    unscrambled_chunks = list( range( len(chunk_list) ) );

    for chunk in chunk_list:
        chunk_start = chunk["start"];
        chunk_end = chunk["end"];

        newchunk_index = unscrambled_chunks.pop( random.randint(0, len(unscrambled_chunks)-1) );
        newchunk_data = chunk_list[newchunk_index]["data"];

        if chunk_start < chunk_end:
            pixeldata[chunk_start:chunk_end] = newchunk_data;
        else:
            pixeldata[chunk_start:] = newchunk_data[:chunk_size-chunk_end];
            pixeldata[:chunk_end] = newchunk_data[chunk_size-chunk_end:];


    return pixeldata;
