def grey(msg: str) -> None:
    print(f'\033[90m[!] {msg}\033[00m')


def red(msg: str) -> None:
    print(f'\033[91m[!] {msg}\033[00m')


def green(msg: str) -> None:
    print(f'\033[92m[+] {msg}\033[00m')


def yellow(msg: str) -> None:
    print(f'\033[93m[+] {msg}\033[00m')


def blue(msg: str) -> None:
    print(f'\033[94m[*] {msg}\033[00m')


def purple(msg: str) -> None:
    print(f'\033[95m[*] {msg}\033[00m')


def cyan(msg: str) -> None:
    print(f'\033[96m[*] {msg}\033[00m')
