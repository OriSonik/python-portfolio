# Design Decisions


## Table of Contents:
1. [Project Goal]
2. [Architecture]
3. [Key Design Decisions]
   3.1. [The Same Use Case in Two Implementations]
   3.2. [A Procedural MVP as the Deliberate Baseline]
   3.3. [A Dataclass for the Drink Entity]
   3.4. [Business Rules and State in the Model]
   3.5. [All Terminal Interaction in the View]
   3.6. [Workflow Coordination in the Controller]
   3.7. [CSV Persistence Instead of a Database]
   3.8. [Returned Results and Exceptions Instead of Printing in the Model]
   3.9. [Dependency Injection Instead of Internal Object Construction]
   3.10. [Separate CSV Files for Independent Comparison]
4. [Testing Approach]
5. [Trade-offs]
6. [Possible Future Improvements]
7. [Summary]

---


## 1. Project Goal

The goal of this project is to demonstrate the evolution of a small command-line application from a procedural Minimum Viable Product into a proper Model-View-Controller architecture.

The application represents a small cocktail bar. It loads a menu from CSV, accepts orders, calculates the order total, validates custom drink combinations and optionally stores new drinks for future use.

The project is designed to show two different levels of implementation:
- a compact procedural script that solves the immediate problem;
- a structured MVC application that separates domain logic, presentation and coordination.

The final implementation is the result of an evolutionary design process. Earlier approaches offered simpler solutions, intermediate approaches improved structure and validation, and the current architecture was chosen deliberately because it provides the best balance of clarity, testability, and proportional complexity.

The comparison is part of the project itself. The procedural implementation is not treated as defective code. It is a valid MVP whose limitations become visible when the application grows.

---


## 2. Architecture

The project contains two independent implementations of the same use case.


### Procedural implementation

small_bar.py
├── ingredient collections
├── CSV loading and saving
├── validation functions
├── menu and order presentation
├── user input handling
└── application control flow

The procedural version keeps all responsibilities in one file. Data is represented with lists and dictionaries. Functions share the menu and order data through arguments and return values.


### MVC implementation

main.py
  └── creates and connects the components

controller.py
  └── coordinates user actions and application flow

view.py
  └── reads input and displays information

model.py
  ├── represents drinks
  ├── owns menu and order state
  ├── validates custom recipes
  └── reads and writes CSV data


The MVC execution flow is:

User
  ↓
View
  ↓
Controller
  ↓
Model
  ↓
Controller
  ↓
View


The `main.py` module creates the dependencies explicitly:
controller = BarController(BarModel(menu_file), BarView())
controller.run()

---


## 3. Key Design Decisions


### 3.1. The Same Use Case in Two Implementations

Both versions implement the same main behaviours:
- menu loading;
- menu display;
- order creation;
- total calculation;
- custom drink validation;
- optional persistence of a new drink.

An alternative would be to use different application ideas for the beginner and MVC examples.

The same use case was selected because architectural differences are easier to evaluate when the business requirements remain stable.

This approach provides:
- direct comparison of code organisation;
- visible movement of responsibilities between components;
- evidence that architecture changes do not require changing the product idea;
- a clear explanation of why MVC becomes useful;
- a practical refactoring narrative for technical interviews.

The trade-off is duplicated implementation effort. That duplication is deliberate because the educational value comes from comparing equivalent solutions.


### 3.2. A Procedural MVP as the Deliberate Baseline

The procedural version uses one main Python file with functions, lists, dictionaries, loops, conditions, direct terminal interaction and CSV operations.

An alternative would be to start immediately with classes and separate modules.

The procedural baseline was selected because it represents a realistic first solution to a small problem. Its complete control flow can be followed from top to bottom without understanding architectural patterns.

This solution provides:
- a low entry barrier;
- visible program flow;
- limited abstraction;
- quick implementation of the core idea;
- a credible starting point for architectural evolution.

Its limitation is that input handling, output, validation, state management and persistence remain close together. Changes in one area can therefore affect unrelated parts of the file.

For a very small one-use script, the procedural version may remain the better choice. MVC becomes justified when the program is expected to grow, be tested extensively or support another interface.


### 3.3. A Dataclass for the Drink Entity

