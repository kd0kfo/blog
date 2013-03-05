
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
