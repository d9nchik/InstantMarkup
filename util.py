import re
import sys
import webbrowser


def html_file_opener(html_file_name):
    sys_argv_ = sys.argv[0]
    sys_argv_ = sys_argv_[:re.search("[^/]+$", sys_argv_).start()]
    webbrowser.open_new_tab(sys_argv_ + html_file_name)


def lines(file):
    for line in file:
        yield line
    yield '\n'


def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []
