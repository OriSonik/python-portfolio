# Design Decisions

## Table of Contents:
1. [Project Goal]
2. [Architecture]
3. [Key Design Decisions]
   3.1. [Named Constants Instead of Magic Values]
   3.2. [Random Sampling Instead of Generating a Random Integer]
   3.3. [String Representation Instead of Numeric Representation]
   3.4. [Dedicated Validation Instead of Inline Checks]
   3.5. [Returned Feedback Instead of Printing Inside the Logic]
   3.6. [Iteration with Enumerate Instead of Repeated Position Checks]
   3.7. [Position-aligned Feedback Instead of Aggregated Feedback]
   3.8. [A Bounded For Loop Instead of an Open-ended While Loop]
   3.9. [Functional Decomposition Instead of a Game Class]
   3.10. [Explicit Module Entry Point Instead of Automatic Execution]
4. [Testing Approach]
5. [Trade-offs]
6. [Possible Future Improvements]
7. [Summary]

---

## 1. Project Goal

The goal of this project is to build a small command-line implementation of a Mastermind-style code guessing game.

The project demonstrates:

- random code generation;

- input validation;

- sequence comparison;

- state management;

- bounded game flow;

- separation of logic and presentation;

- deliberate use of Python data structures;

- readable terminal output.

The final implementation is the result of an evolutionary design process. Earlier approaches offered simpler solutions, intermediate approaches improved structure and validation, and the current architecture was chosen deliberately because it provides the best balance of clarity, testability, and proportional complexity.

The project intentionally remains dependency-free and focused on one complete game session.

---

## 2. Architecture

The application is divided into the following components:

- `generate_secret_code()` — creates the hidden code;

- `is_valid_guess()` — validates player input;

- `build_feedback()` — compares the guess with the secret code;

- `format_code_row()` — formats terminal output;

- `print_rules()` — displays the game instructions;

- `get_player_guess()` — repeatedly requests input until it is valid;

- `play_game()` — coordinates the complete game flow.

The main configuration values are stored as module-level constants:

```python

CODE_LENGTH = 4

MAX_ATTEMPTS = 8

SYMBOLS = "123456"
```

The application starts through:

```python
if __name__ == "__main__":

    play_game()
```

This structure separates configuration, logic, input handling, presentation, and execution.

---

## 3. Key Design Decisions

### 3.1. Named Constants Instead of Magic Values

The project uses named constants for:

code length;

maximum number of attempts;

available symbols.

An alternative approach would place values such as 4, 8, and "123456" directly inside multiple functions.

Named constants were selected because they give meaning to configuration values and prevent the same information from being duplicated across the program.

This approach provides:

one location for configuration changes;

more readable conditions and loops;

lower risk of inconsistent values;

easier future modification;

clearer explanation of the game rules.

For example:

for attempt in range(1, MAX_ATTEMPTS + 1):

is more expressive than:

for attempt in range(1, 9):

A separate configuration object or file could become useful if the game later supported multiple difficulty levels or user-defined settings.

For the current scope, module-level constants are the clearest solution.

### 3.2. Random Sampling Instead of Generating a Random Integer

The secret code is generated with:

random.sample(SYMBOLS, CODE_LENGTH)

An alternative approach would generate a random integer within a selected numeric range.

Random sampling was selected because the code is not treated as a mathematical value. It is a sequence of symbols that must satisfy specific rules:

exact length;

symbols limited to the allowed set;

no duplicate symbols.

Using random.sample() guarantees these conditions during generation.

This solution provides:

exactly four symbols;

no repeated symbols;

no accidental out-of-range value;

no need for additional correction logic;

direct control over the available symbol set.

Generating an integer would require additional validation and could introduce unwanted values, leading zeros, repeated digits, or an incorrect number of characters.

A different generator would become necessary if future rules allowed repeated symbols. In that case, random.choices() or another controlled generation method could be used.

### 3.3. String Representation Instead of Numeric Representation

Both the secret code and the player guess are stored as strings.

An alternative approach would convert them to integers or lists of integers.

