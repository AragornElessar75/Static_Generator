import os
import shutil


def cleanup_public(destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

def copy_static_to_public(source, destination):
    static_dir = source
    public_dir = destination
    contents = os.listdir(static_dir)
    for content in contents:
        content_path = os.path.join(static_dir, content)
        if os.path.isfile(content_path):
            shutil.copy(content_path, public_dir)
        if os.path.isdir(content_path):
            dir_path = os.path.join(public_dir, content)
            os.mkdir(dir_path)
            copy_static_to_public(content_path, dir_path)
