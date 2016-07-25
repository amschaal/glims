from django.conf import settings
from django.utils._os import safe_join
import os
def is_sub_path(path,subpath):
    return subpath.startswith(path) and path != subpath
# remove_sub_paths(['/foo','/foo/bar','/baz/blah','/baz']) returns ['/foo', '/baz']
def remove_sub_paths(paths,path=None):
    if len(paths) == 0:
        return paths
    if path is None:
        paths = list(set(paths))
    path = path or paths[0]
    paths = [p for p in paths if not is_sub_path(path,p)]
    index = paths.index(path) + 1
    if index >= len(paths):
        return paths
    return remove_sub_paths(paths,paths[index])

def is_linked(project_root,project_share_root,subpath):
    share_path = safe_join(project_share_root,subpath)
    if not os.path.exists(share_path):
        return False
    file_path = safe_join(project_root,subpath)
    if os.path.realpath(file_path) != os.path.realpath(share_path):
        return False

"""
Recursively crawl file path and check if any real files (not directories) exist.  Any symlinks encountered are ignored.
If a path contains no real files
"""
def get_real_files(path,relpath=True):
    if not os.path.isdir(path):
        raise Exception("Path: '%s' is not a directory"%path)
    real_files = []
    for name in os.listdir(path):
        full_path = os.path.join(path,name)
        if not os.path.islink(full_path):
            if os.path.isfile(full_path):
                real_files.append(full_path)
            if os.path.isdir(full_path):
                real_files += get_real_files(full_path,False)
    if relpath:
        real_files = [os.path.relpath(file_path, path) for file_path in real_files]
    return real_files

def get_symlinks(path,relpath=True):
    if not os.path.isdir(path):
        raise Exception("Path: '%s' is not a directory"%path)
    symlinks = []
    for name in os.listdir(path):
        full_path = os.path.join(path,name)
        if os.path.islink(full_path):
            symlinks.append(full_path)
        else:    
            if os.path.isdir(full_path):
                symlinks += get_symlinks(full_path,False)
    if relpath:
        symlinks = [os.path.relpath(symlink, path) for symlink in symlinks]
    return symlinks

