#!/usr/bin/python3


# A mapping of one note per key in an octave starting from C.
NOTE_NAMES = [
  "C",
  "C#",
  "D",
  "D#",
  "E",
  "F",
  "F#",
  "G",
  "G#",
  "A",
  "A#",
  "B"
]


# A mapping of sharp notes to their flat equivalents.
ALTERNATES = {
  "C#" : "Db",
  "D#" : "Eb",
  "F#" : "Gb",
  "G#" : "Ab",
  "A#" : "Bb",  
}


# Inverse of the "ALTERNATES" dict above.
ALIAS_NAMES = { flat : sharp for sharp, flat in ALTERNATES.items() }


# Sometimes you just gotta.
GOOFY_NAMES = {
  "Cb" : "B",
  "E#" : "F",
  "Fb" : "E",
  "B#" : "C",
}


# A lookup table of roman numerals.
NUMERALS = [
  "i",
  "ii",
  "iii",
  "iv",
  "v",
  "vi",
  "vii",
  "viii",
  "ix",
  "x",
  "xi",
  "xii",
  "xiii"
]


def normalize_note_name(name):
    """
    Given a note name like "Bb", return the equivalent name from the list
    "NOTE_NAMES".
    """
    assert(type(name) == str)
    name = name.title()
    name = GOOFY_NAMES.get(name) or name
    name = ALIAS_NAMES.get(name) or name
    assert(NOTE_NAMES.count(name))
    return name


def note_num(name):
    """
    For a given note name like "Bb", return the number of half steps the note
    is above "C".
    """
    if type(name) == int:
        return name % 12
    name = normalize_note_name(name)
    return NOTE_NAMES.index(name)


def note_distance(low, high):
    """
    Return the distance between two notes.  The first note is assumed to be lower on
    the keyboard than the second.  The notes can be either numerical offsets from C or
    note name strings.
    """
    low = note_num(low)
    high = note_num(high)
    if high < low:
        high += 12
    return high - low
