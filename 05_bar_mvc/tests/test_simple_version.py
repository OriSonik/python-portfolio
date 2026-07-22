from simple_version.small_bar import validate_drink


def test_beginner_validator_accepts_valid_fruit_drink():
    ingredients = [
        "jagermeister",
        "passion fruit juice",
        "mint",
        "crushed ice",
    ]

    assert validate_drink(ingredients) is True


def test_beginner_validator_requires_exactly_one_juice():
    assert validate_drink(["vodka", "ice cubes"]) is False


def test_beginner_validator_rejects_more_than_two_alcohols():
    ingredients = ["vodka", "rum", "gin", "orange juice"]

    assert validate_drink(ingredients) is False


def test_beginner_validator_rejects_unknown_ingredient():
    assert validate_drink(["rum", "mango juice"]) is False
