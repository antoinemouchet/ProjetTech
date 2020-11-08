from random import randint


def get_random_word():
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    word = ""
    for _ in range(6):
        word += letters[randint(0, 51)]

    return word
