import statistics

from wordless import (
    generate_index,
    select_guesses,
    process_response,
    filter_candidates,
    get_yellow_letters,
)
from word_list import all_words


def generate_response(guess, word):
    # Generate the response
    response = ""
    for i in range(len(guess)):
        if guess[i] == word[i]:
            response += "g"
            continue
        elif guess[i] in word:
            response += "y"
            continue
        else:
            response += "b"
            continue
    return response


if __name__ == "__main__":

    index = generate_index()

    guess_counts = {}
    n_words = len(index["five_letter_words"])
    for k, word in enumerate(index["five_letter_words"]):

        game_state = {
            "all_missing_letters": [],
            "all_wrong_pos_letters": [],
            "all_correct_pos_letters": [],
            "unknown_letters": [letter for letter in "abcdefghijklmnopqrstuvwxyz"],
        }

        guessing = True
        guesses = 0
        guess_sequence = []
        while guessing:

            # Simulate guessing at this word
            candidates = filter_candidates(
                game_state=game_state,
                index=index,
            )
            guess = select_guesses(
                all_words=all_words,
                candidates=candidates,
                game_state=game_state,
                guess_number=guesses,
            )[0]

            response = generate_response(guess=guess, word=word)

            game_state = process_response(guess, response, game_state)

            # print("Guessed {} got response {}".format(guess, response))
            # print(game_state)

            guesses += 1
            guess_sequence.append(
                f"{guess}, {len(get_yellow_letters(game_state))}, {len(candidates)}"
            )
            if guess == word:
                guessing = False

        print(f"{k}/{n_words} Guessed {word} with {guesses} guesses: {guess_sequence}")
        guess_counts[word] = guesses
        if k >= 1000:
            break

    print(f"Mean: {statistics.mean(guess_counts.values())}")
    print(f"Stdev: {statistics.stdev(guess_counts.values())}")
    print(f"Max: {max(guess_counts.values())}")
    print(f"Failures: {sum([val > 5 for val in guess_counts.values()])}")
