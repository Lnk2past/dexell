# @file dexell.py

import argparse
import ctypes
import subprocess
import sys


class Symbol():
    def __init__(self, _radix, _sym_type, _name):
        self.radix = _radix
        self.sym_type = _sym_type
        self.name = _name
        self.dname = self.demangle()

    
    def __str__(self):
        return '{} {} {}'.format(self.radix, self.sym_type, self.name)


    def demangle(self):
        status = ctypes.c_int()
        lib = ctypes.CDLL('libc++abi.so.1.0')
        func = getattr(lib, '__cxa_demangle')
        name = ctypes.c_char_p(self.name.encode())
        func.argtypes = [ctypes.c_char_p, ctypes.c_char, ctypes.c_size_t, ctypes.c_void_p]
        func.restype = ctypes.c_char_p
        d = func(name, 0, 0, ctypes.byref(status))
        if status.value == 0:
            return d.decode()

    
class Binary():
    def __init__(self, _path):
        self.path = _path
        self.symbols = self.load_symbols(_path)
        self.binary = ctypes.CDLL(_path)

    def load_symbols(self, binary):
        args = ['nm', binary]
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = proc.communicate()
       
        symbols = {}
        for entry in stdout.splitlines():
            entry = entry.split()
            if len(entry) == 2:
                radix = ''
                sym_type, name = entry
            else:
                radix, sym_type, name = entry

            symbol = Symbol(radix, sym_type, name)
            symbols[symbol.dname] = symbol

        return symbols


    def execute_symbol(self, _name, *args):
        function = getattr(self.binary, self.symbols[_name].name)
        function()
        

def run(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('binary')
    parser.add_argument('symbol')
    inputs = parser.parse_args(argv)

    binary = Binary(inputs.binary)
    print(binary.symbols)
    binary.execute_symbol(inputs.symbol)
    

if __name__ == '__main__':
    run(sys.argv[1:])