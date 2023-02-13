import random

from dominate import tags

from psynet.js_synth import JSSynth, Note
from psynet.modular_page import ModularPage
from psynet.timeline import Event, Module


def volume_calibration(mean_pitch, sd_pitch, timbre, time_estimate=5, min_time=2.5):
    text = tags.div()
    with text:
        tags.p(
            """
            Please listen to the following sound and adjust your
            computer's output volume until it is at a comfortable level.
            """
        )
        tags.p(
            """
            If you can't hear anything, there may be a problem with your
            playback configuration or your internet connection.
            You can refresh the page to try loading the audio again.
            """
        )

    n_notes = int(1e4)
    notes = [
        Note(random.normalvariate(mu=mean_pitch, sigma=sd_pitch))
        for _ in range(n_notes)
    ]

    return Module(
        "volume_calibration",
        ModularPage(
            "volume_calibration",
            JSSynth(
                text,
                notes,
                timbre=timbre,
            ),
            events={
                "submitEnable": Event(is_triggered_by="trialStart", delay=min_time)
            },
            time_estimate=time_estimate,
        )
    )
