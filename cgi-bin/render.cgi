#!/usr/bin/env python

def render_rst(id = None, category = None):

	# Local Settings needs to be written to provide
	# URL listings. See README for details
	import local_settings
	import util

	categories = util.extract_categories(local_settings.urls)

	print('Content-type: text/html\n')
	if id:
		if not id.isdigit():
			id = "0"
		id = int(id)
		if id > len(local_settings.urls):
			id = None

	import locale
	try:
	    locale.setlocale(locale.LC_ALL, '')
	except:
	    pass

	from docutils.core import publish_parts

	import os.path  as OP
	base_dir = ".."
	filename = ""

	# TODO Sort for unique category_str values. Then display only those.
	if id != None:
		filename = local_settings.urls[id]
		if OP.isfile(OP.join(base_dir,filename)):
			rst_file = open(OP.join(base_dir,filename),"r")
			parts = publish_parts(rst_file.read(),writer_name='html')
		else:
			parts = publish_parts("File Not Found",writer_name='html')
		parts['footer'] = "<p>Source: <a href=\"%s\">%s</a></p>\n"  % (OP.join(base_dir,filename),filename)
		the_category = util.filename2category(filename)
		if the_category:
			parts['footer'] += "Category: <a href=\"render.cgi?cat=%s\">%s</a> " % (the_category,the_category)
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
		elif part == 'stylesheet':
			if local_settings.stylesheet:
				print("<link rel=\"stylesheet\" href=\"%s\" type=\"text/css\"/>\n" % local_settings.stylesheet)
			print(parts[part])
		elif part == 'footer':
			import os, time
			print("<div class=\"footer\">")
			print(parts['footer'])
			if local_settings.footer:
				print(local_settings.footer)
			if filename and OP.isfile(OP.join(base_dir,filename)):
						(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(OP.join(base_dir,filename))
						print("last modified: %s %s" % (time.ctime(mtime),time.tzname[0]))
			print("</div>\n")
		else:
			print(parts[part])

	# end of render_rst

if __name__ == "__main__":
	import cgi
	form = cgi.FieldStorage()
	id = form.getfirst("id",None)
	category = form.getfirst("cat",None)

	render_rst(id,category)
