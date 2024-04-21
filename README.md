# datamosh
Python program to datamosh images using functions

## Requirements
Only PIL is required to use this program. 

## Using
Run as a commandline script.
Example: `python main.py -i image.png -e xor_self_offset`
### Arguments
`-i` or `--input` determines the input file.

`-o` or `--output` determines the output file. (output.png by default)

`-c` or `--count` determines how many times the script will run.

`-e` or `--effect` determines which effect to use. Must be the name of the python file located in the effects folder.

`-p` or `--params` lets you specify custom parameters instead of the default random. Follows the format `param value`, for example `-p intensity 0.5`

## Creating custom effects
Create a copy of the template.py template and manipulate the result_byte to a value between 0 and 255.
Look at other included effects for inspiration/instruction.

# Contact
Please do contact me on discord `flitteringobsolescence` if you have questions or need any help or want to discuss/help out with this project.
