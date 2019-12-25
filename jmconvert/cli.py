from __future__ import print_function
import os
import argparse

import parse
#from . import parse


def main():
    """Jupyter notebook to Jekyll markdown converter"""

    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Jupyter notebook to Jekyll markdown converter')
    parser.add_argument(action='store', dest='ipynb_filepath',
                        help='Jupyter notebook path')
    parser.add_argument(action='store', dest='jekyll_folder',
                        help='Jekyll folder path')
    parser.add_argument('-o', action='store_true', default=False,
                        help='Overwrite existing', dest='overwrite')

    # Get filepaths and settings
    args = parser.parse_args()
    ipynb_filepath = args.ipynb_filepath
    jekyll_folder  = args.jekyll_folder if args.jekyll_folder else ''
    overwrite      = args.overwrite
    assets_path    = os.path.join(jekyll_folder, "assets")
    posts_path     = os.path.join(jekyll_folder, "_posts")

    # Check if filepaths exist
    if not os.path.exists(ipynb_filepath):
        parser.error('File not found: {}'.format(ipynb_filepath))
    if not os.path.exists(assets_path):
        parser.error('Folder not found: {}'.format(assets_path))
    if not os.path.exists(posts_path):
        parser.error('Folder not found: {}'.format(posts_path))

    # Check if filepath is directory
    if os.path.isdir(ipynb_filepath):
        print("filepath is directory")
        for filename in os.listdir(ipynb_filepath):
            if filename.endswith('.ipynb'):
                filepath = os.path.join(ipynb_filepath, filename)
                print('Converting filepath:', filepath)
                try:
                    parse.parse(filepath, assets_path, posts_path, overwrite)
                except Exception as e:
                    print("ERROR: {}, for {}".format(e, filepath))
    else:
        print('Converting filepath:', ipynb_filepath)
        parse.parse(ipynb_filepath, assets_path, posts_path, overwrite)

if __name__ == '__main__':
    main()
