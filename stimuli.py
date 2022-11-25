import glob
import itertools
import os
import pandas as pd
from dataclasses import dataclass, field
from typing import List


@dataclass
class Scale:
    name: str
    steps: List[str]
    pitch_classes: List[int]
    n_scale_degrees: int
    alterations: List[int] = field(init=False)
    reference_scale: List[int] = field(init=False, repr=False)

    def __post_init__(self):
        self.reference_scale = [0, 2, 4, 5, 7, 9, 11]  # major scale
        self.alterations = [
            this - reference
            for this, reference in zip(self.pitch_classes, self.reference_scale)
        ]

    @staticmethod
    def get_scale_degrees(midi, reference_scale):
        "Expresses a given pitch sequence in scale degrees with respective to a reference scale"
        return [reference_scale.index(pitch % 12) for pitch in midi]

    def apply(self, midi):
        "Converts a given pitch sequence to a given scale. Assumes the original pitch sequence is in C major."
        scale_degrees = self.get_scale_degrees(midi, self.reference_scale)
        alterations = [self.alterations[scale_degree] for scale_degree in scale_degrees]
        return [pitch + alteration for pitch, alteration in zip(midi, alterations)]


def load_scales(path):
    df = pd.read_table(path, delimiter="\t")
    return {
        row.name: Scale(
            name=row.name,
            steps=list(row.steps),
            pitch_classes=[int(x) for x in row.pitch_classes.split(", ")],
            n_scale_degrees=row.n_scale_degrees,
        )
        for row in df.itertuples()
    }


def test_scales():
    scales = load_scales("scales.tsv")
    assert scales["Ionian (maj)"].alterations == [0, 0, 0, 0, 0, 0, 0]
    assert scales["Dorian"].alterations == [0, 0, -1, 0, 0, 0, -1]
    assert scales["Dorian"].apply([60, 67, 64, 67, 71, 72]) == [60, 67, 63, 67, 70, 72]


test_scales()


@dataclass
class Melody:
    name: str
    midi: List[float]
    duration: List[float]
    onset: List[float] = field(init=False)
    total_n_beats: float = field(init=False)

    def __post_init__(self):
        self.onset = [0] + list(itertools.accumulate(self.duration))[:-1]
        self.total_n_beats = sum(self.duration)

    def realize(self, tempo, scale: Scale, target_mean_pitch=60.0):
        beat_duration_sec = 60 / tempo
        note_durations_sec = [duration * beat_duration_sec for duration in self.duration]
        total_note_durations_sec = sum(note_durations_sec)

        unnormalised_pitches = scale.apply(self.midi)

        # Note: we weight each pitch by its duration when normalising pitch height
        unnormalised_mean_pitch = sum(
            [
                pitch * duration_sec / total_note_durations_sec
                for pitch, duration_sec in zip(unnormalised_pitches, note_durations_sec)
            ]
        )
        transposition = target_mean_pitch - unnormalised_mean_pitch
        pitches = [pitch + transposition for pitch in unnormalised_pitches]

        return {
            "pitches": pitches,
            "note_durations_sec": note_durations_sec,
            "total_note_durations_sec": total_note_durations_sec,
            "transposition": transposition,
        }


def load_melodies(path):
    melodies = [
        load_melody(x) for x in glob.glob(os.path.join(path, "*.csv"))
    ]
    return {
        melody.name: melody
        for melody in melodies
    }


def load_melody(path):
    name = os.path.splitext(os.path.basename(path))[0]
    df = pd.read_csv(path)
    return Melody(name, list(df.midi), list(df.duration))


def test_melodies():
    scales = load_scales("scales.tsv")

    melody = Melody(
        "test",
        midi=[60, 64, 67, 69, 67],
        duration=[2, 1, 1, 0.5, 1]
    )
    original_mean_pitch = (60 * 2 + 64 + 67 + 69 * 0.5 + 67) / (2 + 1 + 1 + 0.5 + 1)

    realized = melody.realize(tempo=100, scale=scales["Ionian (maj)"], target_mean_pitch=50)
    assert realized["transposition"] == 50 - original_mean_pitch
    assert realized["pitches"] == [pitch + realized["transposition"] for pitch in melody.midi]


test_melodies()
