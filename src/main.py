import os

from copystatic import cleanup_public, copy_static_to_public

destination = (os.path.realpath("public"))
source = (os.path.realpath("static"))
def main():
    cleanup_public(destination)
    copy_static_to_public(source, destination)

if __name__ == "__main__":
    main()
