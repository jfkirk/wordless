from collections import defaultdict
from statistics import mean
import pyinputplus as pyip

from word_list import all_words


def chunkstring(string, length):
    return (string[0 + i : length + i] for i in range(0, len(string), length))


def count_unique_letters_in_string(string):
    return len(set(string))


def calculate_letter_occurrences(game_state, candidates):
    yellow_letters = get_yellow_letters(game_state)
    green_letters = get_green_letters(game_state)
    letter_occurrences = defaultdict(float)
    for word in candidates:
        for letter in set(word):
            # We want to sort primarily on content of unknown letters and
            # secondarily on the number of letters we already know about
            if letter in game_state["unknown_letters"]:
                letter_occurrences[letter] += 1000000
            if letter in yellow_letters:
                letter_occurrences[letter] += 10
            if letter in green_letters:
                letter_occurrences[letter] += 1
    return letter_occurrences


def letter_points_for_word(word, letter_occurrences):
    return sum([letter_occurrences[letter] for letter in set(word)])


def filter_candidates(game_state, index):
    # Run the set logic to produce candidates
    candidates = index["five_letter_words"].copy()
    # Start with the correct position letters, which are the most option-limiting
    for pair in game_state["all_correct_pos_letters"]:
        letter = pair[0]
        position = int(pair[1])
        candidates = candidates.intersection(
            index["letter_position_indices"][letter][True][position]
        )
    for pair in game_state["all_wrong_pos_letters"]:
        letter = pair[0]
        position = int(pair[1])
        candidates = candidates.intersection(
            index["letter_position_indices"][letter][False][position]
        )
    for letter in game_state["all_missing_letters"]:
        candidates = candidates.intersection(index["letter_missing_indices"][letter])
    return candidates


def get_yellow_letters(game_state):
    found_letters = set()
    for pair in game_state["all_wrong_pos_letters"]:
        found_letters.add(pair[0])
    for pair in game_state["all_correct_pos_letters"]:
        try:
            found_letters.remove(pair[0])
        except KeyError:
            pass
    return found_letters


def get_green_letters(game_state):
    return {pair[0] for pair in game_state["all_correct_pos_letters"]}


def select_guesses(candidates, game_state, index):

    letter_occurrences = calculate_letter_occurrences(
        game_state=game_state, candidates=candidates
    )

    # As long as we're guessing, we have at least 1 guess left by definition
    guess_number = len(game_state["guessed_words"])
    remaining_guesses = max(1, 6 - guess_number)
    # Once we're narrowing in, only pick from actual candidates
    set_to_select_from = index["five_letter_words"].copy()
    if (len(candidates) <= remaining_guesses) or (remaining_guesses == 1):
        set_to_select_from = candidates

    # Pop out already-guessed words to prevent loops when using all_words
    for word in game_state["guessed_words"]:
        try:
            set_to_select_from.remove(word)
        except KeyError:
            pass
        except ValueError:
            pass

    candidates_list = sorted(
        [
            (
                candidate,
                letter_points_for_word(candidate, letter_occurrences),
            )
            for candidate in set_to_select_from
        ],
        key=lambda x: x[1],
        reverse=True,
    )

    # print(candidates_list[:10])

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


def process_response(input_word, response_colors, game_state):

    # Add the word we guessed
    game_state["guessed_words"].append(input_word)

    # Process missing letters
    missing_letters = [
        input_word[i] for i in range(0, len(input_word)) if response_colors[i] == "b"
    ]
    for letter in missing_letters:
        if letter not in game_state["all_missing_letters"]:
            game_state["all_missing_letters"].append(letter)
        try:
            game_state["unknown_letters"].remove(letter)
        except ValueError:
            pass

    # Wrong-position letters entry
    wrong_position_letters = [
        (input_word[i], i)
        for i in range(0, len(input_word))
        if response_colors[i] == "y"
    ]
    for pair in wrong_position_letters:
        if pair not in game_state["all_wrong_pos_letters"]:
            game_state["all_wrong_pos_letters"].append(pair)
        try:
            game_state["unknown_letters"].remove(pair[0])
        except ValueError:
            pass

    # Correct letters entry
    right_position_letters = [
        (input_word[i], i)
        for i in range(0, len(input_word))
        if response_colors[i] == "g"
    ]
    for pair in right_position_letters:
        if pair not in game_state["all_correct_pos_letters"]:
            game_state["all_correct_pos_letters"].append(pair)
        try:
            game_state["unknown_letters"].remove(pair[0])
        except ValueError:
            pass

    return game_state


if __name__ == "__main__":
    index = generate_index()

    game_state = {
        "all_missing_letters": [],
        "all_wrong_pos_letters": [],
        "all_correct_pos_letters": [],
        "unknown_letters": [letter for letter in "abcdefghijklmnopqrstuvwxyz"],
        "guessed_words": [],
    }

    print("")
    print(
        "Welcome to Wordless! The #1 app in the world for helping you cheat at Wordle."
    )

    running = True
    while running:

        print("")
        print("So far we know:")
        print("Guessed words:")
        print(game_state["guessed_words"])
        print("Missing letters:")
        print(game_state["all_missing_letters"])
        print("Letters that are present but in the wrong positions:")
        print(game_state["all_wrong_pos_letters"])
        print("Letters that are present and in the correct positions:")
        print(game_state["all_correct_pos_letters"])
        print("Unknown letters:")
        print(game_state["unknown_letters"])

        candidates = filter_candidates(
            game_state=game_state,
            index=index,
        )

        print("")
        print("Current number of candidates: {}".format(len(candidates)))

        print("")
        guesses = select_guesses(
            candidates=candidates,
            game_state=game_state,
            index=index,
        )
        print("Maybe try one of these words next:")
        print(", ".join(guesses))

        print("")
        print(
            "Input the word you guessed (Guess #{}): ".format(
                len(game_state["guessed_words"]) + 1
            )
        )
        print("Or type 'exit' to quit.")
        input_word = pyip.inputStr(
            "",
            blank=False,
        ).lower()
        if input_word == "exit":
            running = False
            break
        print(f"Input the colors that correspond to {input_word}")
        print("'b' for a black letter, 'y' for a yellow letter, 'g' for a green letter")
        print(
            "For example, if you played 'dogma' and got yellow-black-green-yellow-black, then enter 'ybgyb'"
        )
        print("Or type 'exit' to quit.")
        response_colors = pyip.inputStr("Input colors: ", blank=False).lower()

        if response_colors == "exit":
            running = False
            break

        game_state = process_response(input_word, response_colors, game_state)
