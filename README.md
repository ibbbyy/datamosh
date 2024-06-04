# datamosh
Python program to datamosh images using functions

## Requirements
Only PIL is required to use this program. 

## Usage
Run as a commandline script.
Example: `python main.py -i image.png -e xor_self_offset`
This will run the effect `xor_self_offset` on `image.png` (located in the local directory) with random parameters (because they have not been specified.)
### Arguments
`-i` or `--input` determines the input file.

`-o` or `--output` determines the output file. (output.png by default)

`-c` or `--count` determines how many times the script will run.

`-e` or `--effect` determines which effect to use. Must be the name of the python file (without the file extension) located in the effects folder. For example, `-e multiply`

`-p` or `--params` lets you specify custom parameters instead of the default random. Follows the format `-p param value`, for example `-p intensity 0.5`

## Creating custom effects
Create a copy of the template.py template and manipulate the result_byte to any value as long as it is a positive integer less than 256. Use modulo 256 to "wrap around" the byte's value, keeping it in range from 0 to 255.
Look at other included effects for inspiration/instruction.

# Contact
Please do contact me on discord @`flitteringobsolescence` or email me [ibbbyy@proton.me](mailto:ibbbyy@proton.me) if you have any questions, need any help, or simply want to discuss this project.