String representation was selected because the program performs positional and membership comparisons rather than mathematical operations.

The code is never added, multiplied, or evaluated as a number. Each character represents one independent symbol.

This approach provides:

direct access by index;

simple length validation;

easy membership checks;

no unnecessary conversion;

preservation of possible leading symbols;

consistent representation for both the secret code and player input.

A list could become useful if individual symbols needed to store additional properties.

An integer would be appropriate only if the code had mathematical meaning, which it does not in this project.

### 3.4. Dedicated Validation Instead of Inline Checks

Player guesses are validated by:

is_valid_guess()

The function checks:

exact code length;

allowed symbols;

absence of duplicates.

An alternative approach would place all validation conditions directly inside get_player_guess() or play_game().

A dedicated validation function was selected because validation is a separate responsibility from input collection and game coordination.

This solution provides:

one clear location for validation rules;

simpler input-handling code;

easier unit testing;

reusable validation logic;

lower risk of inconsistent checks;

easier extension of the rules.

The function returns a boolean value instead of printing messages or changing game state.

This makes it independent from the terminal interface.

A more advanced validator could later return detailed error information, for example:

invalid length;

unsupported symbol;

repeated symbol.

For the current version, a boolean result is sufficient and keeps the function simple.

### 3.5. Returned Feedback Instead of Printing Inside the Logic

The build_feedback() function returns a feedback string.

It does not print the result directly.

An alternative approach would produce terminal output while comparing the symbols.

Returning the feedback was selected because game logic should generate data, while the presentation layer should decide how that data is displayed.

This approach provides:

easier unit testing;

separation of logic and terminal output;

reuse in another interface;

predictable function behaviour;

simpler future formatting changes;

no hidden side effects.

For example, the same feedback could later be displayed through:

a graphical interface;

a web application;

a different terminal layout;

an automated test.

Printing inside the comparison logic would tie the function directly to the command-line interface.

Returning data keeps the function reusable.

### 3.6. Iteration with Enumerate Instead of Repeated Position Checks

The feedback function iterates through the player guess using:

for index, guessed_symbol in enumerate(player_guess):

An alternative approach would manually check positions 0, 1, 2, and 3 one by one.

Iteration was selected because the comparison rule is identical for every position.

This approach provides:

no repeated comparison code;

support for changing CODE_LENGTH;

lower risk of copy-and-paste errors;

clearer intent;

easier maintenance;

direct access to both index and symbol.

Manual position checks would work for a fixed four-symbol code, but they would make the implementation longer and tightly coupled to the current code length.

Using enumerate() allows the same logic to work for any supported length.

### 3.7. Position-aligned Feedback Instead of Aggregated Feedback

The feedback string is built in the same order as the player's guess.

Each guessed symbol receives one result:

+ — correct symbol in the correct position;

x — correct symbol in the wrong position;

- — symbol not present in the code.

An alternative approach would return only aggregated information, such as the total number of correct positions and misplaced symbols.

Position-aligned feedback was selected because it is easy to understand in a command-line application and creates a direct visual relationship between the guess and its result.

This approach provides:

clear terminal presentation;

immediate understanding of each position;

simple feedback generation;

no need for a separate feedback object;

easier manual verification.

The trade-off is that position-aligned feedback gives the player more detailed information and makes the game easier.

Aggregated feedback would create a more traditional and difficult puzzle, but it would also require a more complex comparison algorithm, especially if repeated symbols were introduced.

For the current educational CLI version, clarity was prioritized over maximum difficulty.

### 3.8. A Bounded For Loop Instead of an Open-ended While Loop

The application uses:

for attempt in range(1, MAX_ATTEMPTS + 1):

An alternative approach would use an open-ended while loop and manually increment an attempt counter.

The bounded for loop was selected because the number of attempts is known before the game begins.

This solution provides:

automatic attempt counting;

a clearly defined stopping point;

no manual counter update;

lower risk of an infinite loop;

readable display of the current attempt;

direct connection to MAX_ATTEMPTS.

