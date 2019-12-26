# jmconvert

Simple Command-line tool that converts Jupyter notebooks to Jekyll markdown including external and embedded images.


# Installation

To install the tool, you can run:

    $ git clone https://github.com/njanakiev/jmconvert
    $ cd jmconvert
    $ pip install .


# Usage

To use it, have a look at the help:

    $ jmconvert --help
    
    usage: jmconvert [-h] [-o] ipynb_filepath jekyll_folder                                             

    Jupyter notebook to Jekyll markdown converter   

    positional arguments:   
      ipynb_filepath  Jupyter notebook path         
      jekyll_folder   Jekyll folder path            

    optional arguments:     
      -h, --help      show this help message and exit                                                
      -o              Overwrite existing
    
# License 
This project is licensed under the MIT license. See the [LICENSE](LICENSE) for details.
