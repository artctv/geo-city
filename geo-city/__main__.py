import argparse
from .main import run


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
    help="how many data need to load, by default load all"
)


if __name__ == "__main__":
    args = parser.parse_args()
    data = run(args.temp, args.data_count)
