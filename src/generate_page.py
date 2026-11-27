import os
from pathlib import Path

from block_markdown import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    for content in contents:
        content_path = os.path.join(dir_path_content, content)
        dir_path = os.path.join(dest_dir_path, content)
        if os.path.isfile(content_path):
            html_path = Path(dir_path).with_suffix(".html")
            generate_page(content_path, template_path, html_path)
        if os.path.isdir(content_path):
            os.mkdir(dir_path)
            generate_pages_recursive(content_path, template_path, dir_path)
