from pathlib import Path

from mvc_version.controller import BarController
from mvc_version.model import BarModel
from mvc_version.view import BarView


def main() -> None:
    menu_file = Path(__file__).with_name("bar_menu.csv")
    controller = BarController(BarModel(menu_file), BarView())
    controller.run()


if __name__ == "__main__":
    main()
