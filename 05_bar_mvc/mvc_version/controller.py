from .model import BarModel
from .view import BarView


class BarController:
    def __init__(self, model: BarModel, view: BarView):
        self.model = model
        self.view = view

    def run(self) -> None:
        while True:
            choice = self.view.show_main_menu()

            if choice == "1":
                self.view.show_menu(self.model.get_menu())
            elif choice == "2":
                self.make_order()
            elif choice == "3":
                self.view.show_ingredient_catalog(
                    self.model.get_ingredient_catalog()
                )
            elif choice == "0":
                self.view.show_message("See you next time!")
                return
            else:
                self.view.show_message("Incorrect option.")

    def make_order(self) -> None:
        while True:
            self.view.show_menu(self.model.get_menu())
            choice = self.view.ask_order_choice()

            if choice == "0":
                self.view.show_order(
                    self.model.get_order(), self.model.calculate_total()
                )
                return

            if choice == "n":
                self.create_custom_drink()
                continue

            try:
                drink = self.model.add_menu_drink_to_order(int(choice))
                self.view.show_message(f"{drink.name} was added to the order.")
            except ValueError:
                self.view.show_message("Enter a number, N or 0.")
            except IndexError as error:
                self.view.show_message(str(error))

    def create_custom_drink(self) -> None:
        self.view.show_ingredient_catalog(self.model.get_ingredient_catalog())
        ingredients = self.view.ask_custom_ingredients()
        name = self.view.ask_drink_name()
        save_to_menu = self.view.ask_save_to_menu()

        try:
            drink = self.model.create_custom_drink(
                name=name,
                ingredients=ingredients,
                save_to_menu=save_to_menu,
            )
            self.model.add_drink_to_order(drink)
            self.view.show_message(f"{drink.name} was added to the order.")
        except ValueError as error:
            self.view.show_message(str(error))
