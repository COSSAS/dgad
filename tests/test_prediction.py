from importlib import resources

import dgad.label_encoders
import dgad.models
from dgad.prediction import Detective, Model
from dgad.schema import Domain
from dgad.utils import load_labels


def test_detective():
    default = Detective()
    with resources.path(dgad.models, "tcn_family_52_classes.h5") as model_path:
        with resources.path(
            dgad.label_encoders, "encoder_52_classes.npy"
        ) as labels_path:
            model_multi_52 = Model(filepath=model_path, labels=load_labels(labels_path))
    custom = Detective(model_multi=model_multi_52)


def test_detection():
    det = Detective()
    padding = det.model_binary.data.input_shape[1]
    domains = [
        Domain(raw=value, padded_length=padding)
        for value in [
            "google.com",
            "mail.google.com",
            "jksdfhklajsdhflaksdjfhalskdj.org",
        ]
    ]
    det.investigate(domains)
    pass
