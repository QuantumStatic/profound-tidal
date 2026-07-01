# tidal/kv.py
_MISSING = object()

class KeyValueStore:
    def __init__(self):
        self._data = {}

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value

    def delete(self, key):
        self._data.pop(key, None)

    def exists(self, key):
        return key in self._data

    def pop(self, key, default=_MISSING):
        if default is _MISSING:
            return self._data.pop(key)
        return self._data.pop(key, default)

    def keys(self):
        return list(self._data.keys())

    def clear(self):
        self._data.clear()

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data
