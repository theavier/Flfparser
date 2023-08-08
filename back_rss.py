import rfeed

def create_rss_items(items):
    _items = []
    for item in items:
        _items.append(rfeed.Item(title=item['titel'],  description=item['description']+", Pris: "+item['price'],
                           link=item['href']))
    return _items


def create_rss(items, title="my title", desc="my desc",):
    _items = create_rss_items(items)
    feed = rfeed.Feed(title=title, description=desc, language='en-US', items=_items, link="link")
    return feed.rss()