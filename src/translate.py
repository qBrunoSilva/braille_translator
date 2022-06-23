import constants.AlphabetBraille as Alphabet

from typing import List

# Variaveis de "controle"
CAPITAL = chr(10272)  # ⠠
NUMBER = chr(10300)  # ⠼
UNRECOGNIZED = '?'


class Translator:

    def __init__(self):
        super().__init__()

    def parse_text(self, text: str) -> List[str]:
        # Divide uma frase com base em caracteres de espaço em branco (" ")
        # e nova linha ("\n").

        words = text.split(" ")
        result = []
        for word in words:
            temp = word.split("\n")
            for item in temp:
                result.append(item)
        return result

    def trim(self, word: str) -> str:
        # Remova a pontuação da palavra

        while len(word) != 0 and not word[0].isalnum():
            word = word[1:]
        while len(word) != 0 and not word[-1].isalnum():
            word = word[:-1]
        return word

    def numbers_handler(self, word: str) -> str:
        # Substitua cada grupo de números em uma palavra para sua
        # respectiva representação em braille

        if word == "":
            return word
        result = word[0]

        if word[0].isdigit():
            result = NUMBER + Alphabet.numbers.get(word[0]) + " "
        for i in range(1, len(word)):
            if word[i].isdigit() and word[i-1].isdigit():
                result += Alphabet.numbers.get(word[i]) + " "
            elif word[i].isdigit():
                result += NUMBER + Alphabet.numbers.get(word[i])
            else:
                result += word[i]

        return result

    def capital_letters_handler(self, word: str) -> str:
        # Coloque o código maiúsculo antes de cada letra/palavra maiúscula.

        if word == "":
            return word
        result = ""

        if len(word) > 1 and word.isupper():
            # Se a palavra for toda maiúscula adiciona o 2x código maíusculo
            # antes da palavra.

            result += CAPITAL + CAPITAL + word.lower()
        elif word[0].isupper() and word[1:].islower():
            # Caso contrário adiciona o 1x código antes da palavra.

            result += CAPITAL + word.lower()

        else:
            # Caso contrário adiciona o código antes de cada letra.

            for char in word:
                if char.isupper():
                    result += CAPITAL + char.lower()
                else:
                    result += char.lower()

        return result

    def character_to_braille(self, char: str) -> str:
        # Converta um caractere para braille.

        if char.isdigit() or char == CAPITAL or char == NUMBER:
            return char
        elif char == "\n":
            return "\n"
        elif char in Alphabet.letters and char.isupper():
            return CAPITAL + Alphabet.letters.get(char)
        elif char in Alphabet.letters:
            return Alphabet.letters.get(char)
        elif char in Alphabet.punctuation:
            return Alphabet.punctuation.get(char)
        else:
            return UNRECOGNIZED

    def convert_word_to_braille(self, word: str) -> str:
        # Converter uma palavra alfabética em braille.

        result = ""
        for char in word:
            result += f"{self.character_to_braille(char)} "
        return result

    def build_braille_word(self, trimmed_word: str,  shavings: str,  index: str,  braille: str) -> str:
        # Traduza uma palavra cortada para braille e,
        # em seguida, recoloque-as na palavra.

        if shavings == "":
            braille += self.convert_word_to_braille(trimmed_word)
        else:
            for i in range(0, len(shavings)):
                if i == index and trimmed_word != "":
                    braille += self.convert_word_to_braille(trimmed_word) \
                        .replace("  ", "(space)") \
                        .replace(" ", "") \
                        .replace("(space)", "  ")

                braille += self.convert_word_to_braille(shavings[i])

            if index == len(shavings):
                braille += self.convert_word_to_braille(trimmed_word)

        return braille

    def trate_word(self, word: str) -> str:
        # Trata o texto final removendo os espaços duplicados,
        # os espaços antes e depois do texto e
        # trocando os caracteres de controle

        return word[:-1] \
            .replace("  ", " (space) ") \
            .replace(CAPITAL, "46") \
            .replace(NUMBER, "3456")

    def translate(self, text: str) -> str:
        # Converte o texto para Braille.

        braille_text = ""
        words = self.parse_text(text)
        for word in words:
            word = self.numbers_handler(word)
            word = self.capital_letters_handler(word)
            trimmed_word = self.trim(word)
            untrimmed_word = word
            index = untrimmed_word.find(trimmed_word)
            shavings = untrimmed_word.replace(trimmed_word, "")
            braille_text = self.build_braille_word(
                trimmed_word, shavings, index, braille_text) + " "

        return self.trate_word(braille_text)
