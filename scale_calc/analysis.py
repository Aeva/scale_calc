#!/usr/bin/python3

from .chords import *
from .transforms import *


def spelling(scale, adjust_accidentals=True):
    """
    Attempt to spell out all of the notes in a scale.  This returns a list of
    human-readable note names.  If the adjust_accidentals parameter is set True,
    then this will attempt to rewrite the accidentals in the scale in such a
    way that minimizes repeat note names.

    For example, Scale("WWHWHWHH", "C#") could be written as either
    "Db, Eb, F, Gb, Ab, A, B, C" or as "C#, D#, F, F#, G#, A, B, C".
    """
    if not scale.has_tonic():
        raise ValueError("The scale must have the tonic set to determine the spelling!")

    notes = [NOTE_NAMES[note % 12] for note, state in enumerate(scale.keyboard[:-1], scale.tonic) if state]
    if not adjust_accidentals:
        return notes

    def rewrite(notes, rewrite_tonic):
        start = 0 if rewrite_tonic else 1
        for i in range(start, len(notes)):
            prev = notes[(i -1) % len(notes)]
            this = notes[i]
            push = note_distance(prev, this) <= 2
            rename = ALTERNATES.get(this)
            if push and rename:
                notes[i] = rename
        return notes

    def unique_letter_names(notes):
        return len({note[0] for note in notes})

    minimal = rewrite(list(notes), False)
    maximal = rewrite(list(notes), True)

    if unique_letter_names(maximal) > unique_letter_names(minimal):
        return maximal
    else:
        return minimal


def degree_numeral(degree, quality):
    """
    For a given degree number and harmonic quality, generate the appropriate roman
    numeral notation.
    """
    assert(type(degree) == int)
    assert(degree > 0)

    if quality in [EQuality.UNKNOWN, EQuality.PERFECT]:
        return str(degree) + "?"

    major = ""
    minor = ""
    try:
        degree = NUMERALS[degree-1]
    except IndexError:
        degree = str(degree)
        major = "M"
        minor = "m"

    if quality is EQuality.MINOR:
        return degree + minor
    elif quality is EQuality.DIMINISHED:
        return degree + "*"
    elif quality is EQuality.MAJOR:
        return degree.upper() + major
    elif quality is EQuality.AUGMENTED:
        return degree.upper() + "+"


def triad_quality(root, third, fifth, scale=None):
    """
    Attempt to determine the harmonic quality of a triad.
    """
    third1 = interval_quality(root, third, scale, EInterval.THIRD)
    third2 = interval_quality(third, fifth, scale, EInterval.THIRD)
    if third1[1] is EInterval.THIRD and third2[1] is EInterval.THIRD:
        if third1[0] is EQuality.MAJOR and third2[0] is EQuality.MINOR:
            return EQuality.MAJOR
        elif third1[0] is EQuality.MINOR and third2[0] is EQuality.MAJOR:
            return EQuality.MINOR
        elif third1[0] is EQuality.MINOR and third2[0] is EQuality.MINOR:
            return EQuality.DIMINISHED
        elif third1[0] is EQuality.MAJOR and third2[0] is EQuality.MAJOR:
            return EQuality.AUGMENTED
    return EQuality.UNKNOWN


def scale_degree_qualities(scale):
    """
    For a given scale, return the list of harmonic qualities for the scale's degrees.
    """
    if not scale.has_tonic():
        # Doesn't matter
        scale = Scale(scale, tonic="C")
    notes = [note % 12 for note, state in enumerate(scale.keyboard[:-1], scale.tonic) if state]
    qualities = []
    for i in range(len(notes)):
        low = notes[i]
        med = notes[(i + 2) % len(notes)]
        high = notes[(i + 4) % len(notes)]
        qualities.append(triad_quality(low, med, high, scale))
    return qualities


def pretty_print(scale):
    if not scale.has_tonic():
        # Doesn't matter
        scale = Scale(scale, tonic="C")

    notes = spelling(scale)
    scale = Scale(scale, tonic=notes[0])
    if not scale.name:
        scale = rename_to_matching_scale(scale)

    degrees = [degree_numeral(i, q) for i, q in enumerate(scale_degree_qualities(scale), 1)]

    def pad(m, size=4):
        m = str(m)
        add = max(0, size - len(m))
        left = add // 2
        right = add - left
        return (" " * left) + m + (" " * right)

    template = """
{} ({})
      notes: {}
    degrees: {}
"""

    print(template.format(
        scale.nice_name,
        scale.intervals,
        " ".join(map(pad, notes)),
        " ".join(map(pad, degrees))))


def adjacent_scales(scale, turns=3):
    """
    Returns a list of adjacent scales to the provided scale, ordered by relative
    brightness.
    """
    scales = []
    for turn in range(turns, 0, -1):
        scales.append(sharpen(scale, turn))
    scales.append(scale)
    for turn in range(1, turns+1):
        scales.append(flatten(scale, turn))
    return tuple(scales)
