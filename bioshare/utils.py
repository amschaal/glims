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
    