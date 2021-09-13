import logging
import os
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List

import numpy as np
import pandas as pd
import tensorflow
import tensorflow.keras as keras
from tcn import TCN
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import LSTM, Activation, Dense, Dropout, Embedding, Input
from tensorflow.keras.models import Model, Sequential

from dgad.data_model import Domain, get_all_padded_token_vectors, set_all_predictions
from dgad.utils import create_characters_dictionary, separate_domains_that_are_too_long


class GenericClassifier(ABC):
    """
    Abstract base class for the specialised classifiers
    """

    def __init__(
        self,
        optimizer: str,
        loss: str = "binary_crossentropy",
        abnormal_label: str = "DGA",
        normal_label: str = "ok",
        model: Any = None,
    ):
        self.normal_label = normal_label
        self.abnormal_label = abnormal_label
        self.model = model
        self.loss = loss
        self.optimizer = optimizer
        self.characters_dictionary = create_characters_dictionary()
        self.labels_dictionary = {1: self.abnormal_label, 0: self.normal_label}

    @abstractmethod
    def initialise_keras_model(self, x_train: np.ndarray) -> None:  # pragma: no cover
        pass

    def train_keras_model(
        self,
        x_train: np.ndarray,
        y_train: np.ndarray,
        checkpoints_directory: Path,
        epochs: int = 5,
        save_best_only: bool = True,
    ) -> keras.callbacks.History:
        checkpoint = ModelCheckpoint(
            filepath=os.path.join(
                checkpoints_directory, "checkpoint-{epoch:02d}-{loss:.2f}.hdf5"
            ),
            monitor="loss",
            verbose=0,
            save_best_only=save_best_only,
            mode="max",
        )
        callbacks_list = [checkpoint]
        return self.model.fit(
            x_train,
            y_train,
            batch_size=16,
            epochs=epochs,
            callbacks=callbacks_list,
            shuffle=True,
        )

    def load_keras_model(self, filepath: Path) -> Any:
        self.model = tensorflow.keras.models.load_model(filepath=filepath)
        self.model.compile(loss=self.loss, optimizer=self.optimizer)

    def __predict_binary_labels__(self, x_test: np.ndarray) -> np.ndarray:
        return (self.model.predict(x_test) > 0.5).astype("int32")

    def __classify_domains_binary__(self, domains: List[Domain]) -> None:
        x_test = get_all_padded_token_vectors(domains=domains)
        predicted_labels = self.__predict_binary_labels__(x_test=x_test)
        set_all_predictions(domains=domains, predictions=predicted_labels)
        for domain in domains:
            domain.update_label()

    def __label_domains__(
        self,
        domains: List[Domain],
        domains_too_long: List[Domain],
        binary_classification: bool = True,
    ) -> List[Domain]:
        if binary_classification:
            self.__classify_domains_binary__(domains=domains)
            for domain in domains_too_long:
                domain.binary_label = "N/A - domain too long for model"
        return domains

    def __classify_dataframe__(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        raw_domains = dataframe["domain"]
        raw_domains_todo, raw_domains_too_long = separate_domains_that_are_too_long(
            raw_domains, self.model.input_shape[1]
        )
        domains_todo = [
            Domain(
                raw_domain,
                self.model.input_shape[1],
                self.characters_dictionary,
                self.labels_dictionary,
            )
            for raw_domain in raw_domains_todo
        ]
        domains_too_long = [
            Domain(
                raw_domain,
                self.model.input_shape[1],
                self.characters_dictionary,
                self.labels_dictionary,
            )
            for raw_domain in raw_domains_too_long
        ]
        self.__label_domains__(
            domains=domains_todo,
            domains_too_long=domains_too_long,
            binary_classification=True,
        )
        dataframe["classification"] = [domain.binary_label for domain in domains_todo]
        return dataframe

    def classify_domains_in_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        high level method to interact with
        """
        if "domain" not in dataframe.columns:
            logging.critical(
                "the dataframe does not contain the required column 'domain'!"
            )
            sys.exit()
        if self.model:
            return self.__classify_dataframe__(dataframe)
        logging.critical(msg="can not perform classification without a model!")
        sys.exit(1)

    def classify_raw_domains(self, raw_domains: List[str]) -> List[Domain]:
        domains = [
            Domain(
                raw=raw_domain,
                padded_length=self.model.input_shape[1],
                characters_dictionary=self.characters_dictionary,
                labels_dictionary=self.labels_dictionary,
            )
            for raw_domain in raw_domains
        ]
        self.__classify_domains_binary__(domains=domains)
        for domain in domains:
            domain.update_label()
        return domains

    def classify_domains_in_csv(self, csv_filepath: Path) -> pd.DataFrame:
        dataframe = pd.read_csv(csv_filepath)
        classified_dataframe = self.classify_domains_in_dataframe(dataframe=dataframe)
        classified_dataframe.to_csv(csv_filepath, index=False)
        return dataframe


class LSTMClassifier(GenericClassifier):
    """
    Specialised LSTM implementation of GenericClassifier
    """

    def __init__(self, optimizer: str = "rmsprop"):
        super().__init__(optimizer)

    def initialise_keras_model(self, x_train: np.ndarray) -> None:
        max_features = 1024
        max_domain_length = x_train.shape[1]
        model = Sequential()
        model.add(Embedding(max_features, 128, input_length=max_domain_length))
        model.add(LSTM(128))
        model.add(Dropout(0.5))
        model.add(Dense(1))
        model.add(Activation("sigmoid"))
        model.compile(loss=self.loss, optimizer=self.optimizer)
        self.model = model


class TCNClassifier(GenericClassifier):
    """
    Specialised TCN implementation of GenericClassifier
    """

    def __init__(self, optimizer: str = "adam"):
        super().__init__(optimizer)

    def initialise_keras_model(self, x_train: np.ndarray) -> None:
        max_features = 1024
        max_domain_length = x_train.shape[1]
        i = Input(batch_shape=(None, x_train.shape[1]))
        # embedding layer to map the input to from 2D to 3D tensor
        e = Embedding(max_features, 128, input_length=max_domain_length)(i)
        o = TCN(
            nb_filters=8,
            kernel_size=4,
            nb_stacks=1,
            dilations=[1, 2, 4, 8, 16, 32],
            padding="same",
            use_skip_connections=True,
            return_sequences=False,
        )(
            e
        )  # The TCN layers are here.
        o = Dense(1)(o)
        o = Activation("sigmoid")(o)
        self.model = Model(inputs=[i], outputs=[o])
        self.model.compile(loss=self.loss, optimizer=self.optimizer)

    def load_keras_model(self, filepath: Path) -> Any:
        self.model = tensorflow.keras.models.load_model(
            filepath=filepath, custom_objects={"TCN": TCN}
        )
        self.model.compile(loss=self.loss, optimizer=self.optimizer)
