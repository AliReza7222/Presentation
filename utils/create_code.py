import random

from string import ascii_letters, digits


class CreateCode:
    SPECIAL_LETTERS = '@%$#(){}!*&^~|<>'

    @classmethod
    def get_token(cls) -> str:
        list_words = list(cls.SPECIAL_LETTERS + digits + ascii_letters)
        return "".join(random.choices(list_words, k=258))
