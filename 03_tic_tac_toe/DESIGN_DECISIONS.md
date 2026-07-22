# Design Decisions

## Table of Contents:
1. [Project Goal]
2. [Architecture]
3. [Key Design Decisions]
   3.1. [A Game Class Instead of Global Mutable State]
   3.2. [A Flat Board Representation Instead of a Two-dimensional Structure]
   3.3. [Winning Patterns Stored as Data Instead of Repeated Conditions]
   3.4. [Calculated Coordinate Parsing Instead of Enumerating Every Valid Input]
   3.5. [Separate Parsing, Validation and Move Application]
   3.6. [A Single Source of Truth for Available Moves]
   3.7. [Game Methods Returning Results Instead of Controlling the Menu]
   3.8. [An Iterative Menu Instead of Recursive Control Flow]
   3.9. [One Shared AI Game Loop Instead of Duplicated Game Modes]
   3.10. [A Priority-based Heuristic AI Instead of Full Minimax]
   3.11. [Temporary Move Simulation Instead of Hard-coded Tactical Scenarios]
   3.12. [Match Mode Built on Reusable Single-game Results]
   3.13. [Parametrized Automated Tests Instead of Manual Verification Only]
   3.14. [An Explicit Module Entry Point Instead of Automatic Execution]
4. [Testing Approach]
5. [Trade-offs]
6. [Possible Future Improvements]
7. [Summary]

---

## 1. Project Goal

The goal of this project is to build a command-line Tic Tac Toe application that demonstrates more than the basic rules of the game.

The project includes:
- two-player mode;
- player versus random computer mode;
- player versus smart computer mode;
- Wimbledon mode, where the first side to win three games wins the match;
- coordinate-based player input;
- win and draw detection;
- reusable game logic;
- automated tests for the core behaviour.

The final implementation is the result of an evolutionary design process. Earlier approaches offered simpler solutions, intermediate approaches improved modularity and validation, and the current architecture was chosen deliberately because it provides the best balance of clarity, testability, reuse and proportional complexity.

The project is intentionally implemented without external runtime dependencies. Its main purpose is to demonstrate Python fundamentals, object-oriented state management, simple artificial intelligence and automated verification.

---

## 2. Architecture

The application is built around the `TicTacToeGame` class.

The class stores the current board state and provides methods responsible for:
- resetting and rendering the board;
- parsing player coordinates;
- validating and applying moves;
- finding available fields;
- detecting winners and draws;
- handling human input;
- selecting random computer moves;
- selecting tactical computer moves;
- running individual game modes;
- running the Wimbledon match mode;
- displaying rules;
- controlling the main menu.

The main class-level constants are:
ROWS = "ABC"
COLUMNS = "123"
                               and:
WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

The board itself is stored as a flat list containing nine fields:
self.board = [" " for _ in range(9)]

The application starts through:
if __name__ == "__main__":
    game = TicTacToeGame()
    game.run_menu()

This structure keeps the current game state inside one object and allows the same rules to be reused by several game modes.

---

## 3. Key Design Decisions


### 3.1. A Game Class Instead of Global Mutable State

The current board is stored inside an instance of TicTacToeGame.

An alternative approach would store the board, scores, turn counter and current player in global variables accessed by multiple functions.

A class was selected because the project contains several closely related behaviours operating on the same game state.

This approach provides:
one clear owner of the board state;
no dependency on mutable global variables;
easier creation of a fresh game instance;
safer reuse between different modes;
methods that clearly belong to the game domain;
easier test setup;
better preparation for future extension.

For example, every test can create an independent game through:
game = TicTacToeGame()

without resetting global state left by another test.

A purely functional approach would still be possible if the board were passed explicitly to every function.

That solution could work well for a smaller version containing only one game mode. Once the application includes several modes, artificial intelligence and a multi-round match, the class provides a more coherent place for the shared state and behaviour.


### 3.2. A Flat Board Representation Instead of a Two-dimensional Structure

The board is represented as a list of nine fields:
[" ", " ", " ", " ", " ", " ", " ", " ", " "]

An alternative approach would use:
a nested three-by-three list;
a dictionary with positions from 1 to 9;
a list containing additional formatting elements;
separate variables for every field.

The flat list was selected because all important game operations work naturally with indexes from 0 to 8.

This approach provides:
simple storage;
direct index access;
easy iteration;
compact win-line definitions;
straightforward move availability checks;
simple temporary AI simulations;
no unnecessary nesting.

