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


def select_guesses(candidates, five_letter_words, unknown_letters):

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

    reduction_occurrences = defaultdict(int)
    for letter in unknown_letters:
        reduction_occurrences[letter] = letter_occurrences[letter]
    reductions_list = sorted(
        [
            (candidate, letter_points_for_word(candidate, reduction_occurrences))
            for candidate in five_letter_words
        ],
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        candidate for candidate, _ in candidates_list[: min(len(candidates_list), 10)]
    ], [candidate for candidate, _ in reductions_list[: min(len(reductions_list), 10)]]


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
    unknown_letters = [letter for letter in "abcdefghijklmnopqrstuvwxyz"]

    print("")
    print(
        "Welcome to Wordless! The #1 app in the world for helping you cheat at Wordle."
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
        print("Unknown letters:")
        print(unknown_letters)

        print("")
        print("Current number of candidates: {}".format(len(candidates)))

        guesses, reductions = select_guesses(
            candidates, five_letter_words, unknown_letters
        )
        print("Maybe try one of these words next:")
        print(", ".join(guesses))
        print("Or one of these words to reduce the number of candidates:")
        print(", ".join(reductions))

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
                try:
                    unknown_letters.remove(letter)
                except ValueError:
                    pass

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
                try:
                    unknown_letters.remove(letter)
                except ValueError:
                    pass

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
                try:
                    unknown_letters.remove(letter)
                except ValueError:
                    pass

        # Quit
        elif input_type_choice == "Quit":
            running = False
