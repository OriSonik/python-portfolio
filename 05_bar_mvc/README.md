# Small Bar — Procedural MVP to MVC

A command-line cocktail bar application presented in two forms:

1. a small procedural MVP built with basic Python functions and data structures;
2. a structured Model-View-Controller implementation of the same use case.

The project demonstrates how a working beginner-level script can be deliberately evolved into a clearer, more testable architecture without changing the core business idea.



## Features

Both implementations allow the user to:

- load a cocktail menu from CSV;
- display available drinks and their ingredients;
- create an order from existing menu items;
- calculate the total order value;
- create a custom drink;
- validate the custom ingredient combination;
- optionally save a valid custom drink for future orders.

The initial menu contains 20 cocktails, including Mojito, Margarita, Aperol Spritz, BeTon and a custom Jägermeister-based drink.



## Custom Drink Rules

A new custom drink must contain:

- exactly one juice;
- one or two alcoholic ingredients;
- zero or one extra;
- zero to two mixers or ice options;
- only ingredients known by the application.

The validator checks the structure of the ingredient set. It does not attempt to predict whether the final drink will taste good.



## Project Structure

05_bar_mvc/
├── simple_version/
│   ├── __init__.py
│   ├── small_bar.py
│   └── bar_menu.csv
├── mvc_version/
│   ├── __init__.py
│   ├── main.py
│   ├── model.py
│   ├── view.py
│   ├── controller.py
│   └── bar_menu.csv
├── tests/
│   ├── test_simple_version.py
│   ├── test_model.py
│   └── test_controller.py
├── pytest.ini
├── requirements-dev.txt
├── README.md
└── DESIGN_DECISIONS.md



## Implementations


### Procedural MVP

`simple_version/small_bar.py` uses:
- lists and dictionaries;
- functions;
- loops and conditions;
- basic exception handling;
- direct `input()` and `print()` calls;
- CSV reading and appending.

The file intentionally keeps presentation, workflow, validation and persistence close together. It represents a small working MVP rather than a reusable architecture.


### MVC Version

The MVC implementation separates responsibilities:
- `model.py` — domain data, validation, menu persistence and order state;
- `view.py` — all command-line input and output;
- `controller.py` — application flow and coordination;
- `main.py` — dependency construction and application entry point.



## Requirements

- Python 3.10 or newer;
- no third-party packages required to run the application;
- `pytest` required only for automated tests.

Install the development dependency:
python -m pip install -r requirements-dev.txt



## Running the Procedural MVP

Open the procedural implementation directory:
cd simple_version
python small_bar.py



## Running the MVC Version

Run the MVC application from the project root:
python -m mvc_version.main



## Example Usage

=== SMALL BAR MVC ===
1. Show menu
2. Make an order
3. Show ingredients
0. Exit
Your choice: 2

Enter a drink number, N for a new drink or 0 to finish.

Your choice: 1
Mojito was added to the order.

Your choice: 0

=== YOUR ORDER ===
- Mojito: 28.00 PLN
Total: 28.00 PLN


A custom drink can be created with a combination such as:
jagermeister, passion fruit juice, mint, crushed ice


## Tests

Run all tests from the project root:
python -m pytest -q


The test suite covers:
- procedural validation rules;
- CSV menu loading;
- valid and invalid ingredient combinations;
- duplicate ingredient and duplicate name handling;
- optional persistence of custom drinks;
- order creation and total calculation;
- controller coordination through a test double instead of terminal input.

Current result:
24 passed


## Notes

The two CSV files are intentionally separate. This allows both implementations to be run and modified independently during comparison without one version changing the menu of the other.
