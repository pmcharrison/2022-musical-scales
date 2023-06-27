# pylint: disable=unused-import,abstract-method,unused-argument
import random

from dominate import tags
from numpy import isnan

import psynet.experiment
from psynet.js_synth import JSSynth, InstrumentTimbre, Note
from psynet.modular_page import SurveyJSControl
from psynet.page import InfoPage, SuccessfulEndPage, ModularPage
from psynet.prescreen import AntiphaseHeadphoneTest
from psynet.timeline import Timeline, Event
from psynet.trial.static import StaticTrial, StaticNode, StaticTrialMaker
from psynet.utils import get_logger, corr

from .consent import consent
from .debrief import debriefing
from .instructions import instructions
from .questionnaire import questionnaire, questionnaire_intro
from .stimuli import load_scales, load_melodies
from .volume_calibration import volume_calibration

logger = get_logger()

TIMBRE = InstrumentTimbre("piano")

SCALES = load_scales("scales.tsv")  # 10 in total
MELODIES = load_melodies("melodies")

RATING_ATTRIBUTES = [  # 14 in total
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
    "Pride, confidence",
    # "Boredom, indifference", # We omitted this from the first experiment by accident
]

N_RATING_ATTRIBUTES_PER_TRIAL = 3
TRIALS_PER_PARTICIPANT = 50
N_REPEAT_TRIALS = 5

# For debugging
# TRIALS_PER_PARTICIPANT = 8
# N_REPEAT_TRIALS = 5


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
    time_estimate = 12

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
                timbre=TIMBRE,
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
                },
                bot_response={
                    attribute: random.choice([0, 1, 2, 3, 4, 5])
                    for attribute in self.definition["rating_attributes"]
                },
            ),
            events={
                "submitEnable": Event(is_triggered_by="promptEnd"),
            },
        )


class ScalesTrialMaker(StaticTrialMaker):
    give_end_feedback_passed = False

    def performance_check(
        self, experiment, participant, participant_trials
    ):
        trials_by_id = {trial.id: trial for trial in participant_trials}

        repeat_trials = [t for t in participant_trials if t.is_repeat_trial]
        parent_trials = [trials_by_id[t.parent_trial_id] for t in repeat_trials]

        repeat_trial_answers = []
        parent_trial_answers = []

        for repeat_trial, parent_trial in zip(repeat_trials, parent_trials):
            assert repeat_trial.definition["rating_attributes"] == parent_trial.definition["rating_attributes"]
            rating_attributes = repeat_trial.definition["rating_attributes"]

            for attribute in rating_attributes:
                repeat_trial_answers.append(int(repeat_trial.answer[attribute]))
                parent_trial_answers.append(int(parent_trial.answer[attribute]))

        consistency = corr(repeat_trial_answers, parent_trial_answers, method="spearman")
        passed = True

        if isnan(consistency):
            consistency = None

        logger.info(
            "Performance check for participant %i: consistency = %.1f%%, passed = %s",
            participant.id,
            consistency * 100.0,
            passed,
        )

        return {"score": consistency, "passed": passed}

    def compute_bonus(self, score, passed):
        max_bonus = 0.40

        if score is None or score <= 0.0:
            bonus = 0.0
        else:
            bonus = max_bonus * score

        bonus = min(bonus, max_bonus)
        return bonus


class Exp(psynet.experiment.Experiment):
    label = "Musical scales experiment"

    timeline = Timeline(
        consent,
        InfoPage(
            tags.div(
                tags.p("This experiment requires you to wear headphones. Please ensure you have plugged yours in now."),
                tags.p("The next page will play some test audio. Please turn down your volume before proceeding.")
            ),
            time_estimate=5,
        ),
        volume_calibration(mean_pitch=67, sd_pitch=5, timbre=TIMBRE),
        InfoPage(
            """
            We will now perform a short listening test to verify that your audio is working properly.
            This test will be difficult to pass unless you listen carefully over your headphones.
            Press 'Next' when you are ready to start.
            """,
            time_estimate=5,
        ),
        AntiphaseHeadphoneTest(),
        instructions(),
        ScalesTrialMaker(
            id_="main_experiment",
            trial_class=MelodyTrial,
            nodes=NODES,
            expected_trials_per_participant=TRIALS_PER_PARTICIPANT,
            max_trials_per_participant=TRIALS_PER_PARTICIPANT,
            recruit_mode="n_participants",
            allow_repeated_nodes=False,
            n_repeat_trials=N_REPEAT_TRIALS,
            balance_across_nodes=False,
            target_n_participants=50,
            check_performance_at_end=True,
        ),
        questionnaire_intro(),
        questionnaire(),
        debriefing(),
        SuccessfulEndPage(),
    )
