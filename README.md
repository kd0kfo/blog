blog
====

About
--------

This is a very simple python based blog. Content is written in plain text using reStructuredText formatting. The purpose of this is to write documents that are easily read, written and migratable, without being dependent on a third party blog software or database. Content is rendered into html using docutils.

Install
-------

The python module docutils must be in the python path used by the cgi script, cgi-bin/render.cgi.

Content may be placed in any subdirectory of the top most directory of the blog website. Then, for each blog file, an entry is made in the "urls" dict in the cgi-bin/local_settings.py file. An example is provided in cgi-bin/local_settings.py.example.

The page can use a custom stylesheet, defined by the variable "stylesheet" in cgi-bin/local_settings.py.

Requires
---------

* docutils -- http://docutils.sourceforge.net

License
-------

This software is available under the GNU General Public License. See COPYING for details.

