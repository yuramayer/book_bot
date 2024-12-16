from types import SimpleNamespace


class BookCache(SimpleNamespace):
    
    def __contains__(self, key):
        return hasattr(self, key)


    def get(self, key, default=None):
        return getattr(self, key, default)


BOOK_CACHE = BookCache()
