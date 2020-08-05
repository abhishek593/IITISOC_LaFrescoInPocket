import random


def get_random_string():
    return '%32x' % random.getrandbits(16 * 8)
