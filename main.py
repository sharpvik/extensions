#!/usr/bin/python3
import os, eel
import json, jsonio
from sys import argv
from path import Path, Dir, File



# globals
S = os.sep
HOME = f'{S}home{S}sharpvik'
FLAGS = set()
CONFIG_FILE = File(f'{HOME}{S}Projects{S}extensions{S}config.json')
CONFIG = dict()



# util
def log(msg):
    print(f'LOG: {msg}')

def match_ignored_extentions(file):
    ext = set( file.get_ext() )
    ignored = set( CONFIG["ignored extentions"] )
    return not ext.isdisjoint(ignored)



eel.init('web', allowed_extensions=['.js', '.css', '.html'])



@eel.expose
def set_recursive(r):
    CONFIG['recursive'] = r

@eel.expose
def analyse( dir=os.getcwd(), ext=dict(), ttl=0 ):
    # make sure argument values don't carry through the recursive call
    dir = Dir(dir)
    ext = dict(ext)
    ttl = int(ttl)

    log(f'Looking through {str}')

    for item in dir.contents():
        """
        The dir.contents() function returns a list of path.Dirs and path.Files.
        Use item._type() to retrieve item's type.
        """

        # account for if item is a file
        if item._type() == 'file':
            file = item
            if CONFIG["ignore multisuffix files"] \
               and len( file.get_ext() ) > 1 \
               or CONFIG["ignore extentionles files"] \
               and len( file.get_ext() ) == 0 \
               or match_ignored_extentions(file):
                log( str(file) + ' is invalid. Skipping...' )
                continue
            log(f'{file} discovered and accounted for.')
            suf = file.get_suffix()
            if suf not in ext:
                ext[suf] = 1
            else:
                ext[suf] += 1
            ttl += 1
            continue

        # recursive call to analyse if item is a folder
        if item._type() == 'dir':
            test_dir = item
            if CONFIG['recursive'] and \
               test_dir.get_name() not in CONFIG["ignored directories"]:
                log(f'{test_dir} discovered. Opening...')
                ext, ttl = analyse( test_dir.get_str_path(), ext, ttl )
            else:
                log(
                    str(test_dir) + \
                    (' discovered, but -r (recursive) flag not set.' \
                    if not CONFIG['recursive'] \
                    else ' discovered, but it is an ignored directory.') + \
                    ' Skipping...'
                )

    log(f'Escaping {dir}...')
    log(
        f'Results:\n{ttl} files in total\n' + \
        f'{json.dumps(ext, sort_keys=True, indent=4)}'
    )

    return ext, ttl



if __name__ == '__main__':
    FLAGS = set(argv[1:])
    CONFIG = jsonio.decode(CONFIG_FILE)
    eel.start( 'index.html', size=(1300, 800) )
