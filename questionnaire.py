from dominate import tags

from psynet.modular_page import ModularPage, SurveyJSControl
from psynet.page import InfoPage


def questionnaire_intro():
    html = tags.div()
    with html:
        tags.p(
            "Congratulations, you completed the listening part of this experiment!"
        )
        tags.p(
            "Before we finish, we just have a few more questions to ask you. ",
            "They should only take a couple of minutes to complete.",
        )
    return InfoPage(html, time_estimate=6)


def questionnaire():
    # https://surveyjs.io/create-free-survey - export with JSON editor
    return ModularPage(
        "questionnaire",
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
                                "name": "age",
                                "title": "Your age (years)",
                                "isRequired": True
                            },
                            {
                                "type": "text",
                                "name": "gender",
                                "title": "I identify my gender as _  (please specify).",
                                "isRequired": True
                            },
                            {
                                "type": "checkbox",
                                "name": "occupation",
                                "title": "Occupational status",
                                "isRequired": True,
                                "choices": [
                                    "Still at School",
                                    {
                                        "value": "At University",
                                        "text": "At University"
                                    },
                                    {
                                        "value": "In Full-time employment",
                                        "text": "In Full-time employment"
                                    },
                                    {
                                        "value": "In Part-time employment",
                                        "text": "In Part-time employment"
                                    },
                                    {
                                        "value": "Self-employed",
                                        "text": "Self-employed"
                                    },
                                    {
                                        "value": "Homemaker/full time parent",
                                        "text": "Homemaker/full time parent"
                                    },
                                    {
                                        "value": "Unemployed",
                                        "text": "Unemployed"
                                    },
                                    {
                                        "value": "Retired",
                                        "text": "Retired"
                                    }
                                ],
                                "showOtherItem": True,
                                "maxSelectedChoices": 1
                            },
                            {
                                "type": "radiogroup",
                                "name": "MT_03",
                                "title": "I have never been complimented for my talents as a musical performer",
                                "choices": [
                                    {
                                        "value": 1,
                                        "text": "completely disagree"
                                    },
                                    {
                                        "value": 2,
                                        "text": "strongly disagree"
                                    },
                                    {
                                        "value": 3,
                                        "text": "disagree"
                                    },
                                    {
                                        "value": 4,
                                        "text": "neither agree not disagree"
                                    },
                                    {
                                        "value": 5,
                                        "text": "agree"
                                    },
                                    {
                                        "value": 6,
                                        "text": "strongly agree"
                                    },
                                    {
                                        "value": 7,
                                        "text": "completely agree"
                                    }
                                ]
                            },
                            {
                                "type": "radiogroup",
                                "name": "MT_06",
                                "title": "I can play _ musical instruments",
                                "choices": [
                                    {
                                        "value": "0",
                                        "text": "0"
                                    },
                                    {
                                        "value": "1",
                                        "text": "1"
                                    },
                                    {
                                        "value": "2",
                                        "text": "2"
                                    },
                                    {
                                        "value": "3",
                                        "text": "3"
                                    },
                                    {
                                        "value": "4",
                                        "text": "4"
                                    },
                                    {
                                        "value": "5",
                                        "text": "5"
                                    },
                                    {
                                        "value": "6 or more",
                                        "text": "6 or more"
                                    }
                                ],
                            },
                            {
                                "type": "radiogroup",
                                "name": "MT_07",
                                "title": "I would not consider myself a musician",
                                "choices": [
                                    {
                                        "value": 1,
                                        "text": "completely disagree"
                                    },
                                    {
                                        "value": 2,
                                        "text": "strongly disagree"
                                    },
                                    {
                                        "value": 3,
                                        "text": "disagree"
                                    },
                                    {
                                        "value": 4,
                                        "text": "neither agree nor disagree"
                                    },
                                    {
                                        "value": 5,
                                        "text": "agree"
                                    },
                                    {
                                        "value": 6,
                                        "text": "strongly agree"
                                    },
                                    {
                                        "value": 7,
                                        "text": "completely agree"
                                    }
                                ]
                            },
                            {
                                "type": "radiogroup",
                                "name": "PA_08",
                                "title": "When I sing, I have no idea whether I'm in tune or not",
                                "choices": [
                                    {
                                        "value": 1,
                                        "text": "completely disagree"
                                    },
                                    {
                                        "value": 2,
                                        "text": "strongly disagree"
                                    },
                                    {
                                        "value": 3,
                                        "text": "disagree"
                                    },
                                    {
                                        "value": 4,
                                        "text": "neither agree nor disagree"
                                    },
                                    {
                                        "value": 5,
                                        "text": "agree"
                                    },
                                    {
                                        "value": 6,
                                        "text": "strongly agree"
                                    },
                                    {
                                        "value": 7,
                                        "text": "completely agree"
                                    }
                                ]
                            },
                            {
                                "type": "radiogroup",
                                "name": "SA_03",
                                "title": "I am able to hit the right notes when I sing along with a recording",
                                "choices": [
                                    {
                                        "value": 1,
                                        "text": "completely disagree"
                                    },
                                    {
                                        "value": 2,
                                        "text": "strongly disagree"
                                    },
                                    {
                                        "value": 3,
                                        "text": "disagree"
                                    },
                                    {
                                        "value": 4,
                                        "text": "neither agree nor disagree"
                                    },
                                    {
                                        "value": 5,
                                        "text": "agree"
                                    },
                                    {
                                        "value": 6,
                                        "text": "strongly agree"
                                    },
                                    {
                                        "value": 7,
                                        "text": "completely agree"
                                    }
                                ]
                            },
                            {
                                "type": "radiogroup",
                                "name": "SA_04",
                                "title": "I am not able to sing in harmony when somebody is singing a familiar tune",
                                "choices": [
                                    {
                                        "value": 1,
                                        "text": "completely disagree"
                                    },
                                    {
                                        "value": 2,
                                        "text": "strongly disagree"
                                    },
                                    {
                                        "value": 3,
                                        "text": "disagree"
                                    },
                                    {
                                        "value": 4,
                                        "text": "neither agree nor disagree"
                                    },
                                    {
                                        "value": 5,
                                        "text": "agree"
                                    },
                                    {
                                        "value": 6,
                                        "text": "strongly agree"
                                    },
                                    {
                                        "value": 7,
                                        "text": "completely agree"
                                    }
                                ]
                            },
                            {
                                "type": "radiogroup",
                                "name": "EM_01",
                                "title": "I sometimes choose music that can trigger shivers down my spine",
                                "choices": [
                                    {
                                        "value": 1,
                                        "text": "completely disagree"
                                    },
                                    {
                                        "value": 2,
                                        "text": "strongly disagree"
                                    },
                                    {
                                        "value": 3,
                                        "text": "disagree"
                                    },
                                    {
                                        "value": 4,
                                        "text": "neither agree nor disagree"
                                    },
                                    {
                                        "value": 5,
                                        "text": "agree"
                                    },
                                    {
                                        "value": 6,
                                        "text": "strongly agree"
                                    },
                                    {
                                        "value": 7,
                                        "text": "completely agree"
                                    }
                                ]
                            },
                            {
                                "type": "radiogroup",
                                "name": "EM_02",
                                "title": "Pieces of music rarely evoke emotions for me",
                                "choices": [
                                    {
                                        "value": 1,
                                        "text": "completely disagree"
                                    },
                                    {
                                        "value": 2,
                                        "text": "strongly disagree"
                                    },
                                    {
                                        "value": 3,
                                        "text": "disagree"
                                    },
                                    {
                                        "value": 4,
                                        "text": "neither agree nor disagree"
                                    },
                                    {
                                        "value": 5,
                                        "text": "agree"
                                    },
                                    {
                                        "value": 6,
                                        "text": "strongly agree"
                                    },
                                    {
                                        "value": 7,
                                        "text": "completely agree"
                                    }
                                ]
                            },
                            {
                                "type": "radiogroup",
                                "name": "EM_03",
                                "title": "I often pick certain music  to motivate or excite me",
                                "choices": [
                                    {
                                        "value": 1,
                                        "text": "completely disagree"
                                    },
                                    {
                                        "value": 2,
                                        "text": "strongly disagree"
                                    },
                                    {
                                        "value": 3,
                                        "text": "disagree"
                                    },
                                    {
                                        "value": 4,
                                        "text": "neither agree nor disagree"
                                    },
                                    {
                                        "value": 5,
                                        "text": "agree"
                                    },
                                    {
                                        "value": 6,
                                        "text": "strongly agree"
                                    },
                                    {
                                        "value": 7,
                                        "text": "completely agree"
                                    }
                                ]
                            },
                            {
                                "type": "radiogroup",
                                "name": "EM_04",
                                "title": "I am able to identify what is special about a given musical piece",
                                "choices": [
                                    {
                                        "value": 1,
                                        "text": "completely disagree"
                                    },
                                    {
                                        "value": 2,
                                        "text": "strongly disagree"
                                    },
                                    {
                                        "value": 3,
                                        "text": "disagree"
                                    },
                                    {
                                        "value": 4,
                                        "text": "neither agree nor disagree"
                                    },
                                    {
                                        "value": 5,
                                        "text": "agree"
                                    },
                                    {
                                        "value": 6,
                                        "text": "strongly agree"
                                    },
                                    {
                                        "value": 7,
                                        "text": "completely agree"
                                    }
                                ]
                            },
                            {
                                "type": "radiogroup",
                                "name": "EM_05",
                                "title": "I am able to talk about the emotions that a piece of music evokes for me",
                                "choices": [
                                    {
                                        "value": 1,
                                        "text": "completely disagree"
                                    },
                                    {
                                        "value": 2,
                                        "text": "strongly disagree"
                                    },
                                    {
                                        "value": 3,
                                        "text": "disagree"
                                    },
                                    {
                                        "value": 4,
                                        "text": "neither agree nor disagree"
                                    },
                                    {
                                        "value": 5,
                                        "text": "agree"
                                    },
                                    {
                                        "value": 6,
                                        "text": "strongly agree"
                                    },
                                    {
                                        "value": 7,
                                        "text": "completely agree"
                                    }
                                ]
                            },
                            {
                                "type": "radiogroup",
                                "name": "EM_06",
                                "title": "Music can evoke my memories of past people and places",
                                "choices": [
                                    {
                                        "value": 1,
                                        "text": "completely disagree"
                                    },
                                    {
                                        "value": 2,
                                        "text": "strongly disagree"
                                    },
                                    {
                                        "value": 3,
                                        "text": "disagree"
                                    },
                                    {
                                        "value": 4,
                                        "text": "neither agree nor disagree"
                                    },
                                    {
                                        "value": 5,
                                        "text": "agree"
                                    },
                                    {
                                        "value": 6,
                                        "text": "strongly agree"
                                    },
                                    {
                                        "value": 7,
                                        "text": "completely agree"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ),
        time_estimate=60 * 2,
        save_answer="questionnaire",
        bot_response="not yet implemented",
    )