The MVC model represents a drink with:

@dataclass(frozen=True)
class Drink:
    name: str
    price: float
    ingredients: tuple[str, ...]


The procedural version uses dictionaries instead.

A dataclass was selected because every drink has the same named fields and represents one domain concept.

This solution provides:
- explicit attributes;
- type information;
- generated initialisation and representation methods;
- fewer string-based dictionary lookups;
- easier comparison in tests;
- a clear domain vocabulary.

The dataclass is frozen because a drink recipe should not change accidentally after it has been added to an order. A new `Drink` object can be created when a recipe needs to change.

A dictionary remains appropriate for the compact MVP because it requires less initial structure and is easy to populate directly from CSV rows.


### 3.4. Business Rules and State in the Model

The `BarModel` owns:
- the loaded menu;
- the current order;
- custom drink validation;
- duplicate-name checks;
- order total calculation;
- CSV menu persistence.

An alternative would place validation and total calculation in the controller because the controller receives the user actions.

The Model was selected as the owner of these responsibilities because they describe the bar domain rather than the terminal workflow.

This separation provides:
- one source of truth for business rules;
- validation independent from the command-line interface;
- reusable order calculations;
- direct unit testing;
- no domain state stored in the View;
- a thinner Controller.

If a graphical or web interface were added, the same Model could remain in use.


### 3.5. All Terminal Interaction in the View

The `BarView` contains all `input()` and `print()` operations used by the MVC implementation.

The Model and Controller do not read directly from the keyboard or format terminal screens.

An alternative would let the Controller request input directly and use the View only for larger displays.

Complete terminal ownership was selected because presentation is one responsibility. Mixing `input()` across multiple classes would make the application harder to test and replace.

This approach provides:
- a clear interface boundary;
- consistent terminal formatting;
- no user-interface code in the Model;
- easier replacement with a GUI or web View;
- controller tests using a fake View instead of patched built-in functions.

The View remains intentionally simple. It does not validate business rules or modify application state.


### 3.6. Workflow Coordination in the Controller

The `BarController` coordinates actions such as:
- reacting to main-menu choices;
- starting and finishing an order;
- requesting custom drink data from the View;
- calling Model operations;
- passing results back to the View.

An alternative would place the entire application loop in `main.py` or let the View call the Model directly.

A Controller was selected to keep navigation and use-case flow separate from both presentation and domain rules.

This solution provides:
- visible application workflow;
- no direct View-to-Model dependency;
- reusable domain logic;
- focused controller tests;
- clear handling of successful and failed operations;
- a small entry-point module.

The Controller does not calculate totals or validate ingredients itself. It delegates those responsibilities to the Model.


### 3.7. CSV Persistence Instead of a Database

Both implementations store the drink menu in CSV.

An alternative would use JSON, SQLite or an external database.

CSV was selected because the stored data is small, flat and human-readable. The file can be inspected and edited without database tooling.

This approach provides:
- no external service;
- no additional runtime dependency;
- immediate application startup;
- simple append operations;
- transparent example data;
- easy repository distribution.

The trade-offs are limited schema enforcement, weak support for concurrent writes and no relational structure.

SQLite would become more appropriate when the application needs separate tables for drinks, ingredients, orders and order items. PostgreSQL would be justified only when the project introduces a server application, multiple users or deployment infrastructure.


### 3.8. Returned Results and Exceptions Instead of Printing in the Model

The MVC Model returns data and validation messages. Operations that cannot create a valid drink raise `ValueError` with a meaningful explanation.

The Model does not print messages.

An alternative would print validation failures directly inside `validate_ingredients()` or `create_custom_drink()`.

Returned values and exceptions were selected because the Model should describe outcomes without deciding how they are presented.

This approach provides:
- testable validation results;
- no terminal dependency;
- one error path for custom drink creation;
- freedom for the View to format messages;
- compatibility with future interfaces;
- clearer separation between failure detection and presentation.

The procedural version intentionally prints validation messages directly because its goal is simplicity rather than interface independence.


### 3.9. Dependency Injection Instead of Internal Object Construction

The Controller receives the Model and View through its constructor:
BarController(model, view)

