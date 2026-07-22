import csv
from dataclasses import dataclass
from pathlib import Path

ALCOHOLS = {
    "vodka", "rum", "gin", "tequila", "whisky", "aperol",
    "becherovka", "jagermeister", "prosecco", "red wine", "white wine"
}
JUICES = {
    "orange juice", "apple juice", "pineapple juice", "cranberry juice",
    "passion fruit juice", "lime juice", "lemon juice"
}
EXTRAS = {"mint", "lime", "lemon", "sugar", "cinnamon"}
MIXERS = {
    "water", "sparkling water", "tonic", "soda", "cola",
    "ginger beer", "ice cubes", "crushed ice"
}

INGREDIENT_CATALOG = {
    "Alcohols": ALCOHOLS,
    "Juices": JUICES,
    "Extras": EXTRAS,
    "Mixers and ice": MIXERS,
}


@dataclass(frozen=True)
class Drink:
    name: str
    price: float
    ingredients: tuple[str, ...]


class BarModel:
    def __init__(self, menu_file: Path):
        self.menu_file = Path(menu_file)
        self.menu: list[Drink] = []
        self.order: list[Drink] = []
        self.load_menu()

    def load_menu(self) -> None:
        self.menu.clear()

        try:
            with self.menu_file.open(newline="", encoding="utf-8") as file:
                for row in csv.DictReader(file):
                    self.menu.append(
                        Drink(
                            name=row["name"].strip(),
                            price=float(row["price"]),
                            ingredients=tuple(
                                ingredient.strip().lower()
                                for ingredient in row["ingredients"].split("|")
                                if ingredient.strip()
                            ),
                        )
                    )
        except FileNotFoundError as error:
            raise FileNotFoundError(
                f"Menu file was not found: {self.menu_file}"
            ) from error

    def get_menu(self) -> tuple[Drink, ...]:
        return tuple(self.menu)

    def get_ingredient_catalog(self) -> dict[str, tuple[str, ...]]:
        return {
            category: tuple(sorted(ingredients))
            for category, ingredients in INGREDIENT_CATALOG.items()
        }

    def validate_ingredients(self, ingredients: list[str]) -> tuple[bool, str]:
        normalized = [ingredient.strip().lower() for ingredient in ingredients]
        known_ingredients = ALCOHOLS | JUICES | EXTRAS | MIXERS
        unknown = [item for item in normalized if item not in known_ingredients]

        if unknown:
            return False, "Unknown ingredients: " + ", ".join(unknown)
        if len(normalized) != len(set(normalized)):
            return False, "The same ingredient cannot be added more than once."

        alcohol_count = sum(item in ALCOHOLS for item in normalized)
        juice_count = sum(item in JUICES for item in normalized)
        extra_count = sum(item in EXTRAS for item in normalized)
        mixer_count = sum(item in MIXERS for item in normalized)

        if juice_count != 1:
            return False, "A new drink must contain exactly one juice."
        if not 1 <= alcohol_count <= 2:
            return False, "A new drink must contain one or two alcohols."
        if extra_count > 1:
            return False, "A new drink can contain only one extra."
        if mixer_count > 2:
            return False, "A new drink can contain up to two mixers or ice options."

        return True, "The ingredient set is valid."

    def create_custom_drink(
        self,
        name: str,
        ingredients: list[str],
        save_to_menu: bool,
        price: float = 25.0,
    ) -> Drink:
        clean_name = name.strip()
        normalized = [ingredient.strip().lower() for ingredient in ingredients]
        is_valid, message = self.validate_ingredients(normalized)

        if not is_valid:
            raise ValueError(message)
        if not clean_name:
            raise ValueError("The drink must have a name.")
        if any(drink.name.casefold() == clean_name.casefold() for drink in self.menu):
            raise ValueError("A drink with this name already exists.")
        if price <= 0:
            raise ValueError("The price must be greater than zero.")

        drink = Drink(clean_name, price, tuple(normalized))

        if save_to_menu:
            self.save_drink(drink)
            self.menu.append(drink)

        return drink

    def save_drink(self, drink: Drink) -> None:
        with self.menu_file.open("a", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow(
                [drink.name, f"{drink.price:.2f}", "|".join(drink.ingredients)]
            )

    def add_menu_drink_to_order(self, menu_number: int) -> Drink:
        if not 1 <= menu_number <= len(self.menu):
            raise IndexError("There is no drink with this number.")

        drink = self.menu[menu_number - 1]
        self.order.append(drink)
        return drink

    def add_drink_to_order(self, drink: Drink) -> None:
        self.order.append(drink)

    def get_order(self) -> tuple[Drink, ...]:
        return tuple(self.order)

    def calculate_total(self) -> float:
        return sum(drink.price for drink in self.order)
