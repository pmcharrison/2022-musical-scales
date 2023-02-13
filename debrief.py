from dominate.tags import div, p, span, h1, strong, ul, li, em

from psynet.consent import NoConsent
from psynet.modular_page import ModularPage, CheckboxControl
from psynet.page import InfoPage
from psynet.timeline import Module, join

debriefing_html = div()

with debriefing_html:
    h1("Debriefing")
    p(
        """
        Thank you for taking part in this experiment. 
        """
    )
    p(
        """
        In this study, we are examining which emotions are commonly associated with different musical modes (also known
        as key signatures). In addition to the emotional associations of each mode, we are interested in uncovering the
        specific structural features in the modes that are responsible for driving the reactions. These features could
        be related to interval size, pitch height, or familiarity, to name only a few.
        """
    )
    p(
        """
        Thank you for helping us shed light on this section of music psychology.
        """
    )
    p(
        """
        For any questions or concerns please contact Claire Anne Brillon at cb2211@cam.ac.uk.
        """
    )

def debriefing():
    return Module(
        "debriefing",
        join(
            InfoPage(debriefing_html, time_estimate=20),
        )
    )
