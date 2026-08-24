import os
import shutil
import sys
from blocks import markdown_to_html_node
from textnode import TextNode, TextType

content_dir_path = 'content/'
public_dir_path = 'docs/'
static_dir_path = 'static/'
template_path = 'template.html'

def main():

    basepath = '/'

    if len(sys.argv) == 2:
        basepath = sys.argv[1]

    if os.path.exists(public_dir_path):
        shutil.rmtree(public_dir_path)
    
    os.mkdir(public_dir_path)

    copy_content(static_dir_path, public_dir_path)

    generate_pages_recursive(content_dir_path, template_path, public_dir_path, basepath)

#-----------------------------------------------------------------

def copy_content(source: str, destination: str) -> None:

    if os.path.exists(source):
        dirs = os.listdir(source)
        #print(dirs)
        for item in dirs:
            item_path = os.path.join(source, item)
            if not os.path.isdir(item_path):
                shutil.copy(item_path, destination)
                print(f"{item} copied to {destination}")
            else:
                new_directory = os.path.join(destination, item)
                os.mkdir(new_directory)
                print(f"New directory {new_directory} created")
                copy_content(item_path, new_directory)

def extract_title(markdown: str):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line[2:].strip()
    raise ValueError("Title not found")

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = str()
    html_template = str()

    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        html_template = file.read()

    title = extract_title(markdown)

    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()

    add_title = html_template.replace('{{ Title }}', title)
    complete_page = add_title.replace('{{ Content }}', html_string)
    complete_page = complete_page.replace('href="/', f'href="{basepath}')
    complete_page = complete_page.replace('src="/', f'src="{basepath}')

    #if not os.path.exists(dest_path):
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(complete_page)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):

    if os.path.exists(dir_path_content):
        dirs = os.listdir(dir_path_content)
        for item in dirs:
            item_path = os.path.join(dir_path_content, item)
            if not os.path.isdir(item_path):
                if item.endswith(".md"):
                    generate_page(item_path, template_path, os.path.join(dest_dir_path, item.replace(".md", ".html")), basepath)
                else:
                    continue
            else:
                generate_pages_recursive(item_path, template_path, os.path.join(dest_dir_path, item), basepath)


main()