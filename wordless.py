from collections import defaultdict
import pyinputplus as pyip

from word_list import all_words


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
            if letter in unknown_letters:
                letter_occurrences[letter] += 1

    candidates_list = sorted(
        [
            (candidate, letter_points_for_word(candidate, letter_occurrences))
            for candidate in candidates
        ],
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        candidate for candidate, _ in candidates_list[: min(len(candidates_list), 10)]
    ]


def generate_indices():
    five_letter_words = {word.lower() for word in all_words}

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

        # Run the set logic to produce candidates
        candidates = five_letter_words.copy()
        # Start with the correct position letters, which are the most option-limiting
        for pair in all_correct_pos_letters:
            letter = pair[0]
            position = int(pair[1])
            candidates = candidates.intersection(
                letter_position_indices[letter][True][position]
            )
        for pair in all_wrong_pos_letters:
            letter = pair[0]
            position = int(pair[1])
            candidates = candidates.intersection(
                letter_position_indices[letter][False][position]
            )
        for letter in all_missing_letters:
            candidates = candidates.intersection(letter_missing_indices[letter])

        print("")
        print("Current number of candidates: {}".format(len(candidates)))

        print("")
        guesses = select_guesses(candidates, five_letter_words, unknown_letters)
        print("Maybe try one of these words next:")
        print(", ".join(guesses))

        print("")
        input_word = pyip.inputStr("Input the word you guessed: ", blank=False).lower()
        print(f"Input the colors that correspond to {input_word}")
        print("'b' for a black letter, 'y' for a yellow letter, 'g' for a green letter")
        input_colors = pyip.inputStr("Input colors: ", blank=False).lower()

        # Process missing letters
        missing_letters = [
            input_word[i] for i in range(0, len(input_word)) if input_colors[i] == "b"
        ]
        for letter in missing_letters:
            all_missing_letters.append(letter)
            try:
                unknown_letters.remove(letter)
            except ValueError:
                pass

        # Wrong-position letters entry
        wrong_position_letters = [
            (input_word[i], i)
            for i in range(0, len(input_word))
            if input_colors[i] == "y"
        ]
        for pair in wrong_position_letters:
            all_wrong_pos_letters.append(pair)
            try:
                unknown_letters.remove(letter)
            except ValueError:
                pass

        # Correct letters entry
        right_position_letters = [
            (input_word[i], i)
            for i in range(0, len(input_word))
            if input_colors[i] == "g"
        ]
        for pair in right_position_letters:
            all_correct_pos_letters.append(pair)
            try:
                unknown_letters.remove(letter)
            except ValueError:
                pass
