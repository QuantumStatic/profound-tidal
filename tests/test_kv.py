# tests/test_kv.py
import pytest
from tidal.kv import KeyValueStore

def test_set_and_get():
    store = KeyValueStore()
    store.set("a", 1)
    assert store.get("a") == 1

def test_get_missing_key_returns_default():
    store = KeyValueStore()
    assert store.get("missing") is None
    assert store.get("missing", "fallback") == "fallback"

def test_set_overwrites_existing_key():
    store = KeyValueStore()
    store.set("a", 1)
    store.set("a", 2)
    assert store.get("a") == 2

def test_delete_removes_key():
    store = KeyValueStore()
    store.set("a", 1)
    store.delete("a")
    assert store.get("a") is None

def test_delete_missing_key_is_a_noop():
    store = KeyValueStore()
    store.delete("missing")

def test_exists_and_contains():
    store = KeyValueStore()
    store.set("a", 1)
    assert store.exists("a") is True
    assert "a" in store
    assert store.exists("b") is False
    assert "b" not in store

def test_pop_removes_and_returns_value():
    store = KeyValueStore()
    store.set("a", 1)
    assert store.pop("a") == 1
    assert "a" not in store

def test_pop_missing_key_without_default_raises():
    store = KeyValueStore()
    with pytest.raises(KeyError):
        store.pop("missing")

def test_pop_missing_key_with_default():
    store = KeyValueStore()
    assert store.pop("missing", "fallback") == "fallback"

def test_keys_lists_all_keys():
    store = KeyValueStore()
    store.set("a", 1)
    store.set("b", 2)
    assert sorted(store.keys()) == ["a", "b"]

def test_clear_empties_store():
    store = KeyValueStore()
    store.set("a", 1)
    store.clear()
    assert len(store) == 0

def test_len_reflects_entry_count():
    store = KeyValueStore()
    assert len(store) == 0
    store.set("a", 1)
    store.set("b", 2)
    assert len(store) == 2

def test_stores_are_independent():
    a = KeyValueStore()
    b = KeyValueStore()
    a.set("x", 1)
    assert b.get("x") is None
