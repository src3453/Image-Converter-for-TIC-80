# Image Converter for TIC-80
An image converter that supports **hi color**.
## Sample
![image](https://github.com/src3453/Image-Converter-for-TIC-80/assets/103661526/cb19a633-d878-4d0b-a2fe-dad027dc8fc4)
## Usage
This tool requires `opencv-python`, `numpy`, `PIL`. (Also, `scikit-video` is required to run `convert_image_gif.py`)



In command line:



Type `$ python convert_image.py` to see the `Image path?>`. Then, enter the path to the image there. Once entered, press Enter to execute.



When executed, the files `converted.code.lua`, `converted.png`, and `converted.colors.png` will be generated.



The `converted.code.lua` file can be pasted directly into the TIC-80's code editor for execution.



## Bonus Tools



- `convert_image_rle.py`: A version that supports RLE compression.
- `convert_image_31c.py`: A version that can use 31 colors per line by switching VRAM banks.
- `convert_image_gif.py`: A version that supports GIF images and various videos. *Note: the code size usually larger than normal.*
