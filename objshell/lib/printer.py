import sys
import ctypes

kernel32 = ctypes.windll.kernel32

# Init the color var
FOREGROUND_BLUE = 0x01 # text color contains blue.  
FOREGROUND_GREEN= 0x02 # text color contains green.  
FOREGROUND_RED = 0x04 # text color contains red.  
FOREGROUND_INTENSITY = 0x08 # text color is intensified.
FOREGROUND_WHITE = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE

# Init the stat
OK = FOREGROUND_GREEN
ERROR = FOREGROUND_RED
NONE = FOREGROUND_WHITE

# Init the handler
STD_OUTPUT_HANDLE= -11
_soh = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def _reset():
    """Resets color to white"""
    kernel32.SetConsoleTextAttribute(_soh, NONE)

def output(text, stat = NONE):
    """The main function for printing information with color.
    
    Args:
        text: the input text
        stat: the stat of the output can be chosen from

            printer.OK
            printer.ERROR
            printer.NONE
    """
    kernel32.SetConsoleTextAttribute(_soh, stat|FOREGROUND_INTENSITY)
    print text
    _reset()