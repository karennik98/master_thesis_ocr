import argparse
import re

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Read labels file and create .txt files for all lines"
    )
    parser.add_argument(
        "--labels_file", type=str, nargs="?", help="The labels file", default="labels.txt"
    )
    return parser.parse_args()

def main(labels_path):
    file = open(labels_path, "r")
    lines = file.readlines()
    for line in lines:
        new_file_name = re.search(r'.+?.jpg', line).group()
        if new_file_name:
            new_file_name = new_file_name.replace("jpg", "txt")
            new_file = open(new_file_name, "w")
            line = re.sub(r'.+?.jpg ', '', line)
            new_file.write(line)
            new_file.close()

if __name__ == "__main__":
    args = parse_arguments()
    main(args.labels_file)