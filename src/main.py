import os

from copystatic import cleanup_public, copy_static_to_public
from generate_page import generate_pages_recursive

destination = (os.path.realpath("public"))
source = (os.path.realpath("static"))
dir_path_content = (os.path.realpath("content"))
template_path = (os.path.realpath("template.html"))
dest_dir_path = (os.path.realpath("public"))
def main():
    cleanup_public(destination)
    copy_static_to_public(source, destination)
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)


if __name__ == "__main__":
    main()