The visual row and column structure is calculated only when the board is rendered.

A nested list could make direct access such as board[row][column] more visually expressive. However, it would make the reusable winning-pattern representation and some iteration operations less compact.

For a fixed three-by-three board, the flat representation offers the clearest balance between display needs and game logic.


### 3.3. Winning Patterns Stored as Data Instead of Repeated Conditions

All possible winning combinations are stored in WIN_LINES.

An alternative approach would place all eight combinations directly inside one long conditional expression.

Representing winning lines as data was selected because every row, column and diagonal follows the same rule:
three indexed fields must contain the same non-empty marker.

This allows one algorithm to evaluate every winning combination:
for first, second, third in self.WIN_LINES:

This approach provides:
no repeated comparison logic;
easier visual verification of all winning combinations;
simpler maintenance;
lower risk of omitting a row, column or diagonal;
direct reuse in automated tests;
easier adaptation to different winning patterns.

The test suite can also iterate over the same WIN_LINES collection and verify every pattern for both X and O.

A longer conditional expression would work for a fixed board, but it would mix game data with control flow and make future changes more error-prone.


### 3.4. Calculated Coordinate Parsing Instead of Enumerating Every Valid Input

The player can enter coordinates in either order:
A1;
1A;
B2;
2B.

The parser normalizes the input and calculates the board index from the selected row and column.

An alternative approach would maintain a collection containing every allowed string and map each value to a field manually.

Calculated parsing was selected because the accepted inputs follow a predictable rule.

The row and column are converted into a flat-board index through:
row * 3 + column

This approach provides:
support for both coordinate orders;
case-insensitive input;
no long list of accepted combinations;
no repeated mapping logic;
easier modification of row and column labels;
a clear relationship between coordinates and board indexes.

A predefined dictionary could still be useful if fields had irregular names or if every coordinate required custom metadata.

For a regular three-by-three grid, calculation is simpler and less repetitive.


### 3.5. Separate Parsing, Validation and Move Application

Player movement is handled through separate responsibilities:
parse_move() converts text into a board index;
is_valid_move() checks whether the index refers to an available field;
make_move() applies the marker only when the move is valid.

An alternative approach would perform all three operations inside the interactive input loop.

The responsibilities were separated because they represent different questions:
Can the text be interpreted as a coordinate?
Does the coordinate point to an available field?
Should the board now be modified?

This approach provides:
focused methods;
easier unit testing;
no board mutation during text parsing;
reusable validation for human and computer moves;
clearer failure handling;
less complex interactive code.

The parser can return None for invalid syntax and "quit" for the quit command without modifying the board.

The move validator remains independent from the source of the move. It can check moves generated by a player, a random computer or a smart computer.


### 3.6. A Single Source of Truth for Available Moves

The available_moves() method returns every empty board index.

An alternative approach would search for empty fields independently inside each human-input or AI method.

A dedicated method was selected because several parts of the application need the same information:
random AI;
tactical AI;
draw detection;
corner selection;
side selection.

This approach provides:
one definition of an available field;
no duplicated board-scanning logic;
consistent behaviour across all game modes;
simpler AI functions;
easier testing;
easier future changes to the representation of an empty field.

The draw condition also uses this method:
return not self.available_moves() and self.check_winner() is None

This keeps the definition of a full board consistent throughout the application.


### 3.7. Game Methods Returning Results Instead of Controlling the Menu

Individual game modes return a result:
"X";
"O";
"draw";
None when the game is cancelled.

An alternative approach would make each game mode call the main menu directly after a game ends.

Returning the result was selected because a game method should report what happened rather than decide what the entire application should do next.

This approach provides:
no hidden navigation between unrelated methods;
reusable single-game logic;
simpler match-mode implementation;
easier testing;
clearer control flow;
no nested menu calls.

The Wimbledon mode can call a regular game and update its score from the returned result:
result = self.play_against_ai(smart_ai=True)

The menu remains the owner of top-level application navigation.

This separation prevents game methods from becoming tightly coupled to one specific interface flow.


### 3.8. An Iterative Menu Instead of Recursive Control Flow

The main menu is implemented with a continuous while loop.

An alternative approach would call run_menu() again from inside game modes, help screens or invalid-input branches.

The iterative approach was selected because returning to the menu is a repeated application state, not a new nested function call.

