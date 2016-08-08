import re
def make_directory_name(name):
    return re.sub(r'\W+', '', name.replace(' ','_'))