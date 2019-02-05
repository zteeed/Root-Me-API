#!/usr/bin/python3
def grey(msg): 
    print('\033[90m[!] {}\033[00m' .format(msg))
def red(msg): 
    print('\033[91m[!] {}\033[00m' .format(msg))
def green(msg): 
    print('\033[92m[+] {}\033[00m' .format(msg))
def yellow(msg): 
    print('\033[93m[+] {}\033[00m' .format(msg))
def blue(msg): 
    print('\033[94m[*] {}\033[00m' .format(msg))
def purple(msg): 
    print('\033[95m[*] {}\033[00m' .format(msg))
def cyan(msg): 
    print('\033[96m[*] {}\033[00m' .format(msg))
