import argparse

from parsers import get_payload

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help='File to process.')


args = parser.parse_args()


with open(args.file, 'r') as file:
    lines = file.read()
    print(get_payload(lines))
