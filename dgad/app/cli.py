import argparse
import logging
import os
from importlib import resources
from pathlib import Path

import dgad.models
from dgad.classification import TCNClassifier
from dgad.utils import create_domains_dataframe

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


def classify(args: argparse.Namespace) -> None:
    classifier = TCNClassifier()
    if not args.model:
        with resources.path(dgad.models, "tcn_best.h5") as model_path:
            classifier.load_keras_model(filepath=model_path)
    else:
        classifier.load_keras_model(filepath=args.model)
    if args.domains:
        classified_dataframe = classifier.classify_domains_in_dataframe(
            dataframe=create_domains_dataframe(domains=args.domains)
        )
    if args.csv:
        classified_dataframe = classifier.classify_domains_in_csv(csv_filepath=args.csv)
        logging.info(
            "classified %s domains from csv file %s",
            len(classified_dataframe),
            args.csv,
        )
    if not args.quiet:
        logging.critical(classified_dataframe)


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--domains",
        help="space separated list of 1 or more domains you want DGA detective to classify",
        nargs="*",
        metavar="DOMAIN",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--model",
        help="the hdf5 keras model file to pass to the classifier",
        type=Path,
        required=False,
    )
    parser.add_argument(
        "--csv",
        help="csv file containing the domains to classify. This file must have a column 'domain'. The classification will be stored in the same file under a column 'classification'",
        type=Path,
        required=False,
    )
    parser.add_argument(
        "-q", "--quiet", help="disables stdout", action="store_true", required=False
    )
    return parser


def main() -> None:
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=os.environ.get(key="LOG_LEVEL", default="ERROR").upper(),
    )
    parser = setup_parser()
    args = parser.parse_args()
    if args:
        classify(args)


if __name__ == "__main__":
    main()
