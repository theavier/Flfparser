import rfeed

def create_rss_items(items):
    _items = []
    for item in items:
        #_item = rfeed.Item(title=item['titel'], link="link", description=item['description'],
        #              author="author", guid=rfeed.Guid("link"),
        #              enclosure=rfeed.Enclosure(url="image", type="image/jpeg",
        #                                            length=0))
        _item = rfeed.Item(title=item['titel'],  description=item['description'])
        _items.append(_item)
    return _items


def create_rss(items, title="my title", desc="my desc",):
    _items = create_rss_items(items)
    feed = rfeed.Feed(title=title, description=desc, language='en-US', items=_items, link="link")
    return feed.rss()