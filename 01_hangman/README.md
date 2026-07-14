\# Hangman



A simple Python CLI word guessing game.



The project focuses on basic control flow, input validation, random word selection and readable terminal interaction.





\## Features



\- Random word selection from multiple categories

\- Category hint shown before the game starts

\- Letter-by-letter guessing

\- Tracks used letters

\- Prevents repeated guesses

\- Validates player input

\- Ends with win or lose condition





\## Technologies



Python • random • CLI • basic input validation





\## Project structure



\- `hangman.py` — main game file

\- `README.md` — project documentation





\## Running the application



From the main repository folder:

`py 01\_hangman\\hangman.py`



From the project folder:

`cd 01\_hangman`

`py hangman.py`





\## Game rules



The player has to guess a hidden word one letter at a time.



The game shows:



\- selected category

\- hidden word progress

\- remaining guesses

\- already used letters



The player wins when the full word is revealed before running out of guesses.





\## Tested manually



The project was checked for:



\- game startup

\- valid letter guessing

\- invalid input handling

\- repeated letter handling

\- win condition

\- lose condition

