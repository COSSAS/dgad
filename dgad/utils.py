"""
utils module for lstm library
provides non lstm specific miscellaneous methods
"""

import logging
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import tldextract


def create_domains_dataframe(domains: List[str]) -> pd.DataFrame:
    return pd.DataFrame(domains, columns=["domain"])


def create_characters_dictionary() -> Dict[str, int]:
    #     digits = [digit for digit in range(10)]
    #     digit_to_str = [str(digit) for digit in digits]
    #     digits_str: Dict[str, int] = dict(zip(digit_to_str, range(1, 11)))
    #     letters: Dict[str, int] = dict(zip(string.ascii_lowercase, range(11, 38)))
    #     symbols: Dict[str, int] = dict(zip(["-", "_", "."], range(38, 41)))
    #     return {**digits_str, **letters, **symbols}
    return {
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


def strip_forbidden_characters(word: str, characters_dictionary: Dict[str, int]) -> str:
    allowed_characters = [character[0] for character in characters_dictionary]
    word = "".join((filter(lambda char: char in allowed_characters, word)))
    return word


def tokenize_word(word: str, characters_dictionary: Dict[str, int]) -> List[int]:
    """
    breaks a word into individual token units from the characters_dictionary
    @param characters_dictionary: dictionary of tokens
    @param word: word to tokenize
    @return: vector of word tokens
    """
    word_characters = [character for character in word]
    vector: List[int] = [characters_dictionary[_] for _ in word_characters]
    return vector


def remove_prefix(text: str, prefix: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def pad_vector(vector: List[int], desired_length: int) -> List[int]:
    padding = [0] * (desired_length - int(len(vector)))
    return vector[:desired_length] + padding


def random_split_train_test(
    domain_names_df: pd.DataFrame, split_ratio: float = 0.8
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_set_df = pd.DataFrame()
    test_set_df = pd.DataFrame()
    if 0 < split_ratio < 1.0:
        train_set = np.random.rand(len(domain_names_df)) < split_ratio
        train_set_df = domain_names_df[train_set]
        test_set_df = domain_names_df[~train_set]
    else:
        logging.error(msg="split_ratio must be between 0 and 1")
    return train_set_df, test_set_df


def extract_domain_name_and_subdomains(raw_domain: str) -> Tuple[str, List[str]]:
    raw_subdomains, raw_domain_name, _ = tldextract.extract(
        remove_prefix(raw_domain, "www.")
    )
    raw_subdomains = list(set(raw_subdomains.split(".")))
    return raw_domain_name, raw_subdomains


def separate_domains_that_are_too_long(
    domains: List[str], max_size: int
) -> Tuple[List[str], List[str]]:
    domains_shorter_or_equal = [domain for domain in domains if len(domain) <= max_size]
    domains_too_long = set(domains) - set(domains_shorter_or_equal)
    return domains_shorter_or_equal, list(domains_too_long)
