from collections import defaultdict
import pyinputplus as pyip

from word_list import all_words


def chunkstring(string, length):
    return (string[0 + i : length + i] for i in range(0, len(string), length))


def count_unique_letters_in_string(string):
    return len(set(string))


def letter_points_for_word(word, letter_occurences):
    return sum([letter_occurences[letter] for letter in set(word)])


def filter_candidates(
    all_correct_pos_letters, all_wrong_pos_letters, all_missing_letters, index
):
    # Run the set logic to produce candidates
    candidates = index["five_letter_words"].copy()
    # Start with the correct position letters, which are the most option-limiting
    for pair in all_correct_pos_letters:
        letter = pair[0]
        position = int(pair[1])
        candidates = candidates.intersection(
            index["letter_position_indices"][letter][True][position]
        )
    for pair in all_wrong_pos_letters:
        letter = pair[0]
        position = int(pair[1])
        candidates = candidates.intersection(
            index["letter_position_indices"][letter][False][position]
        )
    for letter in all_missing_letters:
        candidates = candidates.intersection(index["letter_missing_indices"][letter])
    return candidates


def select_guesses(candidates, unknown_letters):

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


def generate_index():
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

    index = {}
    index["five_letter_words"] = five_letter_words
    index["letter_position_indices"] = letter_position_indices
    index["letter_missing_indices"] = letter_missing_indices
    return index


def process_response(
    input_word,
    response_colors,
    all_missing_letters,
    all_wrong_pos_letters,
    all_correct_pos_letters,
    unknown_letters,
):
    # Process missing letters
    missing_letters = [
        input_word[i] for i in range(0, len(input_word)) if response_colors[i] == "b"
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
        if response_colors[i] == "y"
    ]
    for pair in wrong_position_letters:
        all_wrong_pos_letters.append(pair)
        try:
            unknown_letters.remove(pair[0])
        except ValueError:
            pass

    # Correct letters entry
    right_position_letters = [
        (input_word[i], i)
        for i in range(0, len(input_word))
        if response_colors[i] == "g"
    ]
    for pair in right_position_letters:
        all_correct_pos_letters.append(pair)
        try:
            unknown_letters.remove(pair[0])
        except ValueError:
            pass

    return (
        all_missing_letters,
        all_wrong_pos_letters,
        all_correct_pos_letters,
        unknown_letters,
    )


if __name__ == "__main__":
    index = generate_index()

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

        candidates = filter_candidates(
            all_correct_pos_letters=all_correct_pos_letters,
            all_wrong_pos_letters=all_wrong_pos_letters,
            all_missing_letters=all_missing_letters,
            index=index,
        )

        print("")
        print("Current number of candidates: {}".format(len(candidates)))

        print("")
        guesses = select_guesses(candidates, unknown_letters)
        print("Maybe try one of these words next:")
        print(", ".join(guesses))

        print("")
        input_word = pyip.inputStr("Input the word you guessed: ", blank=False).lower()
        print(f"Input the colors that correspond to {input_word}")
        print("'b' for a black letter, 'y' for a yellow letter, 'g' for a green letter")
        print(
            "For example, if you played 'dogma' and got yellow-black-green-yellow-black, then enter 'ybgyb'"
        )
        response_colors = pyip.inputStr("Input colors: ", blank=False).lower()

        (
            all_missing_letters,
            all_wrong_pos_letters,
            all_correct_pos_letters,
            unknown_letters,
        ) = process_response(
            input_word,
            response_colors,
            all_missing_letters,
            all_wrong_pos_letters,
            all_correct_pos_letters,
            unknown_letters,
        )
