#!/usr/bin/env python

if __name__ == "__main__":
    from util import Post, get_config
    from pyatom import AtomFeed
    import datetime
    import time

    feed = AtomFeed(title=local_settings['title'],
                    feed_url="%s/feed" % local_settings['base_url'],
                    url = local_settings['base_url'],
                    author= local_settings['author'])

    max_mtime = -1
    for path in local_settings['urls'].itervalues():
        post = Post(path)
        mtime = post.mtime()
        if mtime > max_mtime:
            max_mtime = mtime
        feed.add(title=post.title(),
                 content_type="html",
                 author=local_settings['author'],
                 url="%s/%s" % (local_settings['base_url'], post.web_path()),
                 updated=datetime.datetime.fromtimestamp(mtime))

    feed.updated = datetime.datetime.fromtimestamp(max_mtime)

    print("Content-type: application/rss+xml\n")
    print feed.to_string()
