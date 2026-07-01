# tests/test_kv.py
import threading
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

def test_compare_and_swap_succeeds_when_value_matches():
    store = KeyValueStore()
    store.set("a", 1)
    assert store.compare_and_swap("a", 1, 2) is True
    assert store.get("a") == 2

def test_compare_and_swap_fails_when_value_differs():
    store = KeyValueStore()
    store.set("a", 1)
    assert store.compare_and_swap("a", 99, 2) is False
    assert store.get("a") == 1

def test_compare_and_swap_on_missing_key():
    store = KeyValueStore()
    assert store.compare_and_swap("missing", None, "created") is True
    assert store.get("missing") == "created"
    assert store.compare_and_swap("missing2", "expected", "value") is False

def test_increment_defaults_and_accumulates():
    store = KeyValueStore()
    assert store.increment("counter") == 1
    assert store.increment("counter") == 2
    assert store.increment("counter", delta=5) == 7

def test_increment_with_custom_default_and_delta():
    store = KeyValueStore()
    assert store.increment("counter", delta=-1, default=10) == 9

def test_get_or_set_sets_on_first_call_only():
    store = KeyValueStore()
    assert store.get_or_set("a", "first") == "first"
    assert store.get_or_set("a", "second") == "first"
    assert store.get("a") == "first"

def test_concurrent_increment_is_strongly_consistent():
    store = KeyValueStore()
    threads = [
        threading.Thread(target=lambda: [store.increment("counter") for _ in range(1000)])
        for _ in range(8)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert store.get("counter") == 8000

def test_concurrent_set_and_get_never_sees_partial_state():
    store = KeyValueStore()
    errors = []

    def writer():
        for i in range(2000):
            store.set("pair", (i, i))

    def reader():
        for _ in range(2000):
            pair = store.get("pair")
            if pair is not None and pair[0] != pair[1]:
                errors.append(pair)

    threads = [threading.Thread(target=writer)] + [threading.Thread(target=reader) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert errors == []
