import random


WORDS_BY_CATEGORY = {
    "animals": ["tiger", "eagle", "python", "wolf", "shark"],
    "technology": ["laptop", "server", "router", "database", "keyboard"],
    "space": ["planet", "galaxy", "nebula", "comet", "asteroid"],
    "cars": ["mustang", "skyline", "charger", "quattro", "viper"],
    "games": ["portal", "doom", "quake", "fallout", "diablo"],
}


def choose_secret_word():
    category = random.choice(list(WORDS_BY_CATEGORY.keys()))
    word = random.choice(WORDS_BY_CATEGORY[category])
    return category, word


def display_word(secret_word, guessed_letters):
    result = ""

    for letter in secret_word:
        if letter in guessed_letters:
            result += letter
        else:
            result += "-"

    return result


def get_player_guess(guessed_letters):
    while True:
        guess = input("Guess one letter: ").strip().lower()

        if len(guess) != 1:
            print("Please enter exactly one letter.")
        elif not guess.isalpha():
            print("Please enter a letter, not a number or symbol.")
        elif guess in guessed_letters:
            print("You already tried this letter.")
        else:
            return guess


def play_game():
    category, secret_word = choose_secret_word()
    guessed_letters = set()
    guesses_left = 10

    print("=== HANGMAN ===")
    print(f"Category: {category}")
    print(f"The secret word has {len(secret_word)} letters.")

    while guesses_left > 0:
        current_view = display_word(secret_word, guessed_letters)

        print()
        print(f"Word: {current_view}")
        print(f"Guesses left: {guesses_left}")
        print(f"Used letters: {' '.join(sorted(guessed_letters)) if guessed_letters else '-'}")

        if current_view == secret_word:
            print()
            print(f"You win! The secret word was: {secret_word}")
            return

        guess = get_player_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in secret_word:
            print("Good guess!")
        else:
            print("Wrong guess.")
            guesses_left -= 1

    print()
    print(f"You lose. The secret word was: {secret_word}")


if __name__ == "__main__":
    play_game()