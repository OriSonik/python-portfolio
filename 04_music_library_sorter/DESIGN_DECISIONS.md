# Design Decisions

## Table of Contents:
1. [Project Goal]
2. [Architecture]
3. [Key Design Decisions]
   3.1. [A Dataclass Domain Model Instead of Raw Indexed Lists]
   3.2. [Typed Fields Instead of Treating Every Value as Text]
   3.3. [Separate Parsing and File Loading Instead of One Combined Operation]
   3.4. [A Human-readable Text Format with an Explicit Separator]
   3.5. [Module-relative Paths Instead of Current-working-directory Paths]
   3.6. [Pure Sorting Functions Instead of Mutating the Original Library]
   3.7. [Semantic Sort Keys Instead of Sorting Raw Field Values]
   3.8. [Duration Conversion to Seconds Instead of Lexicographic Comparison]
   3.9. [Case-insensitive and Deterministic Text Sorting]
   3.10. [A Cohesive Single Module Instead of Premature Module Separation]
   3.11. [Error Handling at the Application Boundary]
   3.12. [An Iterative Menu and a Reusable Presentation Function]
   3.13. [Automated Pytest Verification Instead of Manual Testing Only]
   3.14. [An Explicit Module Entry Point Instead of Automatic Execution]
4. [Testing Approach]
5. [Trade-offs]
6. [Possible Future Improvements]
7. [Summary]

---

## 1. Project Goal

The goal of this project is to build a command-line music library sorter that loads song data from a text file, converts each row into a structured Python object and allows the user to display the library in several useful orders.

The application supports sorting by:
- artist from A to Z;
- artist from Z to A;
- song title;
- release year from oldest to newest;
- release year from newest to oldest;
- duration from shortest to longest;
- duration from longest to shortest;
- genre.

The project demonstrates:
- file handling;
- text parsing;
- structured domain modelling;
- type conversion;
- sorting with custom keys;
- path handling;
- input-driven CLI flow;
- error handling;
- automated testing.

The final implementation is the result of an evolutionary design process. Earlier approaches offered simpler solutions, intermediate approaches improved structure and data handling, and the current architecture was chosen deliberately because it provides the best balance of clarity, testability and proportional complexity.

The project intentionally remains small and dependency-free at runtime. Its architecture is designed to solve the current problem clearly without introducing layers that would not yet provide enough value.

---

## 2. Architecture

The application is organised into five logical areas inside one Python module.


### Domain model

The `Song` dataclass represents one library entry:
@dataclass
class Song:
    artist: str
    title: str
    album: str
    year: int
    duration: str
    genre: str


### Data parsing and loading:

The following functions convert text data into domain objects:
parse_song_line() — parses one line;
load_songs() — loads the complete file;
duration_to_seconds() — converts duration into a sortable numeric value.


### Sorting logic:

Dedicated functions provide individual sorting strategies:
sort_by_artist_az();
sort_by_artist_za();
sort_by_title();
sort_by_oldest();
sort_by_newest();
sort_by_shortest();
sort_by_longest();
sort_by_genre().


### Presentation:

The print_songs() function displays a collection in a readable tabular layout.

The print_menu() function displays the available commands.


### Application coordination:

The run_program() function:
- loads the source file;
- handles loading errors;
- displays the menu;
- interprets the selected option;
- calls the appropriate sorting function;
- sends the result to the presentation function;
- controls application termination.

The application starts through:
if __name__ == "__main__":
    run_program()

---

## 3. Key Design Decisions


## 3.1. A Dataclass Domain Model Instead of Raw Indexed Lists

Each library entry is represented by a Song dataclass.

An alternative approach would represent every song as a raw list:
["Adele", "Hello", "25", "2015", "04:56", "Pop"]

That approach is short, but every value must then be accessed through a numeric index:
song[0]
song[3]
song[5]

A dataclass was selected because the fields have clear domain meanings.

The current code can use:
song.artist
song.year
song.genre

instead of relying on the developer to remember the meaning of each index.

This approach provides:
- readable field access;
- explicit field names;
- a clear definition of one song record;
- generated object equality;
- easier automated testing;
- safer refactoring;
- better editor and static-analysis support;
- a natural location for future song-related behaviour.

The generated equality method is especially useful in tests because complete Song objects can be compared directly.

A dictionary could also provide named fields. However, a dataclass makes the expected structure explicit and prevents every record from having an accidental or inconsistent set of keys.

A raw list remains suitable for temporary tabular data or very small transformations. For a domain object used throughout the application, the dataclass offers clearer intent.


## 3.2. Typed Fields Instead of Treating Every Value as Text

The Song model stores the release year as an integer:
year: int

The parser performs the conversion when the object is created:
year=int(year)

An alternative approach would leave every imported value as a string.

Typed conversion was selected because a release year is a numeric value, even though it originates from a text file.

