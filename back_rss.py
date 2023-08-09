import rfeed


def create_rss_items(items: list) -> list:
    """ creates rss items from list """
    _items = []
    for item in items:
        _items.append(rfeed.Item(title=item['titel'],  description=item['description']+", Pris: "+item['price'],
                           link=item['href']))
    return _items


def create_rss(items: list, title: str = "my title", desc: str = "my desc",) -> str:
    """ creates rss headers with items """
    _items = create_rss_items(items)
    feed = rfeed.Feed(title=title, description=desc, language='en-US', items=_items, link="link")
    return feed.rss()
