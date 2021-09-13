from dgad.app import cli


def test_classify():
    parser = cli.setup_parser()
    args = parser.parse_args(["--domains", "wikipedia.org"])
    cli.classify(args)
    parser = cli.setup_parser()
    args = parser.parse_args(["--csv", "tests/data/domains_todo_labelled.csv"])
    cli.classify(args)