This approach provides:
- correct numeric sorting;
- clearer meaning of the field;
- earlier detection of invalid data;
- no repeated conversion inside sorting functions;
- simpler comparisons;
- preparation for future numeric filtering.

For example, the application can sort directly with:
key=lambda song: song.year

If the value remained a string, correct ordering would depend on consistent formatting and equal string length.

The duration remains stored as a formatted string because that is the most readable representation for display. It is converted into seconds only when a numeric comparison is required.

This deliberately separates:
the best representation for presentation;
the best representation for computation.


## 3.3. Separate Parsing and File Loading Instead of One Combined Operation

The application separates:
parse_song_line()
                     from:
load_songs()

An alternative approach would open the file, split every line, convert every field and construct every object inside one large function.

The responsibilities were separated because file access and row interpretation are different operations.

load_songs() is responsible for:
- opening the file;
- reading its contents;
- skipping the header;
- ignoring empty lines.

parse_song_line() is responsible for:
- splitting one row;
- trimming surrounding whitespace;
- validating the number of fields;
- converting the year;
- creating a Song object.

This approach provides:
- smaller functions;
- easier unit testing;
- reusable parsing logic;
- clearer error locations;
- the ability to test malformed rows without creating a file;
- simpler future replacement of the file source.

For example, a future version could obtain individual rows from:
- an API;
- a database;
- a graphical file picker;
- pasted text.

The same parser could still be reused.


## 3.4. A Human-readable Text Format with an Explicit Separator

The application uses:
SEPARATOR = " - "
to separate fields in the data file.

An alternative approach would use:
- a comma-separated CSV;
- JSON;
- a database;
- a Python data structure embedded directly in the code.

The current text format was selected because it is easy to inspect and edit manually. Every row remains readable even without opening the file through the application.

Defining the separator as a named constant provides:
- one location for the format definition;
- no repeated separator literals;
- easier format changes;
- clearer parser intent;
- consistency between the data file and the parser.

The exact separator includes surrounding spaces, which means ordinary hyphens inside values, such as A-ha, do not automatically split the row.

The trade-off is that the format does not provide the escaping and quoting rules of a standard CSV parser.

A standard CSV or JSON format would become preferable if:
- fields could contain the exact separator;
- the data were exchanged with other applications;
- the users could enter arbitrary text;
- the file format became a public interface;
- stronger validation were required.

For the current controlled dataset, the simple format provides readability with minimal complexity.


## 3.5. Module-relative Paths Instead of Current-working-directory Paths

The location of the data file is calculated through:
PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "songs_data.txt"

An alternative approach would open:
"songs_data.txt"
directly and assume that the program is always launched from the project directory.

The module-relative path was selected because the location of the data file belongs to the project structure, not to the terminal’s current directory.

This approach provides:
- predictable file discovery;
- correct behaviour when the program is launched from the repository root;
- correct behaviour when the project is started through an IDE;
- cross-platform path construction;
- no manual string concatenation;
- a reusable Path object for tests and future features.

Using pathlib also makes the code more expressive than manually joining path strings.

A user-selected path could become useful if the application later allowed importing different libraries. For the bundled demonstration dataset, the module-relative default is the safer choice.


## 3.6. Pure Sorting Functions Instead of Mutating the Original Library

Each sorting function returns a new list through sorted().

For example:
return sorted(songs, key=lambda song: song.year)

An alternative approach would call:
songs.sort(...)
and modify the original list in place.

Returning a new sorted collection was selected because displaying one order should not permanently change the source library.

This approach provides:
- preservation of the original file order;
- predictable function behaviour;
- easier automated testing;
- no hidden mutation;
- independent sorting operations;
- the ability to return to the original library view;
- safer reuse of the same collection.

The menu can therefore display:
- the original order;
- one sorted order;
- another sorted order;
without reloading the file after every operation.

In-place sorting could be appropriate if the application explicitly allowed the user to reorganise and save the library permanently.

The current project is a viewer and sorter, so non-mutating functions better match its purpose.


## 3.7. Semantic Sort Keys Instead of Sorting Raw Field Values

Every sorting function defines a key that reflects the meaning of the selected field.

Examples include:
key=lambda song: song.artist.lower()
and:
key=lambda song: song.year

An alternative approach would sort complete records directly or use numeric indexes from raw lists.

Semantic keys were selected because each operation should express exactly which property controls the order.

This approach provides:
- self-documenting sorting logic;
- independence from physical field positions;
- easier extension;
- fewer indexing mistakes;
- correct handling of field types;
- straightforward unit tests.

The named model and semantic key work together:
song.title
                               is clearer than:
song[1]

If the order of fields in the input format changed, index-based sorting could silently begin using the wrong value. Attribute-based sorting remains connected to the meaning of the field.


