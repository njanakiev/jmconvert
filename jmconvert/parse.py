import os
import re
import shutil
import datetime
import nbformat
import nbconvert


EXCLUDE_METADATA = ['date']


def parse(ipynb_filepath, assets_path, posts_path, overwrite=False):
    # Get filename and folder from jupyter notebook path
    ipynb_filename = os.path.splitext(os.path.basename(ipynb_filepath))[0]
    ipynb_folder = os.path.dirname(ipynb_filepath)
    image_folder_name = ipynb_filename.replace('-', '_') + "_files"
    images = []

    # Load notebook and convert to markdown
    markdown_exporter = nbconvert.MarkdownExporter()
    with open(ipynb_filepath, 'r') as f:
        nb = nbformat.reads(f.read(), as_version=4)


    # Get title from first cell and remove cell
    first_cell = nb.cells.pop(0)
    title = first_cell.source.replace('#', '').strip()

    # Generate front matter from metadata
    front_matter = "---\n"
    front_matter += "title: \"{}\"\n".format(title)
    
    # Get article metadata
    article_metadata = nb.metadata['article_metadata']

    for key, value in article_metadata.items():
        if key not in EXCLUDE_METADATA:
            if key == 'date_modified':
                front_matter += "seo:\n"
                front_matter += f"    date_modified: {value}\n"
            else:
                if key == 'image':
                    images.append(value)
                    value = '/assets/{}/{}'.format(
                        image_folder_name, value.split('/')[-1])

                front_matter += "{}: {}\n".format(key, value)
    front_matter += "---\n\n"

    print('Front matter created from metadata : ')
    print(front_matter)


    # Remove all cells marked hidden
    for cell in list(nb.cells):
        if cell.metadata and cell.metadata.get('hide', False):
            nb.cells.remove(cell)

    (body, resources) = markdown_exporter.from_notebook_node(nb)
    body = front_matter + body


    # Get current date
    if 'date' in article_metadata:
        dt = datetime.datetime.strptime(article_metadata['date'], '%Y-%m-%d')
    else:
        files = [f for f in os.listdir(posts_path) if ipynb_filename in f]
        if len(files) == 0:
            dt = datetime.datetime.now()
        elif len(files) == 1:
            dt = datetime.datetime.strptime(files[0][:10], '%Y-%m-%d')
        else:
            raise Exception(
                'Multiple files named the same way with different dates')

    markdown_filepath = os.path.join(posts_path,
        '{}-{}.md'.format(dt.strftime('%Y-%m-%d'), ipynb_filename))

    # Remove first and last line breaks
    body = body.strip()


    # Find all image links
    pattern = r'\!\[.*?\]\((.+?)\)'
    images.extend(re.findall(pattern, body))
    print('Images:', images)

    # Replace image links
    def image_replace_link(match):
        image_title, image_path = match.groups()
        return '![{}]({{{{ site.baseurl }}}}/{}/{}/{})'.format(
            image_title, "assets",
            image_folder_name, image_path.split('/')[-1])

    pattern = r'\!\[(.*?)\]\((.+?)\)'
    body = re.sub(pattern, image_replace_link, body)

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
        images_folder = os.path.join(assets_path, image_folder_name)
        if os.path.exists(images_folder):
            shutil.rmtree(images_folder)
        os.mkdir(images_folder)

        # Write images
        for image in images:
            image_path = os.path.join(images_folder, image.split('/')[-1])
            print('Writing image : {}'.format(image))
            print('Image path:', image_path)

            if image in resources['outputs']:
                data = resources['outputs'][image]
                with open(image_path, 'wb') as f:
                    f.write(data)
            else:
                shutil.copy2(os.path.join(ipynb_folder, image), image_path)
