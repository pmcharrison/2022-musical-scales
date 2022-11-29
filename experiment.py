# pylint: disable=unused-import,abstract-method,unused-argument
import random

import psynet.experiment
from psynet.consent import NoConsent
from psynet.js_synth import JSSynth, InstrumentTimbre, Note
from psynet.modular_page import SurveyJSControl
from psynet.page import InfoPage, SuccessfulEndPage, ModularPage
from psynet.timeline import Timeline, Event
from psynet.trial.static import StaticTrial, StaticNode, StaticTrialMaker
from psynet.utils import get_logger
from .stimuli import load_scales, load_melodies

logger = get_logger()


SCALES = load_scales("scales.tsv")
MELODIES = load_melodies("melodies")

RATING_ATTRIBUTES = [
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

N_RATING_ATTRIBUTES_PER_TRIAL = 3


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
    def base_melody(self):
        return MELODIES[self.definition["melody_name"]]

    @property
    def scale(self):
        return SCALES[self.definition["scale_name"]]

    def finalize_definition(self, definition, experiment, participant):
        definition["tempo"] = 100  # Todo - think about this
        definition["target_mean_pitch"] = random.uniform(67 - 1.5, 67 + 1.5)
        definition["rating_attributes"] = random.sample(RATING_ATTRIBUTES, k=N_RATING_ATTRIBUTES_PER_TRIAL)

        realized_melody = self.base_melody.realize(
            tempo=definition["tempo"],
            scale=self.scale,
            target_mean_pitch=definition["target_mean_pitch"],
        )

        definition["realized_melody__pitches"] = realized_melody["pitches"]
        definition["realized_melody__note_durations_sec"] = realized_melody["note_durations_sec"]
        definition["realized_melody__total_duration_sec"] = realized_melody["total_note_durations_sec"]
        definition["realized_melody__transposition"] = realized_melody["transposition"]

        return definition

    def show_trial(self, experiment, participant):
        return ModularPage(
            "rating",
            JSSynth(
                (
                    "Listen to the melody and rate it on the following scales. "
                    # "If you want to hear it again, feel free to refresh the page. "
                    # f"Scale: {self.definition['scale_name']}, "
                    # f"target mean pitch: {self.definition['target_mean_pitch']:.2f}."
                ),
                [
                    Note(pitch, duration=duration)
                    for pitch, duration in zip(
                        self.definition["realized_melody__pitches"],
                        self.definition["realized_melody__note_durations_sec"]
                    )
                ],
                timbre=InstrumentTimbre("piano"),
            ),
            SurveyJSControl(
                # See https://surveyjs.io/create-free-survey
                {
                    "elements": [
                        {
                            "type": "rating",
                            "name": attribute,
                            "title": attribute,
                            "isRequired": True,
                            "minRateDescription": "Not at all",
                            "maxRateDescription": "Very much so",
                        }
                        for attribute in self.definition["rating_attributes"]
                    ]
                }
            ),
            events={
                "submitEnable": Event(is_triggered_by="promptEnd"),
            },
        )


def custom_gmsi():
    # https://surveyjs.io/create-free-survey - export with JSON editor
    return ModularPage(
        "gmsi",
        "Please fill out the following questions.",
        control=SurveyJSControl(
            {
                "logoPosition": "right",
                "pages": [
                    {
                        "name": "page1",
                        "elements": [
                            {
                                "type": "text",
                                "name": "question1",
                                "title": "What's your name?"
                            }
                        ]
                    }
                ]
            }
        ),
        time_estimate=60 * 5,
    )


class Exp(psynet.experiment.Experiment):
    label = "Musical scales experiment"

    variables = {
        "window_width": 1024,
        "window_height": 1024,
    }

    timeline = Timeline(
        NoConsent(),
        InfoPage(
            "Welcome to the experiment!",
            time_estimate=5,
        ),
        StaticTrialMaker(
            id_="main_experiment",
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
        custom_gmsi(),
        # Q: repeat trials for performance incentive?
        SuccessfulEndPage(),
    )

    def __init__(self, session=None):
        super().__init__(session)
        self.initial_recruitment_size = (
            1
        )