## 3.8. Duration Conversion to Seconds Instead of Lexicographic Comparison

Song duration is displayed as text in MM:SS format, but sorting uses:
duration_to_seconds()

The function converts: 04:56 into: 296

An alternative approach would sort the original duration strings or split them into textual components.

Numeric conversion was selected because duration represents elapsed time, not text.

This approach provides:
- correct chronological comparison;
- one reusable conversion rule;
- no dependence on zero-padding;
- clearer intent;
- easier future duration calculations;
- support for totals and averages.

Lexicographic sorting can appear to work when all values use the same exact format, but it relies on formatting rather than meaning.

Converting duration into one numeric unit makes the comparison explicit and reliable.

A future version could store duration internally as seconds and format it only during display. 
The current implementation keeps the original text because it is convenient for presentation while still using a semantic numeric key for sorting.


## 3.9. Case-insensitive and Deterministic Text Sorting

Artist, title and genre sorting use lowercase comparison keys.

For example:
song.artist.lower()

An alternative approach would sort the original strings directly.

Case-insensitive comparison was selected because capitalisation should not affect the alphabetical position of an artist or title.

This provides:
- natural alphabetical order;
- consistent treatment of differently capitalised values;
- predictable output;
- no need to modify the displayed text.

Genre sorting uses a compound key:
(song.genre.lower(), song.artist.lower())

The primary order is genre, while artists inside the same genre are ordered alphabetically.

This creates deterministic and readable groups instead of relying only on the original file order.

A more advanced version could additionally handle:
- locale-aware alphabetical ordering;
- accented characters;
- articles such as The;
- normalised artist aliases.

For the current English-language dataset, lowercase keys provide an appropriate level of complexity.


## 3.10. A Cohesive Single Module Instead of Premature Module Separation

The current application keeps its model, loading logic, sorting functions, presentation and CLI coordination in one module.

An alternative architecture would immediately divide the program into separate files such as:
models.py;
file_handling.py;
reports.py;
display.py;
main.py.

A cohesive single module was selected because the current application is small and all responsibilities remain easy to locate.

This approach provides:
- simple project navigation;
- fewer imports;
- no package configuration;
- straightforward execution;
- low architectural overhead;
- a complete view of the program in one file.

The code is still divided internally through small functions and clear logical sections.

Module separation becomes valuable when files or responsibilities become difficult to understand independently.

A future version should split the project when it introduces:
- editing and deleting songs;
- several data sources;
- persistent configuration;
- advanced reports;
- multiple user interfaces;
- a larger domain model;
- database storage.

The current design deliberately distinguishes between useful modularity and unnecessary file fragmentation.


## 3.11. Error Handling at the Application Boundary

The run_program() function catches:
FileNotFoundError;
ValueError.

An alternative approach would allow low-level exceptions to terminate the application with a traceback or catch them inside every helper function.

Handling errors at the application boundary was selected because parsing and loading functions should report failure accurately, while the CLI should decide how the failure is presented to the user.

This approach provides:
- clear separation between error detection and user communication;
- readable terminal messages;
- no partially loaded library;
- predictable program termination;
- reusable lower-level functions;
- preservation of useful exception types.

parse_song_line() raises a ValueError when the number of fields is invalid.

It does not silently skip malformed data because silently ignoring a damaged row could hide a problem in the library.

A larger application could collect and report multiple invalid rows instead of stopping on the first one.

For the current project, failing clearly is safer than accepting incomplete or ambiguous data.


## 3.12. An Iterative Menu and a Reusable Presentation Function

The menu runs inside a while True loop until the user selects the quit option.

An alternative approach would:
- execute only one selected operation;
- call the menu recursively;
- duplicate printing code in every branch.

The iterative menu was selected because the user should be able to inspect several sorting orders during one session.

This approach provides:
- repeated interaction without restarting the program;
- constant call-stack depth;
- one clear termination condition;
- no recursive navigation;
- simple invalid-option handling.

Every menu branch sends a collection to: 
print_songs()
instead of formatting the table independently.

This centralises:
- column widths;
- headings;
- empty-library handling;
- record formatting.

A separate renderer class would be unnecessary at the current scale. One presentation function provides sufficient reuse.


## 3.13. Automated Pytest Verification Instead of Manual Testing Only

The project includes automated tests written with pytest.

The tests verify:
- conversion of duration into seconds;
- creation of a Song object from one text row;
- the removal of extra whitespace;
- malformed rows rejection;
- loading data while skipping the header;
- artist sorting in both directions;
- title sorting;
- year sorting in both directions;
- duration sorting in both directions;
- genre sorting.

Automated testing was selected because sorting and parsing rules are deterministic and can be verified without interacting with the terminal.

This approach provides:
- repeatable verification;
- fast regression detection;
- confidence during refactoring;
- documentation of expected behaviour;
- independent testing of each responsibility;
- a proof that source data are interpreted correctly.

