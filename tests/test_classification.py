import os
from importlib import resources

import numpy as np
import pandas as pd
import pytest
import tldextract
from pytest import fixture

import dgad.models
from dgad import utils as utils
from dgad.classification import LSTMClassifier, TCNClassifier
from dgad.data_model import Word

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


@fixture
def train_domains():
    raw_domains = [
        "wikipedia.org",
        "haksjdfhasfewuy.ru",
        "laskhafkjhkajsdhfaskjdhfljksadhflkjasdhflkjsdhilaweuhflkjnvkljdszbvlkjbaljkehrbvljhdfskgkjsdgbveiruaygfroeiuhfgiuhsdfjhkvjffkljadshfjlkhewiuhflirf.com",
    ]
    padded_length = len(max(raw_domains, key=len))
    characters_dictionary = utils.create_characters_dictionary()
    _, domain_names, _ = [tldextract.extract(domain) for domain in raw_domains]
    return [
        Word(
            name=domain_name,
            padded_length=padded_length,
            characters_dictionary=characters_dictionary,
        )
        for domain_name in domain_names
    ]


@fixture
def x_train(train_domains):
    return np.array([word.padded_token_vector for word in train_domains])


@fixture
def y_train():
    return np.asarray([0, 1, 1])


@fixture
def lstm_classifier():
    lstm_classifier = LSTMClassifier()
    with resources.path(dgad.models, "lstm_best.h5") as model_path:
        lstm_classifier.load_keras_model(filepath=model_path)
    return lstm_classifier


@fixture
def tcn_classifier():
    tcn_classifier = TCNClassifier()
    with resources.path(dgad.models, "tcn_best.h5") as model_path:
        tcn_classifier.load_keras_model(filepath=model_path)
    return tcn_classifier


@fixture
def classifiers(lstm_classifier, tcn_classifier):
    return [lstm_classifier, tcn_classifier]


def test_train_keras_model(tmpdir, x_train, y_train, classifiers):
    checkpoints_directory = tmpdir.mkdir("checkpoints")
    for classifier in classifiers:
        classifier.initialise_keras_model(x_train=x_train)
        classifier.train_keras_model(
            x_train=x_train,
            y_train=y_train,
            epochs=1,
            checkpoints_directory=checkpoints_directory,
        )


@fixture
def test_dataframe():
    test_examples = [
        {"domain": "wikipedia.org", "expected_classification": "ok"},
        {"domain": "kajsdhflaksdjhfaskdj.com", "expected_classification": "DGA"},
        {"domain": "mail.google.com", "expected_classification": "ok"},
        {"domain": "*invalid.domain.com", "expected_classification": "ok"},
    ]
    return pd.DataFrame.from_dict(test_examples)


def test_label_domains(test_dataframe, classifiers):
    for classifier in classifiers:
        test_dataframe = classifier.classify_domains_in_dataframe(test_dataframe)
        assert (
            test_dataframe["classification"].all()
            == test_dataframe["expected_classification"].all()
        )


def test_no_model(test_dataframe):
    classifier_no_model = TCNClassifier()
    assert classifier_no_model.model is None
    with pytest.raises(SystemExit):
        classifier_no_model.classify_domains_in_dataframe(dataframe=test_dataframe)


def test_predict_binary_empty_x_test(classifiers):
    for classifier in classifiers:
        full_x_test = np.ones([10, classifier.model.input_shape[1]])
        empty_x_test = np.ones([0, classifier.model.input_shape[1]])
        # assert this does not raise an exception
        classifier.__predict_binary_labels__(x_test=full_x_test)
        # assert this does raise an exception
        with pytest.raises(ValueError):
            classifier.__predict_binary_labels__(x_test=empty_x_test)


def test_classify_raw_domains(classifiers):
    for classifier in classifiers:
        classified_domains = classifier.classify_raw_domains(
            ["wikipedia.org", "fkjshdkajsdhfalksdf.com"]
        )
        for domain in classified_domains:
            if domain.raw == "fkjshdkajsdhfalksdf.com":
                assert domain.binary_label is "DGA"
            elif domain.raw == "wikipedia.org":
                assert domain.binary_label is "ok"
