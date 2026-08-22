from textnode import TextNode
from htmlnode import markdown_to_html_node, remove_heading_prefix
import os
import shutil
import re
import sys

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):
    if dest_dir_path.endswith(".md"):
        dest_dir_path = dest_dir_path.replace(".md", ".html")
    if os.path.isfile(dir_path_content) and dir_path_content.endswith(".md"):
        generate_page(dir_path_content, template_path, dest_dir_path, basepath)
        return 

    entries = os.listdir(dir_path_content)

    for entry in entries:
        if os.path.isfile(dir_path_content) and dir_path_content.endswith(".md"):
            generate_page(dir_path_content, template_path, dest_dir_path, basepath)
        else:
            if not os.path.exists(dest_dir_path):
                os.mkdir(dest_dir_path)
            generate_pages_recursive(os.path.join(dir_path_content, entry), template_path,  os.path.join(dest_dir_path, entry), basepath)


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
            paths = (dest_path.split('/'))
            for i in range(len(paths) - 1):
                if not os.path.exists(paths[i]):
                    os.mkdir(paths[i])  
            with open(dest_path, "w") as dest:
                dest.write(template_content)
            

def extract_title(markdown: str) -> str:
    if not markdown.startswith("#"):
        return "My static page"
    return remove_heading_prefix(markdown.splitlines()[0])

def copy_to_dest(src: str, dest: str):
    if os.path.isfile(src):
        print(f"copying {src} to {dest}")
        shutil.copy(src, dest)
        return 

    entries = os.listdir(src)

    for entry in entries:
        if os.path.isfile(src):
            print(f"copying {src} to {dest}")
            shutil.copy(src, dest)
        else:
            if not os.path.exists(dest):
                os.mkdir(dest)
            copy_to_dest(os.path.join(src, entry), os.path.join(dest, entry))
    

def main():
    basepath: str
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    src: str = "static"
    dest: str = "docs"
    shutil.rmtree(dest)
    copy_to_dest(src, dest)
    dir_path_content: str = "content"
    template_path: str = "temlate.html"
    dest_dir_path: str = dest
    # shutil.rmtree(dest_dir_path)
    generate_pages_recursive("content", "template.html", "public", basepath)
    
    

main()
