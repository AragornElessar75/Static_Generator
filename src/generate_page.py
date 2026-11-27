import os
from pathlib import Path

from block_markdown import markdown_to_html_node
from extract_title import extract_title


def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)

def generate_pages_recursive(basepath, from_dir_path, template_path, dest_dir_path):
    contents = os.listdir(from_dir_path)
    for content in contents:
        content_path = os.path.join(from_dir_path, content)
        dir_path = os.path.join(dest_dir_path, content)
        if os.path.isfile(content_path):
            html_path = Path(dir_path).with_suffix(".html")
            generate_page(basepath, content_path, template_path, html_path)
        if os.path.isdir(content_path):
            os.mkdir(dir_path)
            generate_pages_recursive(basepath, content_path, template_path, dir_path)
