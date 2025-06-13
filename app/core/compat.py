from collections.abc import (
    Mapping,
    MutableSet,
    Iterable,
    Sequence,
    MutableSequence,
    Set,
    MutableMapping
)

# Monkey patch collections to include all needed ABC classes
import collections
collections.Mapping = Mapping
collections.MutableSet = MutableSet
collections.Iterable = Iterable
collections.Sequence = Sequence
collections.MutableSequence = MutableSequence
collections.Set = Set
collections.MutableMapping = MutableMapping