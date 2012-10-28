#!/usr/bin/env python

import cgi

# Local Settings needs to be written to provide
# URL listings. See README for details
import local_settings
import util

categories = util.extract_categories(local_settings.urls)

print('Content-type: text/html\n')

form = cgi.FieldStorage()
id = form.getfirst("id",None)
category = form.getfirst("cat",None)

if id:
	if not id.isdigit():
		id = "0"
	id = int(id)
	if id > len(local_settings.urls):
		id = 0
		show_categories = True

import locale
try:
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_parts


import os.path  as OP
base_dir = ".."

# TODO Sort for unique category_str values. Then display only those.
if id != None:
	filename = local_settings.urls[id]
	rst_file = open(OP.join(base_dir,filename),"r")
	parts = publish_parts(rst_file.read(),writer_name='html')
	parts['footer'] = "<div class=\"footer\"><p>Source: <a href=\"%s\">%s</a>  "  % (OP.join(base_dir,filename),filename)
	the_category = local_settings.filename2category(filename)
	if the_category:
		parts['footer'] += "Category: <a href=\"render.cgi?cat=%s\">%s</a> " % (the_category,the_category)
	
	parts['footer'] += "</div>\n"

if category or id == None:
	if id == 0 and local_settings.urls:
		parts = publish_parts(open(OP.join(base_dir,local_settings.urls[id]),"r"),writer_name="html")
	else:
		parts = publish_parts("",writer_name='html')
	if not category:
		parts['fragment'] = "<h1>Categories</h1>\n"
	else:
		parts['fragment'] = "<h1>Category</h1>\n"
	for i in categories:
		if category and category != i:
			continue
		parts['fragment'] += "<p>%s</p>\n" % i
		parts['fragment'] += "<ul>\n"
		for entry in categories[i]:
			basefilename = entry[0]
			if "/" in basefilename:
				basefilename = basefilename[basefilename.rfind("/")+1:]
			if len(basefilename) >= 4 and basefilename[-4:] == ".rst":
				basefilename = basefilename[:-4]
			parts['fragment'] += "<li><a href=\"render.cgi?id=%s\">%s</a></li>\n" % (entry[1],basefilename)
		parts['fragment'] += "</ul>\n"


for part in ['head_prefix','html_head','stylesheet','body_prefix','html_title','fragment','footer','body_suffix']:
	if part == 'html_head':
		print(parts[part] % "utf-8")
	else:
		print(parts[part])

