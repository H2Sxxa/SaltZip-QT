from os import unlink
from os.path import dirname
import pathlib
def combinefile(filepath):
    filenames = map_glob(glob_files(filepath))
    with open('%s/result'%dirname(filepath), 'ab') as outfile:  # append in binary mode
        for fname in filenames:
            with open(fname, 'rb') as infile:        # open in binary mode also
                outfile.write(infile.read())

def glob_files(basename):
    if isinstance(basename, str):
        basename = pathlib.Path(basename)
    files = basename.parent.glob(basename.name + ".*")
    return sorted(files)

def map_glob(files_list):
    return list(map(sort_path,files_list))

def sort_path(filepath):
    return "%s\\%s" % (filepath.parent,filepath.name)