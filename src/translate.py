import json
import re
from typing import List

alphabet = json.load(open("constants/alphabet.json"))


class Translate:
    def parse_text(self, text: str) -> List[str]:

        temp = re.sub(' ', '\t \t', text)
        text_list = temp.split('\t')

        return text_list

    def verify_lowercase(self, text: str) -> bool:
        return text.islower()

    def verify_uppercase(self, text: str) -> bool:
        return text.isupper()

    def convert_to_braille(self, text: str) -> str:
        in_braille = ""
        for character in text.lower():

            if character in alphabet:
                in_braille += f" {alphabet[character]}"

        return in_braille

    def translate(self, phrase: List[str]) -> str:
        result = ""
        if self.verify_uppercase("".join(phrase)):
            result = f"25 46 46" + self.convert_to_braille("".join(phrase))
        else:
            for word in phrase:
                if len(word) > 1 and self.verify_uppercase(word):
                    result += f" 46 46{self.convert_to_braille(word)}"
                elif self.verify_lowercase(word):
                    result += self.convert_to_braille(word)
                else:
                    for char in word:
                        if(self.verify_uppercase(char)):
                            result += f" 46{self.convert_to_braille(char)}"
                        else:
                            result += self.convert_to_braille(char)
        return result

    def run(self, text: str) -> str:
        result = self.parse_text(text)

        return self.translate(result)
