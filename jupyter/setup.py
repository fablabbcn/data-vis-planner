# -*- encoding: utf-8 -*-

import os
import fileinput
import hashlib
import random
from ipython_genutils.py3compat import cast_bytes, str_to_bytes

# Get the password from the environment
password_environment_variable = os.environ.get('JUPYTER_PASSWORD')

# Hash the password, this is taken from https://github.com/jupyter/notebook/blob/master/notebook/auth/security.py
salt_len = 12
algorithm = 'sha1'
h = hashlib.new(algorithm)
salt = ('%0' + str(salt_len) + 'x') % random.getrandbits(4 * salt_len)
h.update(cast_bytes(password_environment_variable, 'utf-8') + str_to_bytes(salt, 'ascii'))
password = ':'.join((algorithm, salt, h.hexdigest()))

# Store the password in the configuration
setup_line = "#c.NotebookApp.password = ''"
new_setup_line = setup_line.replace("''", "u'" + password + "'")
new_setup_line = new_setup_line.replace("#", "")
setup_file = os.getenv("HOME") + "/.jupyter/jupyter_notebook_config.py"

for line in fileinput.input(setup_file, inplace=True):
    print line.replace(setup_line, new_setup_line),

for line in fileinput.input(setup_file, inplace=True):
    print line.replace("#c.NotebookApp.password_required = False", "c.NotebookApp.password_required = True"),
