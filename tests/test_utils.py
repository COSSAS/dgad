import os

import pandas as pd
import pytest

from dgad import utils


@pytest.fixture
def domains_list():
    return ["wikipedia.org", "dsjafhgskjhdfgskdjahfgdjkhsafgajskdh.org"]


@pytest.fixture
def data_directory():
    return "tests/data/"


@pytest.fixture
def training_df(data_directory):
    df_filepath = os.path.join(data_directory, "training_set-sample.csv")
    return pd.read_csv(df_filepath)


def test_random_split_train_test(training_df):
    train_df, test_df = utils.random_split_train_test(domain_names_df=training_df)
    train_df_2, test_df_2 = utils.random_split_train_test(domain_names_df=training_df)
    assert (
        len(train_df) + len(test_df)
        == len(train_df_2) + len(test_df_2)
        == len(training_df)
    )
    # for coverage
    train_df, test_df = utils.random_split_train_test(
        domain_names_df=training_df, split_ratio=66
    )


def test_strip_forbidden_characters():
    entries = [
        {"input": "wikipedia", "output": "wikipedia"},
        {"input": "*wikipedia", "output": "wikipedia"},
        {"input": "/'wikipedia", "output": "wikipedia"},
    ]
    characters_dictionary = utils.create_characters_dictionary()
    for entry in entries:
        assert (
            utils.strip_forbidden_characters(
                word=entry["input"], characters_dictionary=characters_dictionary
            )
            == entry["output"]
        )


def test_create_characters_dictionary():
    assert utils.create_characters_dictionary()


def test_separate_domains_that_are_too_long():
    domains = ["abc.com", "wikipedia.org", "sdajhflakjsdhflkasdjhflaksdjhf.ru"]
    shorter_equal, longer = utils.separate_domains_that_are_too_long(
        domains, max_size=13
    )
    assert shorter_equal == ["abc.com", "wikipedia.org"]
    assert longer == ["sdajhflakjsdhflkasdjhflaksdjhf.ru"]


def test_extract_domain_name_and_subdomains():
    assert ("wikipedia", [""]) == utils.extract_domain_name_and_subdomains(
        "wikipedia.org"
    )
    assert ("domain", ["subdomain"]) == utils.extract_domain_name_and_subdomains(
        "subdomain.domain.org"
    )
    assert ("domain", ["subdomain"]) == utils.extract_domain_name_and_subdomains(
        "subdomain.subdomain.domain.org"
    )
    name, subdomains = utils.extract_domain_name_and_subdomains("sub1.sub2.dom.com")
    assert name == "dom"
    assert set(subdomains) == set(["sub1", "sub2"])
