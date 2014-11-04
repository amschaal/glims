'''
Write an abstract interface for sharing files + directories to users or via random URLs

implementations for:
-Bioshare
-AWS S3?
-IRODS?
-Google Drive?
-Box.com?

Share
-------
@static
create_share()
    return share
@static
get_share(id)
    return share
get_url()
    return share_url #May be public, or require login
add_files(paths=[],subpath='')
    return URL
add_directories(paths=[],subpath='')
    return URL
create_directory(path)
    return URL
delete_path(path)
    return status




BioShare(Share)
---------------
add_files(paths=[],subpath='',symlink=False)
add_directories(paths=[],subpath='',symlink=False)

'''

