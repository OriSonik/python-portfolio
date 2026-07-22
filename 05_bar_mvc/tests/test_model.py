import csv

import pytest

from mvc_version.model import BarModel, Drink


def create_menu_file(tmp_path):
    menu_file = tmp_path / "bar_menu.csv"
    with menu_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "price", "ingredients"])
        writer.writerow(["Mojito", "28.00", "rum|lime juice|mint|soda|crushed ice"])
        writer.writerow(["Aperol Spritz", "30.00", "aperol|prosecco|soda|ice cubes"])
    return menu_file


def test_model_loads_menu_from_csv(tmp_path):
    model = BarModel(create_menu_file(tmp_path))

    assert len(model.get_menu()) == 2
    assert model.get_menu()[0].name == "Mojito"
    assert model.get_menu()[0].price == 28.0


def test_model_raises_when_menu_file_is_missing(tmp_path):
    with pytest.raises(FileNotFoundError, match="Menu file was not found"):
        BarModel(tmp_path / "missing.csv")


def test_validation_accepts_valid_custom_drink(tmp_path):
    model = BarModel(create_menu_file(tmp_path))
    ingredients = [
        "jagermeister",
        "passion fruit juice",
        "mint",
        "crushed ice",
    ]

    valid, message = model.validate_ingredients(ingredients)

    assert valid is True
    assert message == "The ingredient set is valid."


@pytest.mark.parametrize(
    ("ingredients", "expected_message"),
    [
        (["vodka", "ice cubes"], "exactly one juice"),
        (["orange juice", "ice cubes"], "one or two alcohols"),
        (["vodka", "rum", "gin", "orange juice"], "one or two alcohols"),
        (["vodka", "orange juice", "mint", "cinnamon"], "only one extra"),
        (
            ["vodka", "orange juice", "tonic", "soda", "ice cubes"],
            "up to two mixers",
        ),
        (["vodka", "mango juice"], "Unknown ingredients"),
        (["vodka", "orange juice", "vodka"], "more than once"),
    ],
)
def test_validation_rejects_invalid_combinations(
    tmp_path, ingredients, expected_message
):
    model = BarModel(create_menu_file(tmp_path))

    valid, message = model.validate_ingredients(ingredients)

    assert valid is False
    assert expected_message in message


def test_create_custom_drink_without_saving_does_not_change_menu(tmp_path):
    model = BarModel(create_menu_file(tmp_path))

    drink = model.create_custom_drink(
        "Forest Passion",
        ["jagermeister", "passion fruit juice", "mint", "crushed ice"],
        save_to_menu=False,
    )

    assert drink.name == "Forest Passion"
    assert len(model.get_menu()) == 2


def test_create_custom_drink_can_be_saved_and_reloaded(tmp_path):
    menu_file = create_menu_file(tmp_path)
    model = BarModel(menu_file)

    model.create_custom_drink(
        "Forest Passion",
        ["jagermeister", "passion fruit juice", "mint", "crushed ice"],
        save_to_menu=True,
    )
    reloaded_model = BarModel(menu_file)

    assert len(reloaded_model.get_menu()) == 3
    assert reloaded_model.get_menu()[-1].name == "Forest Passion"


def test_duplicate_drink_name_is_rejected_case_insensitively(tmp_path):
    model = BarModel(create_menu_file(tmp_path))

    with pytest.raises(ValueError, match="already exists"):
        model.create_custom_drink(
            "mojito",
            ["rum", "lime juice", "mint", "crushed ice"],
            save_to_menu=False,
        )


def test_menu_drink_can_be_added_to_order(tmp_path):
    model = BarModel(create_menu_file(tmp_path))

    selected = model.add_menu_drink_to_order(2)

    assert selected.name == "Aperol Spritz"
    assert model.get_order() == (selected,)


def test_invalid_menu_number_is_rejected(tmp_path):
    model = BarModel(create_menu_file(tmp_path))

    with pytest.raises(IndexError, match="no drink"):
        model.add_menu_drink_to_order(0)


def test_order_total_is_calculated_from_drink_prices(tmp_path):
    model = BarModel(create_menu_file(tmp_path))
    model.add_menu_drink_to_order(1)
    model.add_drink_to_order(Drink("Custom", 25.0, ("vodka", "orange juice")))

    assert model.calculate_total() == 53.0
