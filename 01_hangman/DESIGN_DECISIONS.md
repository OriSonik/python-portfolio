# Design Decisions

---

## Table of Contents:

1. [Project Goal]
2. [Architecture]
3. [Key Design Decisions]
   3.1. [Functional Decomposition Instead of a Game Class]
   3.2. [Derived Word Display Instead of Separately Maintained Mutable State]
   3.3. [A Set for Guessed Letters Instead of a List]
   3.4. [Built-in Word Categories Instead of an External Data File]
   3.5. [Dedicated Input Validation Instead of Validation Inside the Main Game Loop]
   3.6. [Explicit Game State Instead of Hidden Global Mutable State]
   3.7. [A Direct Loop Condition Instead of Indirect End-state Handling]
   3.8. [Explicit Module Entry Point Instead of Automatic Execution on Import]
4. [Testing Approach]
5. [Trade-offs]
6. [Possible Future Improvements]
7. [Summary]

---

## 1. Project goal

The goal of this project is to build a small, readable command-line Hangman game that demonstrates:
- control flow;
- input validation;
- state management;
- appropriate use of Python data structures;
- separation of responsibilities;
- random word selection;
- clear terminal interaction.

The project intentionally remains small and dependency-free. Its architecture is designed to match the current scope without introducing unnecessary abstraction.

---

## 2. Architecture

The application is divided into four main functions:
- `choose_secret_word()` — selects a random category and word;
- `display_word()` — builds the currently visible form of the secret word;
- `get_player_guess()` — validates and returns player input;
- `play_game()` — coordinates the complete game flow.

The word database is stored in the `WORDS_BY_CATEGORY` constant.

The application is started through:
if __name__ == "__main__":
    play_game()


This prevents the game from starting automatically when the module is imported.

---

## 3. Key design decisions


### 3.1 Functional decomposition instead of a game class

The application uses several small functions instead of a HangmanGame class.

A class-based approach could store values such as:
the secret word;
guessed letters;
remaining guesses;
the selected category.

However, the current application represents one short game session with a limited amount of state. Introducing a class would add more structure, but it would not yet solve a significant design problem.

Functional decomposition was selected because:
each function has one clear responsibility;
the game flow remains easy to follow;
functions can be tested independently;
dependencies are visible through function arguments;
the amount of boilerplate remains small;
the architecture matches the actual scale of the project.

A class would become more appropriate if the application later introduced:
multiple rounds;
persistent scores;
difficulty levels;
save and load functionality;
several players;
a graphical interface;
configurable game modes;
session statistics.

For the current scope, functions provide the clearest and most proportionate solution.


### 3.2 Derived word display instead of separately maintained mutable state

The visible form of the word is generated from:
secret_word;
guessed_letters.

The display_word() function rebuilds the displayed word whenever it is needed.

An alternative approach would be to store the partially revealed word as a separate mutable string and update it after every correct guess.

The derived-state approach was selected because the displayed word is not an independent part of the game state. It is a result that can always be calculated from the secret word and the guessed letters.

This solution provides:
a single source of truth;
lower risk of synchronization errors;
simpler state management;
easier unit testing;
automatic handling of repeated letters;
clear separation between stored state and presentation.

A separately maintained word representation could become useful if every character position needed to store additional information that could not be derived from the guessed letters alone.

For the current game rules, deriving the display is simpler and safer.


### 3.3 A set for guessed letters instead of a list

Guessed letters are stored in a set.

A list could also store player guesses, but it would allow duplicate values and would require additional logic to preserve uniqueness.

A set was selected because:
every guessed letter should occur only once;
duplicate guesses are rejected naturally;
membership checks are straightforward;
the data structure directly represents a collection of unique values;
the order of guesses is not required by the current game logic.

When the letters are displayed to the player, they are sorted only for presentation:
sorted(guessed_letters)

This keeps the internal data structure optimized for the game rules while still producing readable terminal output.

A list could become useful if a future version needed to preserve:
the exact order of guesses;
timestamps;
complete attempt history;
statistics for each guess.

In that case, a list could be used alongside the set. The set would handle duplicate detection, while the list would store chronological history.


### 3.4 Built-in word categories instead of an external data file

The word database is stored directly in WORDS_BY_CATEGORY.

An alternative solution would load words from JSON, CSV, TXT, or another external source.

The built-in dictionary was selected because the current word database is small and the project should run immediately after cloning the repository.

This approach provides:
a self-contained application;
no dependency on additional files;
no risk of a missing or incorrectly located data file;
immediate access to category information;
simpler setup for a recruiter or reviewer;
predictable behaviour regardless of the current working directory.

