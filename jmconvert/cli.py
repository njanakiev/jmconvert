from __future__ import print_function
import os
import re
import sys
import shutil
import datetime
import argparse
import nbconvert
import nbformat


def main():
    """Jupyter notebook to Jekyll markdown converter"""

    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Jupyter notebook to Jekyll markdown converter')
    parser.add_argument(action='store', dest='ipynb_filepath',
                        help='Jupyter notebook path')
    parser.add_argument('-f', action='store', dest='jekyll_folder',
                        help='Jekyll folder path', required=False)
    parser.add_argument('-a', action='store', dest='assets_folder',
                        help='Assets folder path', required=False)
    parser.add_argument('-p', action='store', dest='posts_folder',
                        help='Posts folder path', required=False)
    parser.add_argument('-t', action='store_true', default=False,
                        help='Use current time as date')

    args = parser.parse_args()
    ipynb_filepath = args.ipynb_filepath
    posts_folder   = args.posts_folder  if args.posts_folder  else '_posts'
    assets_folder  = args.assets_folder if args.assets_folder else 'assets'
    jekyll_folder  = args.jekyll_folder if args.jekyll_folder else ''
    current_time   = args.t
    assets_folder  = os.path.join(jekyll_folder, assets_folder)
    posts_folder   = os.path.join(jekyll_folder, posts_folder)

    if not os.path.exists(ipynb_filepath):
        parser.error('File not found: {}'.format(ipynb_filepath))
    if not os.path.exists(assets_folder):
        parser.error('Folder not found: {}'.format(assets_folder))
    if not os.path.exists(posts_folder):
        parser.error('Folder not found: {}'.format(posts_folder))

    print('Ipynb filepath : {}'.format(ipynb_filepath))
    print('Assets folder  : {}'.format(assets_folder))
    print('Posts  folder  : {}'.format(posts_folder))

    # Get filename and folder from jupyter notebook path
    ipynb_filename = os.path.splitext(os.path.basename(ipynb_filepath))[0]
    ipynb_folder = os.path.dirname(ipynb_filepath)
    image_folder_name = ipynb_filename.replace('-', '_') + "_files"

    # Load notebook and convert to markdown
    markdown_exporter = nbconvert.MarkdownExporter()
    with open(ipynb_filepath, 'r') as f:
        nb = nbformat.reads(f.read(), as_version=4)
    (body, resources) = markdown_exporter.from_notebook_node(nb)

    # Get current date
    if current_time:
        dt = datetime.datetime.now()
        files = [f for f in os.listdir(posts_folder) if ipynb_filename in f]
        if len(files) == 1:
             os.remove(os.path.join(posts_folder, files[0]))
        elif len(files) > 1:
            raise Exception('Multiple files named the same way with different dates')
    else:
        files = [f for f in os.listdir(posts_folder) if ipynb_filename in f]
        if len(files) == 0:
            dt = datetime.datetime.now()
        elif len(files) == 1:
            dt = datetime.datetime.strptime(files[0][:10], '%Y-%m-%d')
        else:
            raise Exception('Multiple files named the same way with different dates')

    markdown_filepath = os.path.join(posts_folder, '{}-{}.md'.format(
            dt.strftime('%Y-%m-%d'), ipynb_filename))

    # Remove first line break
    body = body[1:]

    # Find all image links
    pattern = r'\!\[.*?\]\((.+?)\)'
    images = re.findall(pattern, body)

    # Replace image links
    def image_replace(match):
        image_title, image_path = match.groups()
        return '![{}]({{{{ site.baseurl }}}}/assets/{}/{})'.format(
            image_title, image_folder_name, image_path.split('/')[-1])

    pattern = r'\!\[(.*?)\]\((.+?)\)'
    #new_pattern = r'![\1]({{{{ site.baseurl }}}}/{}/{}/\2)'.format(assets_folder, image_folder_name)
    body = re.sub(pattern, image_replace, body)

    # Replace single dollar signs for inline equations
    pattern = r'(?<!\$)\$(?!\$)'
    body = re.sub(pattern, '$$', body)

    # Wirte markdown post
    print('Writing post  : {}'.format(markdown_filepath))
    with open(markdown_filepath, 'w') as f:
        f.write(body)

    # Check if there are any images
    if images:
        # Remove existing image folder and create new one
        images_folder = os.path.join(assets_folder, image_folder_name)
        if os.path.exists(images_folder):
            shutil.rmtree(images_folder)
        os.mkdir(images_folder)

        # Write images
        for image in images:
            image_path = os.path.join(images_folder, image.split('/')[-1])
            print('Writing image : {}'.format(image))

            print(image_path)

            if image in resources['outputs']:
                data = resources['outputs'][image]
                with open(image_path, 'wb') as f:
                    f.write(data)
            else:
                shutil.copy2(os.path.join(ipynb_folder, image), image_path)
