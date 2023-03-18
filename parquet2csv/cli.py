import pyarrow.parquet as pq
import argparse

description = (
    "Dumps a given Parquet file to CSV (efficiently)."
)

def main():
    parser = argparse.ArgumentParser(description=description)

    # user gives Parquet file and CSV file
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
    parser.add_argument(
        "--chunk-size",
        required=False,
        help="How many rows to read/write at a time",
        type=int,
        default=10000,
    )
    args = parser.parse_args()

    # create a Parquet file reader
    parquet_reader = pq.ParquetFile(args.parquet)

    # get the number of rows in the Parquet file
    num_rows = parquet_reader.metadata.num_rows

    # create a CSV file writer
    csv_writer = open(args.csv, 'w')

    # write the column names to the CSV file
    schema = parquet_reader.schema
    csv_writer.write(','.join(schema.names) + '\n')

    # read and write the Parquet file in chunks
    for i in range(0, num_rows, args.chunk_size):
        table = parquet_reader.read_row_group(i)
        df = table.to_pandas()
        df.to_csv(csv_writer, header=False, index=False)
        del table, df

    # close the CSV file writer
    csv_writer.close()
