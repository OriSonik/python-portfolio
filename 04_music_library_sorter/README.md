\# Music Library Sorter



A Python CLI application for loading a music library from a text file and sorting songs by artist, title, year, duration and genre.



The project focuses on text file parsing, structured data representation, sorting logic and automated tests.





\## Features



\- Loads songs from a text file

\- Parses song records into structured Python objects

\- Displays songs in a readable table

\- Sorts songs by artist, title, year, duration and genre

\- Handles missing or invalid data files

\- Includes pytest tests for core logic





\## Technologies



Python • dataclasses • pathlib • pytest • TXT parsing • CLI





\## Project structure



\- `music\_library\_sorter.py` — main application logic

\- `songs\_data.txt` — source music library data

\- `tests/test\_music\_library\_sorter.py` — automated tests

\- `README.md` — project documentation





\## Data format



The application reads song records from `songs\_data.txt`.



Expected row format:

`Artist - Title - Album - Year - Time - Genre`



Example:

`Adele - Hello - 25 - 2015 - 04:56 - Pop`



\## Running the application



From the main repository folder:

`py 04\_music\_library\_sorter\\music\_library\_sorter.py`



From the project folder:

`cd 04\_music\_library\_sorter`

`py music\_library\_sorter.py`





\## Running tests



From the main repository folder:

`py -m pytest 04\_music\_library\_sorter\\tests`





\## Tested logic



The test suite verifies:



\- duration conversion

\- song line parsing

\- invalid row handling

\- file loading

\- sorting by artist

\- sorting by title

\- sorting by year

\- sorting by duration

\- sorting by genre

