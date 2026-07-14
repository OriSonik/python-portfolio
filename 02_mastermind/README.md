\# Mastermind



A Python CLI implementation of the classic Mastermind-style code guessing game.



The project focuses on input validation, hidden code generation, feedback logic and clear terminal presentation.





\## Features



\- Generates a hidden 4-symbol code

\- Uses digits from 1 to 6

\- Each symbol appears only once

\- Gives feedback after every guess

\- Limits the game to 8 attempts

\- Validates player input

\- Displays guesses and feedback in a readable terminal layout





\## Technologies



Python • random • CLI • input validation • game logic





\## Project structure



\- `mastermind.py` — main game file

\- `README.md` — project documentation





\## Feedback system



Feedback symbols:



\- `+` means correct symbol in the correct position

\- `x` means correct symbol in the wrong position

\- `-` means symbol not present in the code





\## Running the application



From the main repository folder:

`py 02\_mastermind\\mastermind.py`



From the project folder:

`cd 02\_mastermind`

`py mastermind.py`





\## Game rules



The player has 8 attempts to guess the hidden 4-symbol code.



Valid guesses must contain:



\- exactly 4 symbols

\- digits from 1 to 6

\- no repeated symbols



The player wins by guessing the full code before all attempts are used.





\## Tested manually



The project was checked for:



\- game startup

\- valid guess handling

\- invalid guess rejection

\- repeated symbol rejection

\- feedback generation

\- win condition

\- lose condition

