import random
import string
from uuid import uuid4


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


def check_if_dicts_match(d1: dict, d2: dict) -> bool:
    return set(d1.keys()) == set(d2.keys())
