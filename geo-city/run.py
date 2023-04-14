import argparse
from main import main


parser = argparse.ArgumentParser(description="Load data param")
parser.add_argument(
    "-t", "--temp",
    default=False,
    action=argparse.BooleanOptionalAction,
    help="load from temp data or not"
)
parser.add_argument(
    "-dc", "--data-count",
    nargs="?",
    default=0,
    type=int,
    help="how many data need to load, by default load all"
)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.temp, args.data_count)