A while loop would become more appropriate if the number of attempts depended on changing conditions, player decisions, difficulty modifiers, or game events.

For a fixed limit, the for loop expresses the rule more directly.

### 3.9. Functional Decomposition Instead of a Game Class

The application uses small functions rather than a MastermindGame class.

A class could store:

the secret code;

the current attempt;

the maximum number of attempts;

configuration values;

game status.

However, the current application represents one short session with limited mutable state.

Functional decomposition was selected because:

each function has one clear responsibility;

most logic can be expressed as independent operations;

the control flow remains easy to follow;

functions can be tested separately;

dependencies are visible through arguments;

the project avoids unnecessary boilerplate.

A class would become more appropriate if the application later introduced:

multiple rounds;

persistent scores;

several players;

difficulty objects;

saved sessions;

game history;

graphical state;

configurable game modes.

For the current scope, functions provide the best balance between structure and simplicity.

### 3.10. Explicit Module Entry Point Instead of Automatic Execution

The application uses:

if __name__ == "__main__":

    play_game()

An alternative approach would start the game immediately at module level.

The explicit entry point was selected because importing the file should not automatically start an interactive session.

This structure provides:

safe module imports;

easier automated testing;

reuse of functions by another interface;

clear separation between definitions and execution;

better compatibility with future package structure.

The same logic could later be imported by a GUI or web interface without launching the terminal version.

---

## 4. Testing Approach

The current version was tested manually for:

successful game startup;

hidden code generation;

valid guesses;

incorrect code length;

unsupported symbols;

repeated symbols;

correct-position feedback;

wrong-position feedback;

absent-symbol feedback;

win condition;

loss condition;

maximum-attempt handling.

The architecture was designed to support automated testing.

The first candidates for unit tests are:

is_valid_guess();

build_feedback();

format_code_row();

generate_secret_code();

win and loss conditions;

attempt-limit handling.

is_valid_guess(), build_feedback(), and format_code_row() are especially suitable for unit testing because they return values and do not depend directly on interactive input.

Random generation can be tested by checking its properties:

correct length;

allowed symbols;

unique symbols.

Interactive input can later be tested using mocked input().

---

## 5. Trade-offs

The project intentionally prioritizes:

readable rules over maximum puzzle difficulty;

unique symbols over duplicate-symbol handling;

direct position-aligned feedback over aggregated feedback;

built-in configuration over external settings;

functions over object-oriented structure;

terminal simplicity over visual complexity;

no external dependencies over additional libraries.

The decision to forbid repeated symbols significantly simplifies feedback generation.

If duplicate symbols were allowed, the algorithm would need to count symbol occurrences carefully to avoid assigning the same secret symbol to multiple guessed positions.

The position-aligned feedback is easy to understand, but it gives more information than an aggregated result.

These choices are appropriate for the current educational and portfolio scope, but they are not universal rules for every Mastermind implementation.

---

## 6. Possible Future Improvements

Possible extensions include:

automated tests with pytest;

aggregated Mastermind-style feedback;

optional repeated symbols;

difficulty levels;

configurable code length;

configurable symbol sets;

multiple rounds;

scoring system;

player statistics;

two-player mode;

game history;

hints;

colour-based graphical interface;

persistent configuration;

saved game sessions.

If the project grows in these directions, introducing a MastermindGame class or a dedicated state object would become justified.

A separate feedback model could also be introduced if the application needed to return counts, symbol positions, and presentation metadata independently.

---

## 7. Summary

The current implementation uses named constants, controlled random sampling, consistent string representation, dedicated validation, returned feedback, bounded iteration, and small focused functions.

Each solution was selected after considering simpler or more complex alternatives.

The final architecture avoids unnecessary abstraction while still separating responsibilities clearly.

It remains:

readable;

portable;

testable;

easy to explain;

proportionate to the project size;

prepared for future extension.

The project demonstrates that good design does not always require the most complex solution.

The strongest solution is the one that solves the current problem clearly while leaving a sensible path for future development.
