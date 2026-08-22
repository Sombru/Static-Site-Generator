from textnode import TextNode
from htmlnode import markdown_to_html_node, remove_heading_prefix
import os
import shutil
import re

def generate_page(from_path, template_path, dest_path: str):
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        content = file.read()
        with open(template_path) as template:
            template_content = template.read()
            html = markdown_to_html_node(content).to_html()
            title = extract_title(content)
            template_content = template_content.replace("{{ Title }}", title)
            template_content = template_content.replace("{{ Content }}", html)
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
    print(src, dest)
    print(entries)
    for entry in entries:
        if os.path.isfile(src):
            print(f"copying {src} to {dest}")
            shutil.copy(src, dest)
        else:
            if not os.path.exists(dest):
                os.mkdir(dest)
            copy_to_dest(os.path.join(src, entry), os.path.join(dest, entry))
    

def main():
    copy_to_dest("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
main()
