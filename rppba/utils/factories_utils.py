import random
import uuid


def generate_barcode(symbols_count=13):
    digits_list = [random.randint(0, 9) for i in range(symbols_count)]
    return ''.join(map(str, digits_list))


def generate_random_string(symbols_count=20):
    return str(uuid.uuid4())[:symbols_count]


def enum_choices_factory(enum_cls):
    return tuple([(member.value, member.value) for name, member in enum_cls.__members__.items()])