This approach provides:
stable stack depth;
predictable navigation;
no accumulation of unfinished menu calls;
clearer exit behaviour;
easier reasoning about the application lifecycle;
one location controlling application termination.

Recursive menu calls can appear to work in a small program, but every call leaves the previous menu invocation waiting on the call stack.

A loop represents repeated menu interaction more accurately and avoids unnecessary recursion.


### 3.9. One Shared AI Game Loop Instead of Duplicated Game Modes

Random and smart computer modes both use:
play_against_ai(smart_ai=False)

The smart_ai argument determines which move-selection strategy is used.

An alternative approach would create two separate game-loop methods containing almost identical code.

One shared loop was selected because the following rules are identical in both modes:
board reset;
player and computer markers;
turn switching;
move application;
winner detection;
draw detection;
final result handling.

Only the computer move selection changes.

This approach provides:
no duplicated game-loop logic;
consistent behaviour between AI modes;
easier bug fixing;
one place for future rule changes;
simpler maintenance;
clear identification of the actual variation.

A more advanced strategy pattern could become useful if the project later included many AI implementations.

For two strategies, a boolean parameter keeps the solution proportionate to the project size.


### 3.10. A Priority-based Heuristic AI Instead of Full Minimax

The smart computer follows a clear priority order:
take an immediate winning move;
block the opponent’s immediate winning move;
take the center;
select an available corner;
select an available side;
fall back to any remaining legal move.

An alternative approach would implement the Minimax algorithm and evaluate the full game tree.

The heuristic approach was selected because it demonstrates tactical decision-making while remaining readable and easy to explain.

This approach provides:
understandable AI behaviour;
immediate offensive decisions;
immediate defensive decisions;
strategic preference for high-value fields;
low computational and conceptual complexity;
straightforward automated testing.

Minimax would make the computer theoretically unbeatable when implemented correctly.

However, it would introduce recursion, game-tree evaluation and scoring logic that are not necessary to demonstrate the current project goals.

The heuristic AI offers a better balance between visible intelligence and proportional complexity.

Minimax remains a natural future extension.


### 3.11. Temporary Move Simulation Instead of Hard-coded Tactical Scenarios

The find_tactical_move() method tests every available field by temporarily placing a marker, checking for a winner and restoring the field.

An alternative approach would create separate conditions for every possible two-in-a-row configuration.

Temporary simulation was selected because the existing winner-detection logic can be reused for both real and hypothetical positions.

The process is:
choose an available field;
place the tested marker;
call check_winner();
restore the empty field;
return the move if it creates a win.

This approach provides:
reuse of the same winning rules;
no duplicate tactical conditions;
support for every row, column and diagonal;
compact AI logic;
easier testing;
automatic adaptation if WIN_LINES changes.

The method temporarily mutates the actual board, but it restores the field before continuing or returning.

For a larger or concurrent application, simulating moves on a copied board could provide stronger isolation.

For this single-threaded CLI game, temporary mutation is simple and efficient.


### 3.12. Match Mode Built on Reusable Single-game Results

Wimbledon mode does not reproduce the full Tic Tac Toe game loop.

Instead, it repeatedly calls the existing smart-AI game mode and updates the match score from the returned result.

An alternative approach would implement a separate large loop containing another copy of the board logic, move handling and winner detection.

Composition was selected because a match consists of repeated normal games plus score tracking.

This approach provides:
reuse of tested single-game logic;
no duplicated move rules;
consistent AI behaviour;
simple score management;
draws without awarded points;
clear separation between round rules and match rules.

The match continues while both scores remain below three:
while human_score < 3 and ai_score < 3:


This makes the match layer responsible only for:
displaying the score;
starting another game;
interpreting its result;
deciding the final match winner.


### 3.13. Parametrized Automated Tests Instead of Manual Verification Only

The project includes automated tests written with pytest.

An alternative approach would verify the application only by repeatedly playing it manually.

Automated testing was selected because the game contains several reusable rules that can be verified without terminal interaction.

The test suite covers:
both coordinate orders;
lowercase and uppercase coordinates;
quitting;
invalid input;
move placement;
rejection of occupied fields;
available-move detection;
every winning line for both markers;
draw detection;
tactical winning moves;
defensive blocking moves;
center selection by the smart AI.

Parametrization is used for repeated families of cases, including invalid inputs and every winning line.

This approach provides:
repeatable verification;
fast regression detection;
less duplicated test code;
documentation of expected behaviour;
confidence during refactoring;
proof that all winning configurations are handled consistently.

