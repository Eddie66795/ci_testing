# Simple Python Jinja2 Script for string replacement (primarily for docker compose files)
# Expects to be executed in the following fashion:

# python variable_replacer.py [FILE_PATH] [VARIABLE] [REPLACEMENT]

# WHERE:
#
# FILE_PATH = The path to the file that you want to modify
#     *Can be just the file name if the file is in the current folder, or full path)
#    *Syntax such as "../docker-compose.yml" can be used
# VARIABLE = Variable you have placed in the file in Jinja2 convention '{{ VARIABLE_NAME }}'
# REPLACEMENT = String you want to replace the variable above with.
# MULTIPLE VARIABLES AND REPLACEMENTS WILL WORK, SIMPLY LIST ONE AFTER ANOTHER

import os
import sys
from jinja2 import Environment, FileSystemLoader, Template
variables = sys.argv[2::2]
values = sys.argv[3::2]
dict = dict(zip(variables, values))

file_path_input = (sys.argv[1])
full_path = os.path.abspath(file_path_input)
j2_env = Environment(loader=FileSystemLoader('%s' %
                                             (full_path)), trim_blocks=True)
output = (j2_env.get_template("").render(dict))
os.remove(full_path)
file = open(full_path, "w")
file.write(output)
