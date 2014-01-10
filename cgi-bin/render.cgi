#!/usr/bin/env python


def lookup_val(val):
	from local_settings import urls

	for entry_id in urls:
		url = urls[entry_id]
		unique_name = url.split(".")[0]
		if unique_name == val:
			return entry_id

	return None


def render_rst(entry_id = None, category = None):

	# Local Settings needs to be written to provide
	# URL listings. See README for details
	import local_settings
	import util

	categories = util.extract_categories(local_settings.urls)

	print('Content-type: text/html\n')
	if entry_id != None:
		if not entry_id.isdigit():
			id_from_val = lookup_val(entry_id)
			if id_from_val is not None:
				entry_id = id_from_val
			else:
				entry_id = "0"
		entry_id = int(entry_id)
		if entry_id > len(local_settings.urls):
			entry_id = None

	import locale
	try:
	    locale.setlocale(locale.LC_ALL, '')
	except:
	    pass

	from docutils.core import publish_parts

	import os.path  as OP
	base_dir = local_settings.base_dir
	filename = ""

	# TODO Sort for unique category_str values. Then display only those.
	if entry_id != None:
		filename = local_settings.urls[entry_id]
		if OP.isfile(OP.join(base_dir,filename)):
			rst_file = open(OP.join(base_dir,filename),"r")
			parts = publish_parts(rst_file.read(),writer_name='html')
		else:
			parts = publish_parts("File Not Found",writer_name='html')
		parts['footer'] = "<p>Source: <a href=\"/%s\">%s</a></p>\n"  % (OP.join(base_dir,filename),filename)
		the_category = util.filename2category(filename)
		if the_category:
			parts['footer'] += "Category: <a href=\"/category/{0}\">{0}</a> ".format(the_category)
	else:
		parts = publish_parts("",writer_name='html')
		if not category:
			parts['fragment'] = "<h1>Categories</h1>\n"
		else:
			parts['fragment'] = "<h1>Category</h1>\n"
		for i in categories:
			if category and category != i:
				continue
			expanded_category_name = ": ".join([word.capitalize() for word in i.split(":")])
			category_name_path = i.replace(":", "/")
			if category_name_path and category_name_path[0] != "/":
				category_name_path = "/%s" % category_name_path
			parts['fragment'] += "<p>%s</p>\n" % expanded_category_name
			parts['fragment'] += "<ul>\n"
			for entry in categories[i]:
				basefilename = entry[0]
				if "/" in basefilename:
					basefilename = basefilename[basefilename.rfind("/")+1:]
				if len(basefilename) >= 4 and basefilename[-4:] == ".rst":
					basefilename = basefilename[:-4]
				human_readable_name = " ".join([word.capitalize() for word in basefilename.split("_")])
				parts['fragment'] += "<li><a href=\"{0}/{1}\">{2}</a></li>\n".format(category_name_path, basefilename, human_readable_name)
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
	entry_id = form.getfirst("id",None)
	category = form.getfirst("cat",None)

	if entry_id and entry_id[-1] == "/":
		entry_id = entry_id[0:-1]
	if category and category[-1] == "/":
		category = category[0:-1]

	render_rst(entry_id,category)

