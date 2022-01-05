from collections import defaultdict
import random

import nltk
from nltk import chunk
import pyinputplus as pyip

nltk.download("words")


def chunkstring(string, length):
    return (string[0 + i : length + i] for i in range(0, len(string), length))


def count_unique_letters_in_string(string):
    return len(set(string))


def letter_points_for_word(word, letter_occurences):
    return sum([letter_occurences[letter] for letter in set(word)])


def select_guesses(candidates):

    letter_occurrences = defaultdict(int)
    for word in candidates:
        letters = set(word)
        for letter in letters:
            letter_occurrences[letter] += 1

    candidates_list = sorted(
        [
            (candidate, letter_points_for_word(candidate, letter_occurrences))
            for candidate in candidates
        ],
        key=lambda x: x[1],
        reverse=True,
    )

    num_to_return = min(len(candidates_list), 10)
    return [candidate for candidate, _ in candidates_list[:num_to_return]]


def generate_indices():
    five_letter_words = {
        word.lower() for word in nltk.corpus.words.words() if len(word) == 5
    }

    # The indices go [letter][in/not-in bool][slot]
    letter_position_indices = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
    letter_missing_indices = defaultdict(set)

    for letter in "abcdefghijklmnopqrstuvwxyz":
        for slot in range(0, 5):
            for word in five_letter_words:
                if word[slot] == letter:
                    letter_position_indices[letter][True][slot].add(word)
                elif letter in word:
                    letter_position_indices[letter][False][slot].add(word)

        for word in five_letter_words:
            if word.count(letter) == 0:
                letter_missing_indices[letter].add(word)

    return five_letter_words, letter_position_indices, letter_missing_indices


if __name__ == "__main__":
    (
        five_letter_words,
        letter_position_indices,
        letter_missing_indices,
    ) = generate_indices()
    candidates = five_letter_words.copy()

    all_missing_letters = []
    all_wrong_pos_letters = []
    all_correct_pos_letters = []

    print("")
    print(
        "Welcome to Wordless! The #1 app in the world for helping you cheat at wordle."
    )

    running = True
    while running:

        print("")
        print("So far we know:")
        print("Missing letters:")
        print(all_missing_letters)
        print("Letters that are present but in the wrong positions:")
        print(all_wrong_pos_letters)
        print("Letters that are present and in the correct positions:")
        print(all_correct_pos_letters)

        print("")
        print("Current number of candidates: {}".format(len(candidates)))
        print("Maybe try one of these words next:")

        guesses = select_guesses(candidates)
        print(", ".join(guesses))

        print("")
        input_type_choice = pyip.inputMenu(
            [
                "Input grey letters",
                "Input yellow letters",
                "Input green letters",
                "Quit",
            ],
            numbered=True,
        )

        # Missing letters entry
        if input_type_choice == "Input grey letters":
            print("Enter grey (missing) letters:")
            print("(e.g. enter 'aghz' to say that a, g, h, z are missing letters)")
            missing_letters = pyip.inputStr("")
            # Process missing letters
            for letter in missing_letters.lower():
                all_missing_letters.append(letter)
                candidates = candidates.intersection(letter_missing_indices[letter])

        # Wrong-position letters entry
        elif input_type_choice == "Input yellow letters":
            print("Enter yellow (present but wrong position) letters:")
            print(
                "(e.g. enter 't1g3' to say that t is not in slot 1 and g is not in slot 3, like in the word 'gamut')"
            )
            wrong_position_letters = pyip.inputStr("")
            pairs = chunkstring(wrong_position_letters, 2)
            for pair in pairs:
                all_wrong_pos_letters.append(pair)
                letter = pair[0]
                position = int(pair[1]) - 1
                candidates = candidates.intersection(
                    letter_position_indices[letter][False][position]
                )

        # Correct letters entry
        elif input_type_choice == "Input green letters":
            print("Enter green (correct) letters:")
            print(
                "(e.g. enter 't1g3' to say that t is in slot 1 and g is in slot 3, like the word 'tiger')"
            )
            correct_letters = pyip.inputStr("")
            pairs = chunkstring(correct_letters, 2)
            for pair in pairs:
                all_correct_pos_letters.append(pair)
                letter = pair[0]
                position = int(pair[1]) - 1
                candidates = candidates.intersection(
                    letter_position_indices[letter][True][position]
                )

        # Quit
        elif input_type_choice == "Quit":
            running = False
