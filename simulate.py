import statistics

from wordless import generate_index, select_guesses, process_response, filter_candidates
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

        all_correct_pos_letters = []
        all_wrong_pos_letters = []
        all_missing_letters = []
        unknown_letters = [letter for letter in "abcdefghijklmnopqrstuvwxyz"]

        guessing = True
        guesses = 0
        guess_sequence = []
        while guessing:

            # Simulate guessing at this word
            candidates = filter_candidates(
                all_correct_pos_letters=all_correct_pos_letters,
                all_wrong_pos_letters=all_wrong_pos_letters,
                all_missing_letters=all_missing_letters,
                index=index,
            )
            guess = select_guesses(
                candidates=candidates, unknown_letters=unknown_letters
            )[0]

            response = generate_response(guess=guess, word=word)

            (
                all_missing_letters,
                all_wrong_pos_letters,
                all_correct_pos_letters,
                unknown_letters,
            ) = process_response(
                guess,
                response,
                all_missing_letters,
                all_wrong_pos_letters,
                all_correct_pos_letters,
                unknown_letters,
            )

            guesses += 1
            guess_sequence.append(guess)
            if guess == word:
                guessing = False

        print(f"{k}/{n_words} Guessed {word} with {guesses} guesses: {guess_sequence}")
        guess_counts[word] = guesses

    print(f"Mean: {statistics.mean(guess_counts.values())}")
    print(f"Stdev: {statistics.stdev(guess_counts.values())}")
    print(f"Min: {min(guess_counts.values())}")
    print(f"Max: {max(guess_counts.values())}")
