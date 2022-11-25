import itertools

import glob

import os

from typing import List
from dataclasses import dataclass, field
from psynet.js_synth import Note

import pandas as pd


@dataclass
class Scale:
    name: str
    steps: List[str]
    pitch_classes: List[int]
    n_scale_degrees: int


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


# print(load_scales("scales.tsv"))


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

    def to_js_synth(self, tempo, transposition=0.0):
        beat_duration_sec = 60 / tempo
        return [
            Note(
                pitch=midi + transposition,
                duration=duration * beat_duration_sec,
            )
            for midi, duration in zip(self.midi, self.duration)
        ]


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


# print(load_melodies("melodies"))
