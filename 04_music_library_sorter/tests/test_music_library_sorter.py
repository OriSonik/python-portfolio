import sys
from pathlib import Path

import pytest


PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from music_library_sorter import (
    Song,
    duration_to_seconds,
    load_songs,
    parse_song_line,
    sort_by_artist_az,
    sort_by_artist_za,
    sort_by_genre,
    sort_by_longest,
    sort_by_newest,
    sort_by_oldest,
    sort_by_shortest,
    sort_by_title,
)


def sample_songs():
    return [
        Song("Vangelis", "Ask The Mountains", "Voices", 1995, "07:55", "New Age"),
        Song("Adele", "Hello", "25", 2015, "04:56", "Pop"),
        Song("Moby", "Extreme Ways", "18", 2002, "03:57", "Alternative Rock"),
        Song("ATB", "My Everything", "Future Memories", 2009, "05:26", "Chillout Trance"),
    ]


def test_duration_to_seconds():
    assert duration_to_seconds("04:56") == 296
    assert duration_to_seconds("07:55") == 475
    assert duration_to_seconds("03:57") == 237


def test_parse_song_line_returns_song_object():
    line = "Adele - Hello - 25 - 2015 - 04:56 - Pop"

    song = parse_song_line(line)

    assert song == Song(
        artist="Adele",
        title="Hello",
        album="25",
        year=2015,
        duration="04:56",
        genre="Pop",
    )


def test_parse_song_line_strips_extra_spaces():
    line = "  Moby  -  Extreme Ways  -  18  -  2002  -  03:57  -  Alternative Rock  "

    song = parse_song_line(line)

    assert song.artist == "Moby"
    assert song.title == "Extreme Ways"
    assert song.album == "18"
    assert song.year == 2002
    assert song.duration == "03:57"
    assert song.genre == "Alternative Rock"


def test_parse_song_line_raises_error_for_invalid_row():
    line = "Adele - Hello - 25"

    with pytest.raises(ValueError, match="Invalid song row"):
        parse_song_line(line)


def test_load_songs_skips_header_and_loads_song_rows(tmp_path):
    data_file = tmp_path / "songs_data.txt"
    data_file.write_text(
        "Artist - Title - Album - Year - Time - Genre\n"
        "Adele - Hello - 25 - 2015 - 04:56 - Pop\n"
        "Moby - Extreme Ways - 18 - 2002 - 03:57 - Alternative Rock\n",
        encoding="utf-8",
    )

    songs = load_songs(data_file)

    assert len(songs) == 2
    assert songs[0].artist == "Adele"
    assert songs[1].title == "Extreme Ways"


def test_sort_by_artist_az():
    songs = sample_songs()

    sorted_songs = sort_by_artist_az(songs)

    assert [song.artist for song in sorted_songs] == ["Adele", "ATB", "Moby", "Vangelis"]


def test_sort_by_artist_za():
    songs = sample_songs()

    sorted_songs = sort_by_artist_za(songs)

    assert [song.artist for song in sorted_songs] == ["Vangelis", "Moby", "ATB", "Adele"]


def test_sort_by_title():
    songs = sample_songs()

    sorted_songs = sort_by_title(songs)

    assert [song.title for song in sorted_songs] == [
        "Ask The Mountains",
        "Extreme Ways",
        "Hello",
        "My Everything",
    ]


def test_sort_by_oldest():
    songs = sample_songs()

    sorted_songs = sort_by_oldest(songs)

    assert [song.year for song in sorted_songs] == [1995, 2002, 2009, 2015]


def test_sort_by_newest():
    songs = sample_songs()

    sorted_songs = sort_by_newest(songs)

    assert [song.year for song in sorted_songs] == [2015, 2009, 2002, 1995]


def test_sort_by_shortest():
    songs = sample_songs()

    sorted_songs = sort_by_shortest(songs)

    assert [song.duration for song in sorted_songs] == ["03:57", "04:56", "05:26", "07:55"]


def test_sort_by_longest():
    songs = sample_songs()

    sorted_songs = sort_by_longest(songs)

    assert [song.duration for song in sorted_songs] == ["07:55", "05:26", "04:56", "03:57"]


def test_sort_by_genre():
    songs = sample_songs()

    sorted_songs = sort_by_genre(songs)

    assert [song.genre for song in sorted_songs] == [
        "Alternative Rock",
        "Chillout Trance",
        "New Age",
        "Pop",
    ]