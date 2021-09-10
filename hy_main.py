import argparse
import errno
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import random as rnd
import string
import sys
from multiprocessing import Pool

from tqdm import tqdm

from trdg.data_generator import FakeTextDataGenerator
from trdg.string_generator import (create_strings_from_dict,
                                   create_strings_from_file,
                                   create_strings_from_wikipedia,
                                   create_strings_randomly)
from trdg.utils import load_dict, load_fonts

output_dir="hy_images"
format=32
extension=1
skew_angle=0
random_skew=False
blur=0
random_blur=False
background=0
distorsion=0
distorsion_orientation=0
handwritten=False
name_format=0
width=100
alignment=1
text_color="#282828"
orientation=0
space_width=1.0
character_spacing=0
marginss=(5, 5, 5, 5)
fit=False
output_mask=0
word_split=False
image_dir=os.path.join(os.path.split(os.path.realpath(__file__))[0], "images")
stroke_width=0
stroke_fill="#282828"
image_mode="RGB"
length=1
random=False
count=200
font_dir="/home/karen/master/data-generator/TextRecognitionDataGenerator/trdg/fonts/hy"


def margins(margin):
    margins = margin.split(",")
    if len(margins) == 1:
        return [int(margins[0])] * 4
    return [int(m) for m in margins]

def main():
    """
        Description: Main function
    """
    # Create the directory if it does not exist.
    try:
        os.makedirs(output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Creating word list
    lang_dict = []
    if os.path.isfile("/home/karen/master/data-generator/TextRecognitionDataGenerator/trdg/dicts/hy.txt"):
        with open("/home/karen/master/data-generator/TextRecognitionDataGenerator/trdg/dicts/hy.txt", "r", encoding="utf8", errors="ignore") as d:
            lang_dict = [l for l in d.read().splitlines() if len(l) > 0]
    else:
        sys.exit("Cannot open dict")

    # Create font (path) list
    if font_dir:
        fonts = [
            os.path.join(font_dir, p)
            for p in os.listdir(font_dir)
            if os.path.splitext(p)[1] == ".ttf"
        ]

    # Creating synthetic sentences (or word)
    strings = []
    strings = create_strings_from_dict(
        length, random, count, lang_dict
    )
    case = "lower"
    if case == "upper":
        strings = [x.upper() for x in strings]
    if case == "lower":
        strings = [x.lower() for x in strings]

    string_count = len(strings)

    thread_count = 1
    p = Pool(thread_count)
    for _ in tqdm(
        p.imap_unordered(
            FakeTextDataGenerator.generate_from_tuple,
            zip(
                [i for i in range(0, string_count)],
                strings,
                [fonts[rnd.randrange(0, len(fonts))] for _ in range(0, string_count)],
                output_dir * string_count,
                format * string_count,
                extension * string_count,
                skew_angle * string_count,
                random_skew * string_count,
                blur * string_count,
                random_blur * string_count,
                background * string_count,
                distorsion * string_count,
                distorsion_orientation * string_count,
                handwritten * string_count,
                name_format * string_count,
                width * string_count,
                alignment * string_count,
                text_color * string_count,
                orientation * string_count,
                space_width * string_count,
                character_spacing * string_count,
                marginss * string_count,
                fit * string_count,
                output_mask * string_count,
                word_split * string_count,
                image_dir * string_count,
                stroke_width * string_count,
                stroke_fill * string_count,
                image_mode * string_count,
            ),
        ),
        total=count,
    ):
        pass
    p.terminate()

    if name_format == 2:
        # Create file with filename-to-label connections
        with open(
            os.path.join(output_dir, "labels.txt"), "w", encoding="utf8"
        ) as f:
            for i in range(string_count):
                file_name = str(i) + "." + extension
                if space_width == 0:
                    file_name = file_name.replace(" ", "")
                f.write("{} {}\n".format(file_name, strings[i]))


if __name__ == "__main__":
    main()
