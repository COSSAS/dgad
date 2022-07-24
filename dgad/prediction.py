import logging
import os
from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import tensorflow
from tcn import TCN

import dgad.label_encoders
import dgad.models
from dgad.schema import Domain, Word
from dgad.utils import load_labels, log_analysis, separate_domains_that_are_too_long

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


def default_binary_labels():
    return {0: "benign", 1: "DGA"}


def default_custom_objects():
    return {}


@dataclass
class Model:
    filepath: Path
    data: Any = None
    labels: Dict[int, str] = field(default_factory=default_binary_labels)
    optimizer: str = "adam"
    loss: str = "binary_crossentropy"
    custom_objects: Dict[str, str] = field(default_factory=default_custom_objects)

    def __post_init__(self):
        self.data = tensorflow.keras.models.load_model(
            filepath=self.filepath, custom_objects={"TCN": TCN}
        )
        self.data.compile(loss=self.loss, optimizer=self.optimizer)


class Detective:
    def __init__(self, model_binary: Model = None, model_multi: Model = None) -> None:
        # use included binary model if one is not provided
        if model_binary:
            self.model_binary = model_binary
        else:
            with resources.path(dgad.models, "tcn_best.h5") as model_path:
                self.model_binary = Model(
                    filepath=model_path, custom_objects={"TCN": TCN}
                )
        # use included family model if one is not provided
        if model_multi:
            self.model_multi = model_multi
        else:
            with resources.path(dgad.models, "tcn_family_81_classes.h5") as model_path:
                with resources.path(
                    dgad.label_encoders, "encoder_81_classes.npy"
                ) as labels_path:
                    self.model_multi = Model(
                        filepath=model_path,
                        labels=load_labels(labels_path),
                        custom_objects={"TCN": TCN},
                    )

    def prepare_domains(
        self, raw_domains: List[str], max_length: int = 0
    ) -> Tuple[List[Domain], List[str]]:
        """
        preprocesses the domains, tokenizing and applying padding to have same size as binary model
        """
        # TODO: padding may be different for the multi model...! That could lead to issues. Same size should be documented or enforced...
        if not max_length:
            max_length = self.model_binary.data.input_shape[1]
        raw_domains_todo, domains_to_skip = separate_domains_that_are_too_long(
            raw_domains, max_length
        )
        domains_todo = [
            Domain(raw=raw_domain, padded_length=max_length)
            for raw_domain in raw_domains_todo
        ]
        if domains_to_skip:
            logging.warning(
                f"will skip domains {domains_to_skip} because they are too long for the binary model"
            )
        return domains_todo, domains_to_skip

    def investigate_binary(self, word: Word) -> None:
        x_test: np.ndarray = np.array([word.padded_token_vector])
        y_test: np.ndarray = self.model_binary.data.predict(x_test, verbose=0)
        word.binary_score = float(y_test[0][0])
        word.binary_label = self.model_binary.labels[int(np.round(word.binary_score))]

    def investigate_family(self, word: Word) -> None:
        x_test: np.ndarray = np.array([word.padded_token_vector])
        y_test = self.model_multi.data.predict(x_test, verbose=0)
        best_class_label_index = np.argmax(y_test, axis=1)[0]
        word.family_score = float(np.max(y_test, axis=1)[0])
        word.family_label = self.model_multi.labels[best_class_label_index]

    def investigate(self, domains: List[Domain]) -> None:
        """
        performs binary and family predictions on provided list of domains.
        predictions are stored in the words attributes
        """
        # TODO: test performance
        for domain in domains:
            is_dga = False
            for word in domain.words:
                self.investigate_binary(word)
                if word.binary_score > 0.5:
                    self.investigate_family(word)
                    is_dga = True
            if is_dga:
                domain.is_dga = True
                domain.set_family()
            log_analysis(domain)
