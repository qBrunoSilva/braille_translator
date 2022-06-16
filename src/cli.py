import argparse
import json
import os
from .translate import Translate

alphabet = json.load(open("constants/alphabet.json"))


class CLI(object):

    def __init__(self):
        self.args = self.parse_args()

    def parse_args(self) -> argparse.Namespace:

        parser = argparse.ArgumentParser(
            add_help=True,
            description="Helper for managing the configuration of the braille translator",
            usage="dt --help",
        )

        parser.add_argument(
            "--path", "-p", type=str, help="Path to the file to be analyzed", required=True
        )

        parser.add_argument(
            "--output", "-o", type=str, help="Output file path", default=os.path.abspath("./output.txt"),
        )

        return parser.parse_args()

    def read_txt_file(self, path: str) -> str:
        if not os.path.isfile(path) and not path.lower().endswith(".txt"):
            raise Exception(f"File {path} does not exist or is not a txt file")

        with open(os.path.abspath(path), "r") as f:
            return f.read()

    def save_txt_file(self, path: str, text: str) -> None:
        with open(os.path.abspath(path), "w") as f:
            f.write(text.replace(alphabet['\n'], "\n"))

    def run(self) -> None:
        text = self.read_txt_file(self.args.path)
        print("Original text:", text + "\n")

        translator = Translate().run(text=text)
        print("Result translator:", translator)

        self.save_txt_file(self.args.output, translator)


if __name__ == "__main__":
    CLI().run()
