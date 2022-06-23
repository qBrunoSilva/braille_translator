import argparse
import os
from .translate import Translator


class CLI:
    def __init__(self):
        self.args = self.parse_args()

    def parse_args(self) -> argparse.Namespace:
        # Recebe os argumentos da linha de comando

        parser = argparse.ArgumentParser(
            add_help=True,
            description="Auxiliar para gerenciar a configuração do tradutor Braille",
            usage="dt --help",
        )

        parser.add_argument(
            "--path", "-p", type=str, help="Caminho do arquivo a ser analisado", required=True
        )

        parser.add_argument(
            "--output", "-o", type=str, help="Caminho do arquivo de saída", default=os.path.abspath("./output.txt"),
        )

        return parser.parse_args()

    def read_txt_file(self, path: str) -> str:
        # Lê o arquivo de texto

        if not os.path.isfile(path) and not path.lower().endswith(".txt"):
            raise Exception(f"File {path} does not exist or is not a txt file")

        with open(os.path.abspath(path), "r") as f:
            return f.read()

    def save_txt_file(self, path: str, text: str) -> None:
        # Salva o arquivo de texto

        with open(os.path.abspath(path), "w") as f:
            f.write(text)

    def run(self) -> None:
        # Executa o programa

        text = self.read_txt_file(self.args.path)

        print("Original text:", text + "\n")
        result = Translator().translate(text=text)
        print("Result translator:", result)

        self.save_txt_file(self.args.output, result)


if __name__ == "__main__":
    CLI().run()
