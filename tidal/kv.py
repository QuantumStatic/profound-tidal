# tidal/kv.py
import threading

_MISSING = object()

class KeyValueStore:
    def __init__(self):
        self._data = {}
        self._lock = threading.RLock()

    def get(self, key, default=None):
        with self._lock:
            return self._data.get(key, default)

    def set(self, key, value):
        with self._lock:
            self._data[key] = value

    def delete(self, key):
        with self._lock:
            self._data.pop(key, None)

    def exists(self, key):
        with self._lock:
            return key in self._data

    def pop(self, key, default=_MISSING):
        with self._lock:
            if default is _MISSING:
                return self._data.pop(key)
            return self._data.pop(key, default)

    def keys(self):
        with self._lock:
            return list(self._data.keys())

    def clear(self):
        with self._lock:
            self._data.clear()

    def compare_and_swap(self, key, expected, new):
        with self._lock:
            if self._data.get(key) != expected:
                return False
            self._data[key] = new
            return True

    def increment(self, key, delta=1, default=0):
        with self._lock:
            value = self._data.get(key, default) + delta
            self._data[key] = value
            return value

    def get_or_set(self, key, default):
        with self._lock:
            if key in self._data:
                return self._data[key]
            self._data[key] = default
            return default

    def __len__(self):
        with self._lock:
            return len(self._data)

    def __contains__(self, key):
        return self.exists(key)