An external data source would become the better solution if:
the word database became significantly larger;
users could create custom word packs;
categories were updated independently from the code;
the application supported multiple languages;
words were downloaded from an API or database.

A future version could move the word data to JSON and use pathlib for reliable path handling.

For the current scope, the embedded dictionary provides better portability and lower complexity.


### 3.5 Dedicated input validation instead of validation inside the main game loop

Player input is handled by get_player_guess().

The function normalizes the input and verifies that:
exactly one character was entered;
the character is a letter;
the letter has not already been used.

An alternative approach would perform these checks directly inside play_game().

A dedicated validation function was selected because:
the main game loop remains focused on game flow;
validation rules are located in one place;
invalid input does not affect the game state;
repeated guesses do not reduce the number of remaining attempts;
input behaviour can be changed without modifying the main loop;
the function can later be tested separately.

The input is normalized using:
.strip().lower()

This prevents surrounding spaces or uppercase letters from being treated as different guesses.

A more advanced validation layer would become useful if the application later supported:
complete-word guesses;
accented characters;
multiple alphabets;
command input such as quit or hint;
graphical or web-based input.

For the current CLI version, a dedicated function provides clear and sufficient validation.


### 3.6 Explicit game state instead of hidden global mutable state

The current game state is created inside play_game():
secret_word;
guessed_letters;
guesses_left.

These values are passed to other functions when needed.

The alternative would be to store the current game state in global variables.

Local state was selected because:
functions clearly show which data they depend on;
one game session does not unexpectedly affect another;
the module is easier to import safely;
tests can provide their own input values;
state changes remain limited to the game coordinator.

The global WORDS_BY_CATEGORY value is treated as configuration data rather than mutable game state.

A separate state object could become useful when the application grows, but global mutable variables would still be avoided because they create hidden dependencies.


### 3.7 A direct loop condition instead of indirect end-state handling

The game continues while:
guesses_left > 0

The player wins when the displayed word matches the secret word. The player loses when no guesses remain.

This direct condition was selected because it maps clearly to the game rules.

Its advantages are:
no additional attempt is available at zero guesses;
the condition is easy to read;
the loss state is unambiguous;
the risk of an off-by-one error is reduced;
the control flow remains simple.

A dedicated game-status value or enumeration could become useful if the application later introduced states such as:
paused;
abandoned;
saved;
timed out;
completed across several rounds.

For the current game, explicit conditions are clearer than introducing a separate status system.


### 3.8 Explicit module entry point instead of automatic execution on import

The application uses:
if __name__ == "__main__":
    play_game()

Without this condition, importing the module would immediately start the interactive game.

The explicit entry point was selected because:
functions can be imported without launching the application;
automated tests can import the module safely;
the code can later be reused by another interface;
the file clearly distinguishes definitions from execution.

This structure also prepares the project for a possible future GUI or web interface that could reuse the same game logic.

---

## 4. Testing approach

The current version has been tested manually for:
successful application startup;
valid letter input;
invalid multi-character input;
numbers and symbols;
repeated letters;
correct guesses;
incorrect guesses;
words containing repeated letters;
win condition;
loss condition.

Manual testing is sufficient for confirming the basic CLI flow, but automated tests would provide better regression protection.

The first candidates for unit testing are:
display_word();
choose_secret_word();
input validation with mocked input();
win and loss conditions;
repeated-guess handling.

The architecture already separates these responsibilities, which makes future test automation easier.

---

## 5. Trade-offs

The project intentionally prioritizes:
readability over abstraction;
portability over a large external word database;
simple functions over object-oriented structure;
direct control flow over a more advanced state machine;
a small dependency-free application over additional libraries.

These choices are appropriate for the current project size.

They are not universal rules. A larger application would require different decisions, particularly around data storage, state management, automated testing, and user interfaces.

---

## 6. Possible future improvements

Possible extensions include:
automated unit tests with pytest;
configurable difficulty levels;
difficulty based on word length;
external JSON word packs;
support for custom categories;
complete-word guessing;
score tracking;
multiple rounds;
saving game statistics;
ASCII hangman animation;
graphical user interface;
multilingual word databases.

If the project grows in these directions, introducing a HangmanGame class or a dedicated state object would become justified.

---

## 7. Summary

The project uses a deliberately simple architecture based on small functions, local state, derived presentation data, and Python data structures selected according to the game rules.

Alternative solutions such as a game class, an external word database, a mutable displayed-word state, or a more advanced state machine were considered.

They were not selected because they would add complexity without providing enough value at the current scale.

The chosen design keeps the application readable, portable, testable, and easy to extend when new requirements appear.
