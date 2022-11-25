# pylint: disable=unused-import,abstract-method,unused-argument
import json
import random
import tempfile
from statistics import mean

from flask import Markup

import psynet.experiment
from psynet.asset import DebugStorage
from psynet.consent import MainConsent, NoConsent
from psynet.modular_page import PushButtonControl, AudioRecordControl, SurveyJSControl
from psynet.page import InfoPage, SuccessfulEndPage, ModularPage
from psynet.timeline import Timeline, Module, CodeBlock, Event, ProgressDisplay, ProgressStage
from psynet.trial.static import StaticTrial, StaticNode, StaticTrialMaker
from psynet.utils import get_logger

from psynet.js_synth import JSSynth, Chord, InstrumentTimbre

from .stimuli import load_scales, load_melodies

logger = get_logger()


SCALES = load_scales("scales.tsv")
MELODIES = load_melodies("melodies")

ATTRIBUTES = [
    "Happiness, elation",
    "Sadness, melancholy",
    "Surprise, astonishment",
    "Calm, contentment",
    "Anger, irritation",
    "Nostalgia, longing",
    "Interest, expectancy",
    "Anxiety, nervousness",
    "Love, tenderness",
    "Disgust, contempt",
    "Spirituality, transcendence",
    "Admiration, awe",
    "Enjoyment, pleasure",
    "Pride, confidence"
]

N_ATTRIBUTES_PER_TRIAL = 3


NODES = [
    StaticNode(
        definition={
            "scale_name": scale_name,
            "melody_name": melody_name,
        },
    )
    for scale_name in SCALES.keys()
    for melody_name in MELODIES.keys()
]


class MelodyTrial(StaticTrial):
    time_estimate = 10

    @property
    def melody(self):
        return MELODIES[self.definition["melody_name"]]

    def finalize_definition(self, definition, experiment, participant):
        definition["tempo"] = 100  # Todo - think about this
        definition["n_beats"] = self.melody.total_n_beats
        definition["duration_sec"] = definition["n_beats"] * 60 / definition["tempo"]
        definition["transposition"] = 0.0
        definition["attributes"] = random.sample(ATTRIBUTES, k=N_ATTRIBUTES_PER_TRIAL)

        return definition

    def show_trial(self, experiment, participant):

        return ModularPage(
            "rating",
            JSSynth(
                "Listen to the melody and rate it on the following scales.",
                self.melody.to_js_synth(
                    tempo=self.definition["tempo"],
                    transposition=self.definition["transposition"],
                ),
                timbre=InstrumentTimbre("piano"),
            ),
            SurveyJSControl(
                {
                    "elements": [
                        {
                            "type": "rating",
                            "name": attribute,
                            "title": attribute,
                            "isRequired": True,
                            "minRateDescription": "Not at all",
                            "maxRateDescription": "Very much so"
                        }
                        for attribute in self.definition["attributes"]
                    ]
                }
            ),
            events={
                "submitEnable": Event(is_triggered_by="promptEnd"),
            },
        )


class Exp(psynet.experiment.Experiment):
    label = "Musical scales experiment"

    timeline = Timeline(
        NoConsent(),
        InfoPage(
            "Welcome to the experiment!",
            time_estimate=5,
        ),
        StaticTrialMaker(
            id_="consonance_main_experiment",
            trial_class=MelodyTrial,
            nodes=NODES,
            expected_trials_per_participant=len(NODES),
            max_trials_per_participant=len(NODES),
            recruit_mode="n_participants",
            allow_repeated_nodes=False,
            n_repeat_trials=0,
            balance_across_nodes=False,
            target_n_participants=50,
        ),
        SuccessfulEndPage(),
    )

    def __init__(self, session=None):
        super().__init__(session)
        self.initial_recruitment_size = (
            1
        )
