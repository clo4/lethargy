"""
## What needs to be tested?

- [x] prettynames sorts by length alphabetically
- [ ] index finds correct index
- [ ] index raises indexerror if not found
- [ ] index raises exc instead of indexerror if set

"""

from lethargy.mixins import Named


def test_prettynames_sorts_by_length_alphabetically():
    class Impl(Named):
        names = frozenset(["a", "cc", "aa", "zz", "fff", "b"])

    assert Impl().prettynames() == "a|b|aa|cc|zz|fff"


def test_index_finds_correct_index():
    pass


def test_index_raises_indexerror_if_not_found():
    pass


def test_index_raises_exc_instead_of_indexerror_if_set():
    pass
