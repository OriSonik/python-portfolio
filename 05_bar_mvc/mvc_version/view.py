from .model import Drink


class BarView:
    def show_main_menu(self) -> str:
        print("\n=== SMALL BAR MVC ===")
        print("1. Show menu")
        print("2. Make an order")
        print("3. Show ingredients")
        print("0. Exit")
        return input("Your choice: ").strip().lower()

    def show_menu(self, menu: tuple[Drink, ...]) -> None:
        print("\n=== BAR MENU ===")
        for number, drink in enumerate(menu, start=1):
            print(f"{number}. {drink.name} - {drink.price:.2f} PLN")
            print("   " + ", ".join(drink.ingredients))

    def show_ingredient_catalog(
        self, catalog: dict[str, tuple[str, ...]]
    ) -> None:
        print("\n=== INGREDIENTS ===")
        for category, ingredients in catalog.items():
            print(f"{category}: " + ", ".join(ingredients))

    def ask_order_choice(self) -> str:
        print("\nEnter a drink number, N for a new drink or 0 to finish.")
        return input("Your choice: ").strip().lower()

    def ask_custom_ingredients(self) -> list[str]:
        text = input("Ingredients separated with commas: ").strip().lower()
        return [item.strip() for item in text.split(",") if item.strip()]

    def ask_drink_name(self) -> str:
        return input("Drink name: ").strip()

    def ask_save_to_menu(self) -> bool:
        return input("Save it for future orders? [y/n]: ").strip().lower() == "y"

    def show_message(self, message: str) -> None:
        print(message)

    def show_order(self, order: tuple[Drink, ...], total: float) -> None:
        print("\n=== YOUR ORDER ===")
        if not order:
            print("The order is empty.")
            return

        for drink in order:
            print(f"- {drink.name}: {drink.price:.2f} PLN")
        print(f"Total: {total:.2f} PLN")
