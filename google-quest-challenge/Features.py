import string
import numpy as np


def character_density(search_for, search_in):
    return search_in.count(search_for) / len(search_in)


def punctuation_density(text: str):
    return sum([character_density(symbol, text) for symbol in string.punctuation])


class FormatFeatures:
    def __init__(self):
        # https://stackoverflow.com/editing-help
        # Maybe use regex here to identy specific pattern instead of only usage of these symbols
        self.formatting_pattern = [
            # Code
            "    ",
            "'''",
            "~~~",
            "`",
            # String formatting
            "*",
            "**",
            "***"
            # TODO: add further formatting pattern here
        ]

    def patternExists(self, text):
        return np.array([pattern in text for pattern in self.formatting_pattern])

    def patternDensity(self, text):
        return np.array([text.count(pattern) for pattern in self.formatting_pattern]) / len(text)
