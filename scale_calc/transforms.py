#!/usr/bin/python3

from .scales import *


def rename_to_matching_mode(scale):
    """
    If the scale's interval pattern matches that of one of the diatonic modes,
    then rename the scale to that.
    """
    if scale.is_diatonic():
        for name, reference_scale in COMMON_SCALES.items():
            if name in DIATONIC_MODE_NAMES and scale.intervals == reference_scale.intervals:
                return Scale(scale, name=name)
    return scale


def sharpen(scale, turns):
    """
    Rotate a scale some number of turns clockwise around the circle of fifths.
    """
    assert(type(scale) == Scale)
    if not scale.has_tonic():
        raise ValueError("Scale cannot be sharpened if the tonic is unset!")
    if turns <= 0:
        return rename_to_matching_mode(scale)
    else:
        keyboard = scale.keyboard
        check = keyboard[5:]
        nudge = check.index(1)
        shift = 5 + nudge
        keyboard = (keyboard[:12] + keyboard[:12])[shift:][:13]
        scale = Scale(keyboard, tonic=(scale.tonic + nudge), name=scale.name)
        return sharpen(scale, turns - 1)


def flatten(scale, turns):
    """
    Rotate a scale some number of turns widdershins around the circle of fifths.
    """
    assert(type(scale) == Scale)
    if not scale.has_tonic():
        raise ValueError("Scale cannot be flattened if the tonic is unset!")
    if turns <= 0:
        return rename_to_matching_mode(scale)
    else:
        keyboard = scale.keyboard
        check = keyboard[:8][-1::-1]
        nudge = check.index(1)
        shift = 7 - nudge
        keyboard = (keyboard[:12] + keyboard[:12])[shift:][:13]
        scale = Scale(keyboard, tonic=(scale.tonic - nudge), name=scale.name)
        return flatten(scale, turns - 1)


def rotate(scale, turns):
    """
    Rotate a scale some number of turns around the circle of fifths.
    Positive number of turns = clockwise / sharper.
    Negative number of turns = widdershins / flatter.
    """
    assert(type(scale) == Scale)
    if not scale.has_tonic():
        raise ValueError("Scale cannot be rotated if the tonic is unset!")
    if turns == 0:
        return scale
    elif turns < 0:
        return flatten(scale, -turns)
    else:
        return sharpen(scale, turns)


def clink_my_heptatonic(scale):
    """
    This function builds a pentatonic scale from a heptatonic scale by dropping
    the scale's 3rd and 6th degrees, which produces a pleasant non-functional
    harmony.  This is named after my esteemed colleague and notable iconoclast
    Alex Clinkscales, who came up with idea in pursuit of his noble quest to
    break out of the matrix of diatonic harmony.
    """
    assert(scale.is_heptatonic())
    ab, bc, cd, de, ef, fg, ga = map(int, scale.intervals)
    intervals = "".join(map(str, (ab, bc + cd, de, ef + fg, ga)))
    name = scale.name
    tonic = scale.tonic
    if type(name) is str:
        name = "Clinked-" + name
    return Scale(intervals, tonic=tonic, name=name)


def test_transforms():
    clink = clink_my_heptatonic(Scale("Dorian"))
    assert(clink.intervals == "23232")
    assert(clink.name == "Clinked-Dorian")

    rotated = rotate(Scale("Locrian", tonic="C"), 7)
    assert(rotated.tonic == note_num("C#"))
    assert(rotated.name == "Locrian")
    assert(rotated.intervals == Scale("Locrian").intervals)
    assert(rotated.keyboard == Scale("Locrian").keyboard)

    rotated = rotate(Scale("Locrian", tonic="C"), -7)
    assert(rotated.tonic == note_num("B"))
    assert(rotated.name == "Locrian")
    assert(rotated.intervals == Scale("Locrian").intervals)
    assert(rotated.keyboard == Scale("Locrian").keyboard)

    rotated = rotate(Scale("Locrian", tonic="C"), 6)
    assert(rotated.tonic == note_num("C"))
    assert(rotated.name == "Lydian")
    assert(rotated.intervals == Scale("Lydian").intervals)
    assert(rotated.keyboard == Scale("Lydian").keyboard)
