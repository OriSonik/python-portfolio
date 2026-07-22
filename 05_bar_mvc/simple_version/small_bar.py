import csv

MENU_FILE = "bar_menu.csv"

alcohols = [
    "vodka", "rum", "gin", "tequila", "whisky", "aperol",
    "becherovka", "jagermeister", "prosecco", "red wine", "white wine"
]
juices = [
    "orange juice", "apple juice", "pineapple juice", "cranberry juice",
    "passion fruit juice", "lime juice", "lemon juice"
]
extras = ["mint", "lime", "lemon", "sugar", "cinnamon"]
mixers = [
    "water", "sparkling water", "tonic", "soda", "cola",
    "ginger beer", "ice cubes", "crushed ice"
]


def load_menu():
    menu = []
    try:
        with open(MENU_FILE, newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                menu.append({
                    "name": row["name"],
                    "price": float(row["price"]),
                    "ingredients": row["ingredients"].split("|")
                })
    except FileNotFoundError:
        print("Menu file was not found.")
    return menu


def show_menu(menu):
    print("\n=== SMALL BAR MENU ===")
    for number, drink in enumerate(menu, start=1):
        print(f'{number}. {drink["name"]} - {drink["price"]:.2f} PLN')
        print("   " + ", ".join(drink["ingredients"]))


def show_ingredients():
    print("\nAvailable ingredients:")
    print("Alcohols: " + ", ".join(alcohols))
    print("Juices: " + ", ".join(juices))
    print("Extras: " + ", ".join(extras))
    print("Mixers and ice: " + ", ".join(mixers))


def validate_drink(ingredients):
    alcohol_count = 0
    juice_count = 0
    extra_count = 0
    mixer_count = 0

    for ingredient in ingredients:
        if ingredient in alcohols:
            alcohol_count += 1
        elif ingredient in juices:
            juice_count += 1
        elif ingredient in extras:
            extra_count += 1
        elif ingredient in mixers:
            mixer_count += 1
        else:
            print("Unknown ingredient: " + ingredient)
            return False

    if juice_count != 1:
        print("A new drink must contain exactly one juice.")
        return False
    if alcohol_count < 1 or alcohol_count > 2:
        print("A new drink must contain one or two alcohols.")
        return False
    if extra_count > 1:
        print("A new drink can contain only one extra.")
        return False
    if mixer_count > 2:
        print("A new drink can contain up to two mixers or ice options.")
        return False
    return True


def save_drink(drink):
    try:
        with open(MENU_FILE, "a", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow([
                drink["name"], drink["price"], "|".join(drink["ingredients"])
            ])
        print("The new drink was saved in the menu.")
    except PermissionError:
        print("The menu file cannot be changed.")


def create_new_drink(menu):
    show_ingredients()
    text = input("\nEnter ingredients separated with commas: ").lower()
    ingredients = []

    for part in text.split(","):
        if part.strip() != "":
            ingredients.append(part.strip())

    if validate_drink(ingredients) is False:
        print("This combination cannot be added.")
        return None

    name = input("Drink name: ").strip()
    if name == "":
        print("The drink must have a name.")
        return None

    for drink in menu:
        if drink["name"].lower() == name.lower():
            print("A drink with this name already exists.")
            return None

    new_drink = {"name": name, "price": 25.00, "ingredients": ingredients}
    if input("Save it for future orders? [y/n]: ").lower() == "y":
        save_drink(new_drink)
        menu.append(new_drink)
    return new_drink


def show_order(order):
    print("\n=== YOUR ORDER ===")
    if len(order) == 0:
        print("The order is empty.")
        return

    total = 0
    for drink in order:
        print(f'- {drink["name"]}: {drink["price"]:.2f} PLN')
        total += drink["price"]
    print(f"Total: {total:.2f} PLN")


def make_order(menu):
    order = []
    while True:
        show_menu(menu)
        print("\nEnter a drink number, N for a new drink or 0 to finish.")
        choice = input("Your choice: ").lower()

        if choice == "0":
            break
        elif choice == "n":
            new_drink = create_new_drink(menu)
            if new_drink is not None:
                order.append(new_drink)
                print(new_drink["name"] + " was added to the order.")
        else:
            try:
                number = int(choice)
                if number >= 1 and number <= len(menu):
                    order.append(menu[number - 1])
                    print(menu[number - 1]["name"] + " was added to the order.")
                else:
                    print("There is no drink with this number.")
            except ValueError:
                print("Enter a number, N or 0.")
    show_order(order)


def main():
    menu = load_menu()
    if len(menu) == 0:
        return

    while True:
        print("\n=== SMALL BAR ===")
        print("1. Show menu\n2. Make an order\n3. Show ingredients\n0. Exit")
        choice = input("Your choice: ")

        if choice == "1":
            show_menu(menu)
        elif choice == "2":
            make_order(menu)
        elif choice == "3":
            show_ingredients()
        elif choice == "0":
            print("See you next time!")
            break
        else:
            print("Incorrect option.")


if __name__ == "__main__":
    main()