An alternative would make `BarController` create `BarModel` and `BarView` internally.

Constructor injection was selected because the Controller depends on behaviours, not on one hard-coded environment.

This solution provides:
- easy replacement of the real View with a fake View in tests;
- explicit dependencies;
- simpler controller setup;
- no terminal input during automated tests;
- flexibility for another interface implementation.

A dependency-injection framework would be excessive for this project. Direct constructor arguments provide the required flexibility without additional complexity.


### 3.10. Separate CSV Files for Independent Comparison

The procedural and MVC directories contain separate copies of the initial menu.

An alternative would make both implementations use one shared data file.

Separate files were selected because both applications allow users to append custom drinks. Running one version should not silently modify the starting data of the other version during comparison.

This approach provides:
- independent demonstrations;
- predictable initial state;
- easier manual testing;
- no path dependency between implementations;
- reduced risk of one version affecting the other.

The trade-off is duplicated seed data. A shared repository or migration tool would become useful if both interfaces were intended to operate on one production dataset.

---


## 4. Testing Approach

The project uses `pytest` and currently contains 24 automated tests.

The procedural tests focus on the custom drink validator because it contains the most important independent rule set in the MVP.

The MVC Model tests cover:
- loading menu rows from CSV;
- missing menu files;
- valid custom combinations;
- missing or excessive ingredient categories;
- unknown ingredients;
- duplicate ingredients;
- optional menu persistence;
- menu reload after saving;
- duplicate drink names;
- menu selection;
- invalid menu numbers;
- order total calculation.

The Controller tests use a `FakeView` instead of real terminal input.

The fake records:
- displayed menus;
- displayed orders;
- messages;
- requested actions;
- custom drink data.

This makes it possible to test workflow coordination without patching `input()` or analysing printed output.

The test command is:
python -m pytest -q

Current result:
24 passed


Manual testing remains useful for terminal layout and complete interactive sessions, but business rules and controller flow are covered automatically.

---


## 5. Trade-offs

The project intentionally prioritises:
- a visible architectural comparison over avoiding duplicated code;
- clarity over minimum file count in the MVC version;
- simple CSV persistence over database features;
- a fixed custom drink price over pricing complexity;
- structural recipe validation over flavour prediction;
- one active order over order history;
- a command-line interface over graphical presentation;
- direct Python standard-library tools over external frameworks.

The validation rules describe one simplified category of custom fruit-based drinks. They do not model every real cocktail style. Existing menu items may contain ingredients or structures that would not pass the custom-drink validator.

This is deliberate: the menu represents known recipes, while the creator accepts only combinations that fit the small bar's simplified rules.

MVC introduces more files and more indirection than the procedural version. For a script that will never grow beyond its current size, that additional structure may not provide enough value.

For an application with growing rules, automated tests or multiple interfaces, the separation becomes beneficial.

---


## 6. Possible Future Improvements

Possible extensions include:
- SQLite persistence;
- a repository layer separating storage from the Model;
- separate `Ingredient`, `Order` and `OrderItem` entities;
- support for alcohol-free drinks;
- configurable ingredient categories;
- recipe quantities and units;
- ingredient stock management;
- calculated prices based on ingredients;
- order history;
- removal of items from an active order;
- JSON or database-based configuration;
- GUI or web View using the same domain logic;
- more detailed validation results;
- protection against concurrent file writes;
- broader cocktail-family validation.

A database-backed version should not simply replace CSV calls with SQL inside `BarModel`. A dedicated repository interface would keep persistence decisions separate from business rules.

---


## 7. Summary

The project demonstrates that a procedural MVP and an MVC application can both be valid solutions when judged against different goals.

The procedural implementation is compact, direct and suitable for proving the idea quickly. Its limitations appear when responsibilities begin to overlap and automated testing requires interaction with terminal and file operations.

The MVC implementation separates:
- domain rules and state in the Model;
- terminal interaction in the View;
- workflow coordination in the Controller;
- dependency construction in the entry point.

The selected architecture is intentionally proportional. It applies MVC clearly without introducing a database server, framework or unnecessary hierarchy.

The result is a small but complete example of architectural evolution driven by concrete maintainability and testability needs rather than by pattern usage alone.
