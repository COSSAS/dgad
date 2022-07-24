import logging
from dataclasses import dataclass, field
from typing import List

import tldextract

from dgad import utils

CHARACTERS_DICTIONARY = {
    "0": 1,
    "1": 2,
    "2": 3,
    "3": 4,
    "4": 5,
    "5": 6,
    "6": 7,
    "7": 8,
    "8": 9,
    "9": 10,
    "a": 11,
    "b": 12,
    "c": 13,
    "d": 14,
    "e": 15,
    "f": 16,
    "g": 17,
    "h": 18,
    "i": 19,
    "j": 20,
    "k": 21,
    "l": 22,
    "m": 23,
    "n": 24,
    "o": 25,
    "p": 26,
    "q": 27,
    "r": 28,
    "s": 29,
    "t": 30,
    "u": 31,
    "v": 32,
    "w": 33,
    "x": 34,
    "y": 35,
    "z": 36,
    "-": 38,
    "_": 39,
    ".": 40,
}


@dataclass
class Word:
    """
    A word is the smallest unit on which we can peform classification
    """

    value: str
    padded_length: int = 0
    padded_token_vector: List[int] = field(default_factory=list)
    binary_score: float = 0.0
    binary_label: str = ""
    family_score: float = 0.0
    family_label: str = "N/A"

    def __post_init__(self) -> None:
        """
        preprocessing. if padded length is not provided (default=0) then sets it to the length of the string
        """
        sanitised_value = utils.strip_forbidden_characters(
            word=self.value, characters_dictionary=CHARACTERS_DICTIONARY
        )
        token_vector = utils.tokenize_word(
            word=sanitised_value, characters_dictionary=CHARACTERS_DICTIONARY
        )
        if not self.padded_length:
            self.padded_length = len(self.value)
        self.padded_token_vector = utils.pad_vector(
            vector=token_vector, desired_length=self.padded_length
        )


@dataclass
class Domain:
    raw: str
    words: List[Word] = None
    suffix: str = ""
    is_dga: bool = False
    family_label: str = "N/A"
    padded_length: int = 0

    def __post_init__(self) -> None:
        raw_subdomains, raw_domain_name, self.suffix = tldextract.extract(
            utils.remove_prefix(self.raw, "www.")
        )
        raw_words = []
        raw_words.append(raw_domain_name)
        if raw_subdomains:
            raw_words += list(set(raw_subdomains.split(".")))
        self.words = [Word(raw_word, self.padded_length) for raw_word in raw_words]
        logging.debug(self)

    def set_family(
        self,
        binary_confidence_threshold: float = 0.5,
        family_confidence_threshold: float = 0,
    ):
        """
        sets the domain family to be the one from the word with the highest family score
        """
        max_family_score = family_confidence_threshold
        for word in self.words:
            if word.binary_score > binary_confidence_threshold:
                if word.family_score > max_family_score:
                    max_family_score = word.family_score
                    self.family_label = word.family_label
