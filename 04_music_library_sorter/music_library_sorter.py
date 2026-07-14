from dataclasses import dataclass


DATA_FILE = "songs_data.txt"
SEPARATOR = " - "


@dataclass
class Song:
    artist: str
    title: str
    album: str
    year: int
    duration: str
    genre: str


def duration_to_seconds(duration):
    minutes, seconds = duration.split(":")
    return int(minutes) * 60 + int(seconds)


def parse_song_line(line):
    parts = [part.strip() for part in line.strip().split(SEPARATOR)]

    if len(parts) != 6:
        raise ValueError(f"Invalid song row: {line.strip()}")

    artist, title, album, year, duration, genre = parts

    return Song(
        artist=artist,
        title=title,
        album=album,
        year=int(year),
        duration=duration,
        genre=genre,
    )


def load_songs(filename=DATA_FILE):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    song_lines = lines[1:]

    return [parse_song_line(line) for line in song_lines if line.strip()]


def print_songs(songs):
    if not songs:
        print("No songs to display.")
        return

    print()
    print(f"{'Artist':<28} {'Title':<28} {'Album':<28} {'Year':<6} {'Time':<7} {'Genre'}")
    print("-" * 115)

    for song in songs:
        print(
            f"{song.artist:<28} "
            f"{song.title:<28} "
            f"{song.album:<28} "
            f"{song.year:<6} "
            f"{song.duration:<7} "
            f"{song.genre}"
        )

    print()


def sort_by_artist_az(songs):
    return sorted(songs, key=lambda song: song.artist.lower())


def sort_by_artist_za(songs):
    return sorted(songs, key=lambda song: song.artist.lower(), reverse=True)


def sort_by_title(songs):
    return sorted(songs, key=lambda song: song.title.lower())


def sort_by_oldest(songs):
    return sorted(songs, key=lambda song: song.year)


def sort_by_newest(songs):
    return sorted(songs, key=lambda song: song.year, reverse=True)


def sort_by_shortest(songs):
    return sorted(songs, key=lambda song: duration_to_seconds(song.duration))


def sort_by_longest(songs):
    return sorted(songs, key=lambda song: duration_to_seconds(song.duration), reverse=True)


def sort_by_genre(songs):
    return sorted(songs, key=lambda song: (song.genre.lower(), song.artist.lower()))


def print_menu():
    print("=== MUSIC LIBRARY SORTER ===")
    print("1. Show original library")
    print("2. Sort by artist A-Z")
    print("3. Sort by artist Z-A")
    print("4. Sort by title")
    print("5. Sort by year: oldest first")
    print("6. Sort by year: newest first")
    print("7. Sort by duration: shortest first")
    print("8. Sort by duration: longest first")
    print("9. Sort by genre")
    print("0. Quit")
    print()


def run_program():
    try:
        songs = load_songs()
    except FileNotFoundError:
        print(f"Data file not found: {DATA_FILE}")
        return
    except ValueError as error:
        print(error)
        return

    while True:
        print_menu()
        choice = input("Choose option: ").strip()

        if choice == "1":
            print_songs(songs)
        elif choice == "2":
            print_songs(sort_by_artist_az(songs))
        elif choice == "3":
            print_songs(sort_by_artist_za(songs))
        elif choice == "4":
            print_songs(sort_by_title(songs))
        elif choice == "5":
            print_songs(sort_by_oldest(songs))
        elif choice == "6":
            print_songs(sort_by_newest(songs))
        elif choice == "7":
            print_songs(sort_by_shortest(songs))
        elif choice == "8":
            print_songs(sort_by_longest(songs))
        elif choice == "9":
            print_songs(sort_by_genre(songs))
        elif choice == "0":
            print("Goodbye. The music library fades out.")
            break
        else:
            print("Invalid option. Choose a number from the menu.")

        input("Press Enter to return to menu...")


if __name__ == "__main__":
    run_program()