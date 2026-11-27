import os
import sys

from copystatic import cleanup_public, copy_static_to_public
from generate_page import generate_pages_recursive

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"
destination = (os.path.realpath("docs"))
source = (os.path.realpath("static"))
from_dir_path = (os.path.realpath("content"))
template_path = (os.path.realpath("template.html"))
dest_dir_path = (os.path.realpath("docs"))
def main():
    cleanup_public(destination)
    copy_static_to_public(source, destination)
    generate_pages_recursive(basepath, from_dir_path, template_path, dest_dir_path)


if __name__ == "__main__":
    main()
