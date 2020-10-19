# description
* An image file loader gui with some simple features written in python

# directory structure
* ImageLoad.py: main program, run to implement the file loader gui; written used Python framework kiwy
* ImageLoad.kv: a kv file that mainly contains screen and screen manager info, which will be used by "ImageLoad.py"
* image1.jpg: 

# function description:
* User can load images files "*.jpg" or "*.png" after entering a correct file path
* A popup window will show up if the file path or file type is invalid
* User can loaded new images as they want, and each time the newly loaded one will replace the previous one on the screen.
* User can do simple operations on the loaded image, such as
  - zoom in/zoon out, where zoom in is limited by the window size
  - 
* The position of loaded image will be automatically adjusted by the window size