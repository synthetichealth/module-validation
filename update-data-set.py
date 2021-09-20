import argparse
import os
from pathlib import Path
from zipfile import ZipFile, ZIP_BZIP2
import multiprocessing as mp

# This script will take Synthea CSV output files, compress them and
# put them in the data-set directory. The source directory is passed
# in on the command line.
def parse_args():
    """Handle command line arguments."""
    p = argparse.ArgumentParser()
    p.add_argument(
        "--inputdir",
        default=None,
        help="Directory of Synthea CSV files",
    )
    return p.parse_args()


def main(args):
  output_dir = Path('data-set')
  csv_files = filter(lambda f: f.endswith('.csv'), os.listdir(args.inputdir))
  with mp.Pool(processes=8) as pool:
    for csv_file in csv_files:
      pool.apply_async(handle_file, (csv_file, args.inputdir, output_dir))
    pool.close()
    pool.join()


def handle_file(csv_file, inputdir, output_dir):
  csv_file_path = Path(inputdir, csv_file)
  output_file_name = csv_file_path.stem + '.zip'
  with ZipFile(Path(output_dir, output_file_name), 'w', compression=ZIP_BZIP2) as compressed_csv:
    compressed_csv.write(csv_file_path, os.path.basename(csv_file))

if __name__ == "__main__":
    args = parse_args()
    main(args)
