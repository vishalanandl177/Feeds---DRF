import random


def mt_rand(low=0, high=0):
    """
        Generate a better random value
    """
    return random.randint(low, high)


def gen_rand_string(length, charset):
    num = ''
    for i in range(0, length):
        num += charset[mt_rand(0, len(charset) - 1)]
    return num

