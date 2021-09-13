from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

import numpy as np

import dgad.utils as utils


@dataclass
class Word:
    """
    A word is the smallest unit that can be reasonably classified as produced by a DGA.
    A subdomain is just a word.
    """

    name: str
    characters_dictionary: Dict[str, int]
    padded_length: int
    padded_token_vector = [0]
    binary_prediction: int = 0

    def __post_init__(self) -> None:
        """
        word preprocessing
        """
        sanitised_name = utils.strip_forbidden_characters(
            word=self.name, characters_dictionary=self.characters_dictionary
        )
        token_vector = utils.tokenize_word(
            word=sanitised_name, characters_dictionary=self.characters_dictionary
        )
        self.padded_token_vector = utils.pad_vector(
            vector=token_vector, desired_length=self.padded_length
        )


class Domain:
    """
    RFC 1035 Domain Name.
    Can have 0 or more subdomains, which are Words.
    """

    domain_name: Word

    def __init__(
        self,
        raw: str,
        padded_length: int,
        characters_dictionary: Dict[str, int],
        labels_dictionary: Dict[int, str],
    ):
        self.raw = raw
        self.labels_dictionary = labels_dictionary
        raw_domain_name, list_raw_subdomains = utils.extract_domain_name_and_subdomains(
            self.raw
        )
        self.domain_name = Word(raw_domain_name, characters_dictionary, padded_length)
        self.subdomains = [
            Word(
                name=subdomain,
                characters_dictionary=characters_dictionary,
                padded_length=padded_length,
            )
            for subdomain in list_raw_subdomains
        ]
        self.binary_label: str = ""

    def update_label(self) -> None:
        binary_prediction = self.__get_overall_prediction__()
        self.binary_label = self.__get_human_label__(binary_prediction)

    def __get_overall_prediction__(self) -> int:
        if self.domain_name.binary_prediction == 1:
            return 1
        for subdomain in self.subdomains:
            if subdomain.binary_prediction == 1:
                return 1
        else:
            return 0

    def __get_human_label__(self, binary_prediction: int) -> str:
        return self.labels_dictionary[binary_prediction]

    def __hash__(self) -> int:
        return hash(self.raw)


def get_all_subdomains(domains: List[Domain]) -> List[Word]:
    """
    returns a list of all the subdomains from the provided Domains
    """
    subdomains: List[Word] = []
    for domain in domains:
        for subdomain in domain.subdomains:
            subdomains.append(subdomain)
    return subdomains


def get_all_padded_token_vectors(domains: List[Domain]) -> np.ndarray:
    """
    returns a list of all the padded token vectors from the provided Domains
    """
    subdomains = get_all_subdomains(domains=domains)
    domains_vectors = [domain.domain_name.padded_token_vector for domain in domains]
    subdomains_vectors = [subdomain.padded_token_vector for subdomain in subdomains]
    return np.array(domains_vectors + subdomains_vectors)


def set_all_words_predictions(predictions: np.ndarray, words: Sequence[Word]) -> None:
    """
    for each word, stores the prediction from the array to
    the binary_prediction attribute of the Word
    """
    for index, prediction in enumerate(predictions):
        word = words[index]
        word.binary_prediction = prediction[0]


def set_all_predictions(domains: List[Domain], predictions: np.ndarray) -> None:
    """
    for each domain, stores the prediction from the array to
    all the domain names and subdomains
    """
    domain_names = [domain.domain_name for domain in domains]
    subdomains = get_all_subdomains(domains=domains)
    predictions_domain_names, predictions_subdomains = np.split(
        predictions, [len(domains)]
    )
    set_all_words_predictions(predictions=predictions_domain_names, words=domain_names)
    set_all_words_predictions(predictions=predictions_subdomains, words=subdomains)