Full interactive flows and random branches are not yet covered completely.

They could later be tested with mocked input, captured output and controlled random choices.


### 3.14. An Explicit Module Entry Point Instead of Automatic Execution

The application uses:
if __name__ == "__main__":
    game = TicTacToeGame()
    game.run_menu()

An alternative approach would create the game and start the menu immediately at the module level.

The explicit entry point was selected because importing the module should not start an interactive application.

This approach provides:
safe imports in automated tests;
reuse of the class by another interface;
clear separation between definitions and execution;
easier future package structure;
predictable module behaviour.

A graphical interface, web interface or separate launcher could import TicTacToeGame without triggering the terminal menu.

---

## 4. Testing Approach

The current test suite focuses on deterministic core logic.

The tests verify:
conversion of coordinates into board indexes;
support for A1 and 1A formats;
case-insensitive input;
invalid coordinate rejection;
the quit command;
placing markers;
occupied-field protection;
available fields;
all rows, columns and diagonals;
both player markers;
draw detection;
tactical AI behaviour;
smart AI priority rules.

The test design uses fresh game instances to prevent state leakage:
game = TicTacToeGame()

Parametrization is used where the same behaviour must be checked against multiple inputs.

This is especially suitable for:
all winning lines;
both markers;
invalid move formats.

The tests currently concentrate on methods that return values or modify state predictably.

Future integration tests could additionally cover:
complete two-player games;
complete games against AI;
menu navigation;
quitting during a game;
Wimbledon score progression;
printed terminal output;
random corner and side selection.

Random behaviour could be tested by injecting or mocking the random-choice function.

---

## 5. Trade-offs

The project intentionally prioritizes:
a readable heuristic AI over a full Minimax implementation;
one cohesive class over several architectural layers;
a flat board over a visually nested representation;
direct terminal output over a separate renderer abstraction;
a boolean AI-mode selector over a full strategy hierarchy;
temporary board simulation over copying the board for every tested move;
straightforward strings such as "X", "O" and "draw" over enums or result objects.

These choices keep the application readable and proportionate to its size.

The current class contains both game logic and terminal presentation. This is acceptable for a small CLI project, but a larger application would benefit from separating:
the game engine;
player strategies;
match management;
input handling;
rendering.

The heuristic AI is tactically competent but not guaranteed to be unbeatable.

The flat board is efficient for the current algorithms, although a nested structure might appear more intuitive when representing coordinates directly.

The use of random selection among equivalent corners and sides makes the AI less repetitive, but it also means that some complete game paths are not deterministic without controlling the random generator.

---

## 6. Possible Future Improvements

Possible extensions include:
Minimax-based unbeatable AI;
selectable AI difficulty levels;
separate strategy classes for random, heuristic and Minimax players;
separation of game logic from terminal rendering;
dependency injection for random move selection;
complete integration tests with mocked input;
automated tests for menu navigation;
enums for markers and game results;
type hints for methods and return values;
configurable board size;
configurable winning-line length;
player name support;
player-selected markers;
score history;
saved match statistics;
persistent settings;
graphical user interface;
web interface;
network multiplayer;
replay functionality;
move history and undo support.

If additional interfaces were introduced, the current class could be divided into:
a pure TicTacToeEngine;
player-strategy classes;
a match controller;
a CLI renderer and input adapter.

This would preserve the existing game rules while allowing several user interfaces to reuse the same engine.

---

## 7. Summary

The final implementation combines object-oriented state management, reusable rule definitions, calculated coordinate parsing, separated move responsibilities, tactical artificial intelligence and automated tests.

The design evolved from direct procedural control toward modular responsibilities and finally into a cohesive game object capable of supporting several game modes.

The current architecture was selected deliberately because it:
encapsulates state;
avoids global mutable data;
reduces repeated logic;
reuses single-game behaviour;
supports automated verification;
remains readable;
avoids unnecessary enterprise-level abstraction;
provides a clear path for future development.

The project demonstrates that object-oriented programming is most useful when state and related behaviours genuinely belong together.

It also demonstrates that artificial intelligence does not need to be maximally complex to be purposeful. A transparent priority-based strategy can provide meaningful behaviour while remaining understandable and testable.

The strongest design is not the one containing the greatest number of patterns or abstractions.

It is the one whose complexity remains proportional to the problem while making future changes safer and easier.
