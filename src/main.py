from textnode import TextNode
from htmlnode import markdown_to_html_node, remove_heading_prefix
import os
import shutil
import re
import sys

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):
    if os.path.isfile(dir_path_content):
        if dir_path_content.endswith(".md"):
            html_path = os.path.splitext(dest_dir_path)[0] + ".html"
            generate_page(dir_path_content, template_path, html_path, basepath)
        return

    os.makedirs(dest_dir_path, exist_ok=True)
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        destination_path = os.path.join(dest_dir_path, entry)
        generate_pages_recursive(source_path, template_path, destination_path, basepath)


def generate_page(from_path, template_path, dest_path: str, basepath: str):
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        content = file.read()
        with open(template_path) as template:
            template_content = template.read()
            html = markdown_to_html_node(content).to_html()
            title = extract_title(content)
            template_content = template_content.replace("{{ Title }}", title)
            template_content = template_content.replace("{{ Content }}", html)
            template_content = template_content.replace('href="/', f'href="{basepath}')
            template_content = template_content.replace('src="/', f'src="{basepath}')
            parent_dir = os.path.dirname(dest_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            with open(dest_path, "w") as dest:
                dest.write(template_content)
            

def extract_title(markdown: str) -> str:
    if not markdown.startswith("#"):
        return "My static page"
    return remove_heading_prefix(markdown.splitlines()[0])

def copy_to_dest(src: str, dest: str):
    os.makedirs(dest, exist_ok=True)
    if os.path.isfile(src):
        shutil.copy(src, dest)
        return 

    entries = os.listdir(src)

    for entry in entries:
        source_path = os.path.join(src, entry)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest)
        else:
            copy_to_dest(source_path, os.path.join(dest, entry))

def main():
    basepath: str
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    src: str = "static"
    dest: str = "docs"
    try:
        shutil.rmtree(dest)
    except Exception as e:
        print(e)
    copy_to_dest(src, dest)
    dir_path_content: str = "content"
    template_path: str = "template.html"
    dest_dir_path: str = dest
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath)
    
    

main()
