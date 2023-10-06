# Python 3
def color_code(code): return f"\x1b[{code}m"
def colorize(code: int, s: str) -> str: return f"{color_code(code)}{str(s).replace(color_code(0), color_code(code))}{color_code(0)}"
def green(s: str) -> str: return colorize(32, s)
def yellow(s: str) -> str: return colorize(33, s)
def blue(s: str) -> str: return colorize(34, s)
def red(s: str) -> str: return colorize(31, s)
def cyan(s: str) -> str: return colorize(36, s)
def magenta(s: str) -> str: return colorize(35, s)
def bold(s: str) -> str: return colorize(1, s)
def info_log(*strs: str) -> None:
    for s in strs: print(yellow(s))
def warning_log(*strs: str) -> None:
    for s in strs: print(bold(yellow(s)))
def success_log(*strs: str) -> None:
    for s in strs: print(green(s))
def error_log(*strs: str) -> None:
    for s in strs: print(red(s))
