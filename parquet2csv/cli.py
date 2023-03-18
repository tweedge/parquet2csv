import pandas
import argparse

description = (
    "Dumps a given Parquet file to CSV."
)

def main():
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "--parquet",
        required=True,
        help="The path to the Parquet file to dump",
    )
    parser.add_argument(
        "--csv",
        required=True,
        help="The path to the CSV file output the dump to",
    )
    args = parser.parse_args()

    dataframe = pandas.read_parquet(args.parquet)
    dataframe.to_csv(args.csv)