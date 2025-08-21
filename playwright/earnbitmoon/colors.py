# file: colors.py

def clean():
    """Tạo biến màu global cho terminal"""
    colors = {
        "reset": "\033[0m",
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",

        # bright
        "lblack": "\033[90m",
        "lred": "\033[91m",
        "lgreen": "\033[92m",
        "lyellow": "\033[93m",
        "lblue": "\033[94m",
        "lmagenta": "\033[95m",
        "lcyan": "\033[96m",
        "lwhite": "\033[97m",

        # style
        "bold": "\033[1m",
        "underline": "\033[4m",
        "reverse": "\033[7m"
    }

    globals().update(colors)  # tạo biến global


# gọi 1 lần để public biến màu
clean()
