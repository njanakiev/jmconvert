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
    
    usage: jmconvert [-h] [-f JEKYLL_FOLDER] [-a ASSETS_FOLDER] [-p POSTS_FOLDER]
                 [-t]
                 ipynb_filepath

    Jupyter notebook to Jekyll markdown converter

    positional arguments:
      ipynb_filepath    Jupyter notebook path

    optional arguments:
      -h, --help        show this help message and exit
      -f JEKYLL_FOLDER  Jekyll folder path
      -a ASSETS_FOLDER  Assets folder path
      -p POSTS_FOLDER   Posts folder path
      -t                Use current time as date
    
# License 
This project is licensed under the MIT license. See the [LICENSE](LICENSE) for details.
