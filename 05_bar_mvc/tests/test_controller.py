import csv

from mvc_version.controller import BarController
from mvc_version.model import BarModel


class FakeView:
    def __init__(self):
        self.main_choices = []
        self.order_choices = []
        self.messages = []
        self.shown_menus = []
        self.shown_orders = []
        self.catalog_was_shown = False
        self.custom_ingredients = []
        self.custom_name = ""
        self.save_custom = False

    def show_main_menu(self):
        return self.main_choices.pop(0)

    def show_menu(self, menu):
        self.shown_menus.append(menu)

    def show_ingredient_catalog(self, catalog):
        self.catalog_was_shown = True

    def ask_order_choice(self):
        return self.order_choices.pop(0)

    def ask_custom_ingredients(self):
        return self.custom_ingredients

    def ask_drink_name(self):
        return self.custom_name

    def ask_save_to_menu(self):
        return self.save_custom

    def show_message(self, message):
        self.messages.append(message)

    def show_order(self, order, total):
        self.shown_orders.append((order, total))


def create_controller(tmp_path):
    menu_file = tmp_path / "bar_menu.csv"
    with menu_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "price", "ingredients"])
        writer.writerow(["Mojito", "28.00", "rum|lime juice|mint|soda|crushed ice"])

    model = BarModel(menu_file)
    view = FakeView()
    return BarController(model, view), model, view


def test_controller_can_show_menu_and_exit(tmp_path):
    controller, model, view = create_controller(tmp_path)
    view.main_choices = ["1", "0"]

    controller.run()

    assert view.shown_menus == [model.get_menu()]
    assert view.messages[-1] == "See you next time!"


def test_controller_adds_selected_menu_drink_and_shows_order(tmp_path):
    controller, model, view = create_controller(tmp_path)
    view.order_choices = ["1", "0"]

    controller.make_order()

    assert model.get_order()[0].name == "Mojito"
    assert view.shown_orders[0][1] == 28.0


def test_controller_creates_custom_drink_and_adds_it_to_order(tmp_path):
    controller, model, view = create_controller(tmp_path)
    view.custom_name = "Forest Passion"
    view.custom_ingredients = [
        "jagermeister",
        "passion fruit juice",
        "mint",
        "crushed ice",
    ]

    controller.create_custom_drink()

    assert model.get_order()[0].name == "Forest Passion"
    assert view.catalog_was_shown is True
    assert view.messages[-1] == "Forest Passion was added to the order."


def test_controller_reports_custom_drink_validation_error(tmp_path):
    controller, model, view = create_controller(tmp_path)
    view.custom_name = "Broken"
    view.custom_ingredients = ["vodka", "ice cubes"]

    controller.create_custom_drink()

    assert model.get_order() == ()
    assert "exactly one juice" in view.messages[-1]
