import os
import sys
import inspect
import getpass
import json
import traceback
import lib.printer as printer

commands = []

def command(f):
    """command decorator used for wrapping commands"""
    def wrapper(*args):
        # print args
        try:
            r = f(*args)
            if r:
                printer.output("DONE: ", printer.OK)
        except Exception, e:
            traceback.print_exc(file = sys.stdout)
            printer.output(e, printer.ERROR)
    wrapper.__name__ = f.__name__ # pass the name of the function
    wrapper.__doc__ = f.__doc__ # pass the docstring 

    _args = inspect.getargspec(f).args
    _args = _args if _args else []
    _varargs = inspect.getargspec(f).varargs
    _varargs = [_varargs] if _varargs else []

    arr = ' '.join([a.upper() for a in _args + _varargs])
    wrapper.__args__ = arr
    commands.append(wrapper)
    return wrapper

# -----------------------------------------------------------------------------
# below part is commands definition. function with @command decorator would 
# be considered as a command, the wrapped command function object will be
# put into a commands list, then be turned to a dictionary { name: func-obj }
# thus the shell can easily find out the command object from the command list
# to get all the information about each one ( eg: name, args, doc, etc )

@command
def test(parm):
    return "OK"


# puts collected commands into a dictionary.
cmd_dict = {}
for c in commands:
    cmd_dict[c.__name__] = c

# command definition overs here. 
# -----------------------------------------------------------------------------

def get_cmd_args(input):
    """Retuns cmd and its args from the input string.
    
    Args:
        input: the input string captured from the command line.

    Returns:
        (command, args[])
    """
    arr = input.split(' ', 1)
    if arr.__len__() == 1:
        cmd, args = arr[0], []
    elif arr.__len__() == 2:
        cmd, args = arr
        args = args.split(' ')
    else:
        cmd, args = None, []
    return cmd, args

def exc_batch(script_content):
    """Executes the command from the script file.

    The script content can be a set of commands that are runnable from the 
    shell. the content comes from a file which contains those command set.

    Args:
        script_content: the script info
    """
    for input in [ln for ln in script_content.split('\n') if ln]:
        cmd, args = get_cmd_args(input)
        cmd_dict[cmd].__call__(*args)



# print welcome header
printer.output("****************************************", printer.OK)
printer.output("Welcome to the shell", printer.OK)
printer.output("****************************************", printer.OK)

# command capture
while True:
    input = raw_input('$ ')
    cmd, args = get_cmd_args(input)
    if cmd == 'q':
        break
    if cmd == '@': # execute batch file.
        collection = []
        for p5script in args:
            with open(p5script, 'r') as f:
                exc_batch(f.read())
    elif cmd_dict.has_key(cmd):
        cmd_dict[cmd].__call__(*args)
    else:
        R.printc("Command not found, type 'help' to see more info")

