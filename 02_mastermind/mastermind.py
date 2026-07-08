import random


CODE_LENGTH = 4
MAX_ATTEMPTS = 8
SYMBOLS = "123456"


def generate_secret_code():
    """Generate a secret code with unique symbols."""
    return "".join(random.sample(SYMBOLS, CODE_LENGTH))


def is_valid_guess(guess):
    """Check if the guess has the correct length, symbols and no duplicates."""
    return (
        len(guess) == CODE_LENGTH
        and all(symbol in SYMBOLS for symbol in guess)
        and len(set(guess)) == CODE_LENGTH
    )


def build_feedback(secret_code, player_guess):
    """Return feedback for the player's guess.

    + means correct symbol in the correct position
    x means correct symbol in the wrong position
    - means symbol is not present in the code
    """
    feedback = ""

    for index, guessed_symbol in enumerate(player_guess):
        if guessed_symbol == secret_code[index]:
            feedback += "+"
        elif guessed_symbol in secret_code:
            feedback += "x"
        else:
            feedback += "-"

    return feedback


def format_code_row(label, code):
    """Format a code or guess as a simple terminal row."""
    boxes = " ".join(f"[ {symbol} ]" for symbol in code)
    return f"{label:<10}{boxes}"


def print_rules():
    print("=== MASTERMIND ===")
    print()
    print("Guess the hidden 4-symbol code.")
    print("Available symbols: 1 2 3 4 5 6")
    print("Each symbol appears only once.")
    print()
    print("Feedback:")
    print("+  correct symbol in the correct position")
    print("x  correct symbol in the wrong position")
    print("-  symbol not present in the code")
    print()


def get_player_guess():
    while True:
        guess = input("Enter your guess: ").strip()

        if is_valid_guess(guess):
            return guess

        print("Invalid guess. Use 4 different digits from 1 to 6.")
        print()


def play_game():
    secret_code = generate_secret_code()

    print_rules()
    print(format_code_row("Code:", "?" * CODE_LENGTH))
    print()

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"Attempt {attempt}/{MAX_ATTEMPTS}")

        player_guess = get_player_guess()
        feedback = build_feedback(secret_code, player_guess)

        print(format_code_row("Guess:", player_guess))
        print(format_code_row("Feedback:", feedback))
        print()

        if player_guess == secret_code:
            print(f"You win! The secret code was: {secret_code}")
            return

    print(f"You lose. The secret code was: {secret_code}")


if __name__ == "__main__":
    play_game()