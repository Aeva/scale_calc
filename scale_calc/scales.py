#!/usr/bin/python3

import re


# This will be prepopulated with common scales.  See "populate_common_scales" below.
COMMON_SCALES = {}


INTERVAL_PATTERN = re.compile(r"^[wh1-9]+$", re.I)


def normalize_intervals(intervals):
    """
    This accepts the "WWHWWWH" style spelling, but returns "2212221" spelling,
    and ensures that the intervals span exactly an octave.
    """
    assert(INTERVAL_PATTERN.search(intervals))
    intervals = list(map(int, intervals.lower().replace("w", "2").replace("h", "1")))
    assert(sum(intervals) == 12)
    return "".join(map(str, intervals))


def intervals_to_keyboard(intervals):
    """
    This takes an interval string like "2212221" and returns a tuple representing
    which keys in an octave are covered by the given interval string.  For example,
    "WWHWWWH" would return (1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1).
    """
    intervals = list(map(int, normalize_intervals(intervals)))
    keyboard = [1]
    for interval in intervals:
        zeros = interval-1
        for zero in range(zeros):
            keyboard.append(0)
        keyboard.append(1)
    assert(keyboard[0] == 1)
    assert(keyboard[-1] == 1)
    assert(len(keyboard) == 13)
    return tuple(keyboard)


def keyboard_to_intervals(keyboard):
    """
    This is the inverse of the function "intervals_to_keyboard".
    """
    assert(keyboard[0] == 1)
    assert(keyboard[-1] == 1)
    cdr = list(keyboard)[1:]
    acc = []
    while cdr:
        next = cdr.index(1) + 1
        acc.append(next)
        cdr = cdr[next:]
    return normalize_intervals("".join(map(str, acc)))


class Scale:
    """
    This class represents a 12-note diatonic scale, and is meant to facilitate
    the various transforms and calculations of this program.

    This can be constructed from either a interval string (such as "WWHWWWH" or
    "23232"), from a tuple of 13 integers representing an octave w/ the tonic
    repeated, or from another instance of this class.

    The "keyboard" and "intervals" attributes of this class are used to retrieve
    the two different representations of the scale that this class manages,
    however these are not exposed w/ setters as they are intended to be immutable.
    """


    def __init__(self, pattern, name=None, tonic=None):
        self.name = name
        self.tonic = tonic

        if COMMON_SCALES.get(pattern):
            pattern = COMMON_SCALES[pattern]

        if type(pattern) is str:
            self.__keyboard = None
            self.__intervals = normalize_intervals(pattern)

        elif type(pattern) is tuple:
            assert(len(pattern) == 13)
            for key in pattern:
                assert(type(key) == int)
                assert(key == 0 or key == 1)
            self.__keyboard = pattern
            self.__intervals = None

        elif type(pattern) is Scale:
            self.__keyboard = pattern.keyboard
            self.__intervals = None

        else:
            raise TypeError("Malformed scale pattern.")


    def __repr__(self):
        name = self.name or self.intervals
        if self.tonic:
            return "<{} {} Scale>".format(tonic, name)
        else:
            return "<{} Scale>".format(name)


    @property
    def keyboard(self):
        if not self.__keyboard:
            assert(self.__intervals)
            self.__keyboard = intervals_to_keyboard(self.__intervals)
        return self.__keyboard


    @property
    def intervals(self):
        if not self.__intervals:
            assert(self.__keyboard)
            self.__intervals = keyboard_to_intervals(self.__keyboard)
        return self.__intervals


def populate_common_scales():
    assert(not COMMON_SCALES)
    params = (
        ("Ionian", "WWHWWWH"),
        ("Dorian", "WHWWWHW"),
        ("Phrygian", "HWWWHWW"),
        ("Lydian", "WWWHWWH"),
        ("Mixolydian", "WWHWWHW"),
        ("Aeolian", "WHWWHWW"),
        ("Locrian", "HWWHWWW"),
        ("Major", "Ionian"),
        ("Harmonic Major 1", "2212131"),
        ("Harmonic Major 2", "2213121"),
        ("Minor", "Aeolian"),
        ("Natural Minor", "Minor"),
        ("Melodic Minor", "2122221"),
        ("Harmonic Minor", "2122131"),
        ("Cursed 1", "WHWHWHWH"),
        ("Cursed 2", "HWHWHWHW"))

    for name, interval in params:
        COMMON_SCALES[name.title()] = interval

    for key in COMMON_SCALES.keys():
        alias = COMMON_SCALES[key]
        while COMMON_SCALES.get(alias.title()):
            alias = COMMON_SCALES[alias.title()]
        COMMON_SCALES[key] = alias

    for name, interval in COMMON_SCALES.items():
        COMMON_SCALES[name] = Scale(interval, name)


populate_common_scales()
del populate_common_scales


def test_scales():
    from random import randint
    keyboard = tuple([1] + [randint(0,1) for i in range(11)] + [1])
    from_keyboard = Scale(keyboard)
    from_intervals = Scale(from_keyboard.intervals)
    from_scale = Scale(from_intervals)
    intervals = from_scale.intervals
    assert(keyboard_to_intervals(keyboard) == intervals)
    assert(intervals_to_keyboard(intervals) == keyboard)