The file-loading test uses pytest’s tmp_path fixture.

This means the test creates its own temporary data file instead of modifying the real project library.

That provides:
- test isolation;
- repeatability;
- no dependency on production data;
- automatic cleanup;
- reliable execution on different systems.

Manual testing remains useful for checking the complete menu flow and table layout, but it does not replace automated verification of the core rules.


## 3.14. An Explicit Module Entry Point Instead of Automatic Execution

The application uses:
if __name__ == "__main__":
    run_program()


An alternative approach would call: 
run_program() 
directly at module level.

The explicit entry point was selected because importing the module should not automatically launch the interactive menu.

This approach provides:
- safe imports in automated tests;
- reuse of the Song model and sorting functions;
- clear separation between definitions and execution;
- predictable module behaviour;
- preparation for future package structure.

Another interface could import the existing functions without starting the CLI.

---

## 4. Testing Approach

The test suite focuses on deterministic domain and data-processing logic.

Parsing tests:
The parser is verified for:
- correct field mapping;
- conversion of year into an integer;
- stripping of surrounding whitespace;
- rejection of incomplete rows.
- Loading tests

File loading is verified using a temporary file created by pytest.
The test confirms that:
- the header is skipped;
- song rows are loaded;
- records are returned in source order;
- parsed objects contain the expected values.
- Sorting tests

Every public sorting strategy has a dedicated test:
- artist A–Z;
- artist Z–A;
- title;
- oldest first;
- newest first;
- shortest first;
- longest first;
- genre.

The tests compare the relevant output fields rather than relying on printed terminal text.
This keeps the tests focused on behaviour rather than presentation.


Current test boundary:

The current tests do not yet cover:
- print_songs() output formatting;
- menu navigation;
- invalid menu options;
- missing data files;
- invalid year values;
- malformed duration values;
- empty source files;
- duplicate records.

These scenarios are suitable candidates for future unit and integration tests.

Terminal output could be tested through pytest’s capsys fixture.

User input could be tested through monkeypatch.

---

## 5. Trade-offs

The project intentionally prioritises:
- a readable dataclass over anonymous lists;
- a simple text file over a database;
- a custom separator over a more complex serialisation format;
- a cohesive module over premature package separation;
- non-mutating sorting over permanent reordering;
- explicit functions over a larger service-class architecture;
- clear failure on malformed data over silent recovery;
- CLI simplicity over a graphical interface.

The current separator format is easy to read but does not support arbitrary escaped values as safely as CSV or JSON.

The complete file is loaded into memory at once. This is appropriate for a small demonstration library, but a very large collection should be streamed or stored in a database.

The Song object stores duration as a formatted string and converts it when required. This preserves simple display formatting, but repeated duration sorting performs the conversion each time.

The current module includes both application logic and terminal presentation. This keeps the project compact, although a larger application would benefit from separating those layers.

The project supports sorting but does not save the selected order back to the data file. This is intentional: the application presents alternative views without modifying the source library.

---

## 6. Possible Future Improvements

Possible extensions include:
- filtering by artist, album, year or genre;
- searching by partial text;
- adding, editing and deleting songs;
- saving changes to the source file;
- CSV or JSON support;
- validation of year ranges;
- validation of duration format;
- duplicate detection;
- total library duration;
- genre statistics;
- oldest and newest song reports;
- longest and shortest song reports;
- multiple simultaneous sorting keys;
- user-selected input files;
- export to a new file;
- persistent user settings;
- pagination for large libraries;
- database storage;
- graphical user interface;
- web interface;
- additional automated integration tests.

If the application grows, the module could be divided into:
models.py — domain objects;
repository.py — data loading and saving;
services.py — sorting, filtering and reports;
cli.py — terminal interaction;
main.py — application entry point.

A repository abstraction would become especially useful if text-file storage were replaced or supplemented by a database.

---

## 7. Summary

The final implementation uses a structured Song model, typed data conversion, separated parsing and loading, module-relative paths, semantic sorting keys, non-mutating operations and automated tests.

The design evolved from manipulating anonymous text rows toward treating each song as a defined domain object.

The current architecture was selected deliberately because it:
- makes the data model explicit;
- removes dependency on remembered numeric indexes;
- keeps file handling testable;
- preserves the original library order;
- sorts values according to their real meaning;
- works reliably from different launch locations;
- handles damaged input clearly;
- remains proportionate to the size of the project;
- provides a direct path for future extension.

The project demonstrates that data processing becomes safer and easier to explain when raw input is converted into meaningful objects at the system boundary.

It also demonstrates that modular design does not always require a large number of files. The current implementation separates responsibilities through focused functions while keeping a small application cohesive.

The strongest design is the one that represents the domain clearly, makes invalid states visible and introduces additional complexity only when the project genuinely requires it.