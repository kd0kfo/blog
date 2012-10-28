#!/usr/bin/env python

import cgi

# Local Settings needs to be written to provide
# URL listings. See README for details
import local_settings

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

from docutils.core import publish_parts


import os.path  as OP
base_dir = ".."
filename = local_settings.urls[int(id)]
rst_file = open(OP.join(base_dir,filename))
#publish_file(rst_file,writer_name='html')

parts = publish_parts(rst_file.read(),writer_name='html')

parts['footer'] = "<div class=\"footer\">Source: <a href=\"%s\">%s</a>"  % (OP.join(base_dir,filename),filename)

for part in ['head_prefix','html_head','stylesheet','html_body','footer','body_suffix']:
	print(parts[part])

