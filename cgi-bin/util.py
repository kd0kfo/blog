
def filename2category(filename):
    category = filename.split('/')
    return ":".join(category[:-1])

def extract_categories(urls):
    categories = {}
    for entry_id in urls.keys():
        key = urls[entry_id]
        category_str = filename2category(key)
        if not category_str in categories:
            categories[category_str] = [(key,entry_id)]
        else:
            categories[category_str].append((key,entry_id))
    return categories


class Post(object):
    def __init__(self, filename):
        self.filename = filename
        self.category = filename2category(filename)

    def title(self):
        from os.path import basename
        currfilename = basename(self.filename.split("/")[-1])
        return currfilename.replace(".rst","").title().replace("_", " ")

    def web_path(self):
        return self.filename.replace(".rst", "")

    def mtime(self):
        import os
        import os.path
        import time
        import local_settings
        path = os.path.join(local_settings.base_dir, self.filename)
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(path)
        return mtime
