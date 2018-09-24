# @file dexell.py

import argparse
import ctypes
import os
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
        args = ['c++filt', self.name]
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = proc.communicate()
        return stdout.strip()

    
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
    parser.add_argument('binary', type=os.path.abspath)
    parser.add_argument('symbol')
    inputs = parser.parse_args(argv)

    binary = Binary(inputs.binary)
    binary.execute_symbol(inputs.symbol)
    

if __name__ == '__main__':
    run(sys.argv[1:])
