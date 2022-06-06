import random
import string
from uuid import uuid4
from random import randint


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_unique_string() -> str:
    return uuid4().hex[:6].lower()


def random_dict_obj() -> dict:
    obj = {}
    obj[random_unique_string()] = random_lower_string()
    return obj


def random_listofdict_obj() -> list:
    li = []
    for _ in range(1, randint(2, 5)):
        obj = {}
        obj[random_unique_string()] = random_lower_string()
        li.append(obj)

    return li


def check_if_dicts_match(d1: dict, d2: dict) -> bool:
    return set(d1.keys()) == set(d2.keys())


def check_if_listofdicts_match(l1: list, l2: list) -> bool:
    length = len(l1) == len(l2)

    if not length:
        return False

    for i in l1:
        if i not in l2:
            return False

    return True
