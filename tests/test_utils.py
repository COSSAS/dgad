from importlib import resources

import dgad.label_encoders
import dgad.schema
from dgad.utils import (
    load_labels,
    separate_domains_that_are_too_long,
    strip_forbidden_characters,
)


def test_load_labels():
    with resources.path(dgad.label_encoders, "encoder_81_classes.npy") as labels_path:
        _ = load_labels(labels_path)


def test_strip_forbidden_characters():
    entries = [
        {"input": "wikipedia", "output": "wikipedia"},
        {"input": "*wikipedia", "output": "wikipedia"},
        {"input": "/'wikipedia", "output": "wikipedia"},
    ]
    characters_dictionary = dgad.schema.CHARACTERS_DICTIONARY
    for entry in entries:
        assert (
            strip_forbidden_characters(
                word=entry["input"], characters_dictionary=characters_dictionary
            )
            == entry["output"]
        )


def test_separate_domains_that_are_too_long():
    domains = ["abc.com", "wikipedia.org", "sdajhflakjsdhflkasdjhflaksdjhf.ru"]
    shorter_equal, longer = separate_domains_that_are_too_long(domains, max_size=13)
    assert shorter_equal == ["abc.com", "wikipedia.org"]
    assert longer == ["sdajhflakjsdhflkasdjhflaksdjhf.ru"]
