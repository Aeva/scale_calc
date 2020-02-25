#!/usr/bin/python3

from enum import Enum
from .scales import *


class EInterval(Enum):
    UNISON = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6
    SEVENTH = 7
    OCTAVE = 8
    NINTH = 9
    TENTH = 10
    ELEVENTH = 11
    TWELFTH = 12
    THIRTEENTH = 13
    UNKNOWN = 999


class EQuality(Enum):
    PERFECT = 1
    MAJOR = 2
    MINOR = 3
    DIMINISHED = 4
    AUGMENTED = 5
    UNKNOWN = 6


INTERVAL_MAP = {
    EInterval.UNISON : {
        0 : EQuality.PERFECT,
        1 : EQuality.AUGMENTED,
    },

    EInterval.SECOND : {
        0 : EQuality.DIMINISHED,
        1 : EQuality.MINOR,
        2 : EQuality.MAJOR,
        3 : EQuality.AUGMENTED,
    },

    EInterval.THIRD : {
        2 : EQuality.DIMINISHED,
        3 : EQuality.MINOR,
        4 : EQuality.MAJOR,
        5 : EQuality.AUGMENTED,
    },

    EInterval.FOURTH : {
        4 : EQuality.DIMINISHED,
        5 : EQuality.PERFECT,
        6 : EQuality.AUGMENTED,
    },

    EInterval.FIFTH : {
        6 : EQuality.DIMINISHED,
        7 : EQuality.PERFECT,
        8 : EQuality.AUGMENTED,
    },

    EInterval.SIXTH : {
        7 : EQuality.DIMINISHED,
        8 : EQuality.MINOR,
        9 : EQuality.MAJOR,
        10 : EQuality.AUGMENTED,
    },

    EInterval.SEVENTH : {
        9 : EQuality.DIMINISHED,
        10 : EQuality.MINOR,
        11 : EQuality.MAJOR,
        12 : EQuality.AUGMENTED,
    },

    EInterval.OCTAVE : {
        11 : EQuality.DIMINISHED,
        12 : EQuality.PERFECT,
    },
}


def degree_in_scale(note, scale):
    """
    For a given note, return the note's degree within the scale, or None if the note is
    not in the scale.
    """
    if not scale.has_tonic():
        raise ValueError("The scale must have the tonic set to determine a note's degree.")

    notes = [note % 12 for note, state in enumerate(scale.keyboard[:-1], scale.tonic) if state]
    try:
        return notes.index(note_num(note)) + 1
    except ValueError:
        return None


def interval_quality(low, high, scale=None, interval=None):
    """
    Attempt to determine the harmonic quality of a given interval.
    """
    dist = note_distance(low, high)

    if interval:
        if type(interval) == EInterval:
            interval = interval.value
        assert(type(interval) == int)
        alias = interval if interval < 8 else (interval % 8) + 1
        quality = INTERVAL_MAP[EInterval(alias)].get(dist)
        if quality:
            return (quality, EInterval(interval))

    if scale:
        low_degree = degree_in_scale(low, scale)
        high_degree = degree_in_scale(high, scale)
        if low_degree and high_degree:
            interval = EInterval(abs(high_degree - low_degree) + 1)
            qualities = INTERVAL_MAP[interval]
            return (qualities.get(dist) or EQuality.UNKNOWN, interval)

    # We don't know the scale degrees so we just have to guess.
    guesses = []
    for interval, qualities in INTERVAL_MAP.items():
        quality = qualities.get(dist)
        if quality:
            guesses.append((quality, interval))
    if guesses:
        guesses.sort(key=lambda x: int(x[0].value))
        return guesses[0]
    return (EQuality.UNKNOWN, EInterval.UNKNOWN)


class Interval:
    """
    Represents an interval between two notes.
    """

    def __init__(self, root, above, interval=None):
        self.root = note_num(root)
        self.quality, self.interval = interval_quality(root, above, None, interval)


    def __repr__(self):
        root_name = NOTE_NAMES[self.root]
        return "<{} {} {} Interval>".format(root_name, self.quality, self.interval)


    def __hash__(self):
        return hash((self.root, self.interval, self.quality))


    def value(self):
        return (self.interval.value, self.quality.value, self.root)


    def __lt__(self, other):
        return self.value() < other.value()


    def __le__(self, other):
        return self.value() <= other.value()


    def __eq__(self, other):
        return self.value() == other.value()


    def __gt__(self, other):
        return self.value() > other.value()


    def __ge__(self, other):
        return self.value() >= other.value()


class Chord:
    """
    Represents a chord as a collection of intervals from a root note.
    """

    def __init__(self, root, *intervals):
        self.root = note_num(root)
        for interval in intervals:
            assert(type(interval) == Interval)
            assert(interval.root == self.root)
        self.intervals = tuple(sorted(set(intervals)))


    def __repr__(self):
        return "<{} Chord>".format(self.name())


    def name(self):
        nth = self.intervals[-1].interval.value
        function = "???"
        root_name = NOTE_NAMES[self.root]
        return "{} {} {}".format(root_name, function, nth)


def chord_test():
    scale = "CDEFGAB"

    root = scale[0]
    first = Interval(root, scale[0], 1)
    assert(first.quality == EQuality.PERFECT)
    assert(first.interval == EInterval.UNISON)

    second = Interval(root, scale[1], 2)
    assert(second.quality == EQuality.MAJOR)
    assert(second.interval == EInterval.SECOND)

    third = Interval(root, scale[2], 3)
    assert(third.quality == EQuality.MAJOR)
    assert(third.interval == EInterval.THIRD)

    fourth = Interval(root, scale[3], 4)
    assert(fourth.quality == EQuality.PERFECT)
    assert(fourth.interval == EInterval.FOURTH)

    fifth = Interval(root, scale[4], 5)
    assert(fifth.quality == EQuality.PERFECT)
    assert(fifth.interval == EInterval.FIFTH)

    sixth = Interval(root, scale[5], 6)
    assert(sixth.quality == EQuality.MAJOR)
    assert(sixth.interval == EInterval.SIXTH)

    seventh = Interval(root, scale[6], 7)
    assert(seventh.quality == EQuality.MAJOR)
    assert(seventh.interval == EInterval.SEVENTH)

    eighth = Interval(root, scale[0], 8)
    assert(eighth.quality == EQuality.PERFECT)
    assert(eighth.interval == EInterval.OCTAVE)

    ninth = Interval(root, scale[1], 9)
    assert(ninth.quality == second.quality)
    assert(ninth.interval == EInterval.NINTH)

    tenth = Interval(root, scale[2], 10)
    assert(tenth.quality == third.quality)
    assert(tenth.interval == EInterval.TENTH)

    eleventh = Interval(root, scale[3], 11)
    assert(eleventh.quality == fourth.quality)
    assert(eleventh.interval == EInterval.ELEVENTH)

    twelfth = Interval(root, scale[4], 12)
    assert(twelfth.quality == fifth.quality)
    assert(twelfth.interval == EInterval.TWELFTH)

    thirteenth = Interval(root, scale[5], 13)
    assert(thirteenth.quality == sixth.quality)
    assert(thirteenth.interval == EInterval.THIRTEENTH)

    chord = Chord(root, third, fifth, seventh, ninth, thirteenth)
