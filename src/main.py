import shutil
import os
from pathlib import Path
from convert_markdown import markdown_to_html_node, extract_title

#recursive helper function for copy_all
def copy_all_helper(source, target):
    if not os.path.exists(target):
        os.mkdir(target)
    for item in os.listdir(source):
        path_from = f"{source}/{item}"
        if os.path.isfile(path_from):
            shutil.copy2(path_from, target)
        else: #item should be a directory
            path_to = f"{target}/{item}"
            os.mkdir(path_to)
            copy_all_helper(path_from, path_to)

#recursively copies all files and subdirectories from source dir to target dir
def copy_all(source, target):
    if not os.path.exists(source):
        raise Exception(f"invalid source path: {source}")
    if os.path.exists(target):
        shutil.rmtree(target)
    copy_all_helper(source, target)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, encoding="utf-8") as content_file: 
        with open(template_path, encoding="utf-8") as template_file:
            content = content_file.read()
            template = template_file.read()
            heading = extract_title(content)
            content_html = markdown_to_html_node(content).to_html()
            result = template.replace("{{ Title }}", heading)
            result = result.replace("{{ Content }}", content_html)
            print(f"test: from {from_path}, to {dest_path}")
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            basename = os.path.basename(from_path).replace(".md", ".html")
            with open(os.path.join(dest_path, basename), "w", encoding="utf-8") as dest_file:
                dest_file.write(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.isdir(dir_path_content): 
        raise Exception("dir_path_content must be a folder")
    for item in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, item)
        if os.path.isdir(path):
            generate_pages_recursive(path, template_path, dest_dir_path + "/" + item)
        else:
            generate_page(path, template_path, dest_dir_path)


def main():
    copy_all("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()