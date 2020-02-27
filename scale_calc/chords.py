#!/usr/bin/python3

from enum import Enum
from .scales import *


# This will be prepopulated with common chords.  See "populate_common_chords" below.
COMMON_CHORDS = {}


class Chord:
    """
    Represents a chord.  Internally this is represented by a tuple of 0s and 1s that
    represents the keyboard's state starting at the chord's root.  This should make it
    compatible with the Scale objects for a number of things.

    Chords take any number of positional parameters upon construction.  If a param is
    an integer, then it will be treated as a chord with two notes where the second note
    is that many semitones above the root.  For example, a major third could be constructed
    with "4".

    The construction positional params can also be other Chord objects (or Chord-like
    objects).  In which case, they will be concatinated.

    You can also pass in key of any of the chords in COMMON_CHORDS, and the constructor
    will use that automatically.
    """

    def __init__(self, *params, name=None, root=None):
        self.__root = root
        self.__name = name
        self.__keyboard = (1,)
        for param in params:
            if param in COMMON_CHORDS.keys():
                param = COMMON_CHORDS.get(param)
            if type(param) == int:
                self.__keyboard += (0,) * (param - 1) + (1,)
            else:
                self.__keyboard += param.keyboard[1:]


    @property
    def root(self):
        return self.__root


    @property
    def name(self):
        return self.__name


    @property
    def keyboard(self):
        return self.__keyboard


    @property
    def nice_name(self):
        name = self.name or str(self.keyboard)
        if self.root:
            return "{} {}".format(self.root, name)
        else:
            return name


    def __repr__(self):
        return "<{} Chord>".format(self.nice_name)


    def order(self):
        return (self.root, len(self.keyboard), self.name, self.keyboard)


    def __hash__(self):
        return hash(self.order())


    def __lt__(self, other):
        return self.order() < other.order()


    def __le__(self, other):
        return self.order() <= other.order()


    def __eq__(self, other):
        return self.order() == other.order()


    def __gt__(self, other):
        return self.order() > other.order()


    def __ge__(self, other):
        return self.order() >= other.order()


def compare_chords(lhs, rhs):
    """
    Take two chords or chord-like objects and compare them.
    The return result is a pair of floats that say how much one was like the value.
    """
    try:
        lhs = lhs.keyboard
    except AttributeError:
        pass
    try:
        rhs = rhs.keyboard
    except AttributeError:
        pass
    lhs_pad = max(len(rhs) - len(lhs), 0)
    rhs_pad = max(len(lhs) - len(rhs), 0)
    lhs += (0,) * lhs_pad
    rhs += (0,) * rhs_pad
    lhs_pressed = sum(lhs)
    rhs_pressed = sum(rhs)
    parity = sum(map(lambda x: (x[0] & x[1]), zip(lhs, rhs)))
    return parity/lhs_pressed, parity/rhs_pressed


def populate_common_chords():
    assert(not COMMON_CHORDS)
    params = (
        ("Diminished 3rd", 2),
        ("Minor 3rd", 3),
        ("Major 3rd", 4),
        ("Augmented 3rd", 5),

        ("Diminished 5th", "Minor 3rd", "Minor 3rd"),
        ("Minor 5th", "Minor 3rd", "Major 3rd"),
        ("Major 5th", "Major 3rd", "Minor 3rd"),
        ("Augmented 5th", "Major 3rd", "Major 3rd"),

        ("Major 7th", "Major 5th", "Major 3rd"),
        ("Minor 7th", "Minor 5th", "Minor 3rd"),
        ("Dominant 7th", "Major 5th", "Minor 3rd"),
        ("Diminished 7th", "Diminished 5th", "Minor 3rd"),
        ("Half-diminished 7th", "Diminished 5th", "Major 3rd"),
        ("Minor Major 7th", "Minor 5th", "Major 3rd"),
        ("Augmented Major 7th", "Augmented 5th", "Major 3rd"),
        ("Augmented 7th", "Augmented 5th", "Diminished 3rd"),
        ("Diminished Major 7th", "Diminished 5th", "Augmented 3rd"),
        ("Dominant 7th b5", "Major 3rd", "Diminished 3rd", "Major 3rd"),
        ("Major 7th b5", "Major 3rd", "Diminished 3rd", "Augmented 3rd"))

    for fnord in params:
        car, cdr = fnord[0], fnord[1:]
        COMMON_CHORDS[car] = Chord(*cdr, name=car)


populate_common_chords()
del populate_common_chords
