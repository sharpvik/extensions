import os

class Path:
    def __init__(self, strpath):
        self.strpath = strpath if strpath[-1] != os.sep else strpath[:-1]

    def exists(self):
        return os.path.exists(self.strpath)

    def isdir(self):
        return os.path.isdir(self.strpath)

    def isfile(self):
        return os.path.isfile(self.strpath)

    def __add__(self, other):
        return Path(self.strpath + os.sep + other)

    def __str__(self):
        return self.strpath



class Dir:
    def __init__(self, strpath):
        self.path = Path(strpath)
        self.name = self.get_str_path().split(os.sep)[-1]

    def get_path(self):
        return self.path

    def get_str_path(self):
        return str(self.path)

    def get_name(self):
        return self.name

    def contents(self):
        c = list()
        for item in os.listdir( self.get_str_path() ):
            test_path = self.get_path() + item
            if test_path.isfile():
                c.append(  File( str(test_path) )  )
            elif test_path.isdir():
                c.append(  Dir( str(test_path) )  )
        return c

    def _type(self):
        return 'dir'

    def __str__(self):
        return f'<Dir: {self.name}>'



class File:
    def __init__(self, strpath):
        self.path = Path(strpath)
        fullname = strpath.split(os.sep)[-1].split('.')
        self.name = fullname[0]
        self.ext = [ each.lower() for each in fullname[1:] ]
        self.suffix = '.'.join( self.get_ext() ) if len( self.get_ext() ) > 0 \
                      else ''

    def get_path(self):
        return self.path

    def get_str_path(self):
        return str(self.path)

    def get_ext(self):
        return self.ext

    def get_suffix(self):
        return self.suffix

    def _type(self):
        return 'file'

    def read(self, mode):
        return open( self.get_str_path(), mode ).read()

    def __str__(self):
        return f'<File: {self.name}.{self.suffix}>' if self.suffix != '' else \
               f'<File: {self.name}>'
