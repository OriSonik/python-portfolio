\# Tic Tac Toe



A Python CLI Tic Tac Toe game with multiple game modes, object-oriented structure and automated tests.



The project focuses on board game logic, move validation, simple AI behavior and pytest-based verification.





\## Features



\- Object-oriented game structure

\- Coordinate-based move input

\- Supports input such as A1, B2, C3 and reversed format like 1A or 3C

\- Two-player mode

\- Player vs random computer mode

\- Player vs smart computer mode

\- Wimbledon mode: 3-set-win match against smart computer

\- Win and draw detection

\- Smart computer can win, block and choose strategic fields

\- Automated tests for core logic





\## Technologies



Python • OOP • random • pytest • CLI • board game logic





\## Project structure



\- `tic\_tac\_toe.py` — main game file

\- `tests/test\_tic\_tac\_toe.py` — automated tests

\- `README.md` — project documentation





\## Game modes



Available modes:



\- Two players

\- Player vs random computer

\- Player vs smart computer

\- Wimbledon mode: 3-set-win match: Player vs smart computer



In Wimbledon mode, the first side to win 3 games wins the match. Draws do not give points.





\## Running the application



From the main repository folder:

`py 03\_tic\_tac\_toe\\tic\_tac\_toe.py`



From the project folder:

`cd 03\_tic\_tac\_toe`

`py tic\_tac\_toe.py`





\## Running tests



From the main repository folder:

`py -m pytest 03\_tic\_tac\_toe\\tests`





\## Tested logic



The test suite verifies:



\- move parsing

\- row-column and column-row coordinates

\- invalid input handling

\- placing markers on the board

\- rejecting taken fields

\- available move detection

\- all win lines for both markers

\- draw detection

\- tactical move detection

\- smart AI winning move

\- smart AI blocking move

\- smart AI center selection

