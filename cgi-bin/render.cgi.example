#!/usr/bin/env python

import cgi

print('Content-type: text/html\n')

form = cgi.FieldStorage()
id = form.getfirst("id","0")

if not id.isdigit():
	id = "0"

import locale
try:
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_file, Publisher, default_description

urls = {}
urls[0] = "test.rst"
urls[1] = "science/conversion_factors.rst"

import os.path  as OP
base_dir = ".."
rst_file = open(OP.join(base_dir,urls[int(id)]))
publish_file(rst_file,writer_name='html')
