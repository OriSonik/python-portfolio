import random


class TicTacToeGame:
    ROWS = "ABC"
    COLUMNS = "123"

    WIN_LINES = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

    def __init__(self):
        self.board = [" " for _ in range(9)]

    def reset_board(self):
        self.board = [" " for _ in range(9)]

    def render_board(self):
        print()
        print("     1   2   3")
        print("   +---+---+---+")

        for row_index, row_name in enumerate(self.ROWS):
            start = row_index * 3
            row = self.board[start:start + 3]
            print(f" {row_name} | {row[0]} | {row[1]} | {row[2]} |")
            print("   +---+---+---+")

        print()

    def parse_move(self, user_input):
        cleaned_input = user_input.strip().upper()

        if cleaned_input == "Q":
            return "quit"

        if len(cleaned_input) != 2:
            return None

        first, second = cleaned_input

        if first in self.ROWS and second in self.COLUMNS:
            row = self.ROWS.index(first)
            column = self.COLUMNS.index(second)
            return row * 3 + column

        if first in self.COLUMNS and second in self.ROWS:
            row = self.ROWS.index(second)
            column = self.COLUMNS.index(first)
            return row * 3 + column

        return None

    def is_valid_move(self, move):
        return isinstance(move, int) and 0 <= move <= 8 and self.board[move] == " "

    def make_move(self, move, marker):
        if self.is_valid_move(move):
            self.board[move] = marker
            return True

        return False

    def available_moves(self):
        return [index for index, field in enumerate(self.board) if field == " "]

    def check_winner(self):
        for first, second, third in self.WIN_LINES:
            if (
                self.board[first] != " "
                and self.board[first] == self.board[second] == self.board[third]
            ):
                return self.board[first]

        return None

    def is_draw(self):
        return not self.available_moves() and self.check_winner() is None

    def get_human_move(self, player_name):
        while True:
            user_input = input(
                f"{player_name}, choose a field like A1, B2 or 3C. Press Q to quit: "
            )
            move = self.parse_move(user_input)

            if move == "quit":
                return "quit"

            if self.is_valid_move(move):
                return move

            print("Invalid move. The board refuses your offer.")

    def get_random_ai_move(self):
        return random.choice(self.available_moves())

    def find_tactical_move(self, marker):
        for move in self.available_moves():
            self.board[move] = marker

            if self.check_winner() == marker:
                self.board[move] = " "
                return move

            self.board[move] = " "

        return None

    def get_smart_ai_move(self, ai_marker, opponent_marker):
        winning_move = self.find_tactical_move(ai_marker)
        if winning_move is not None:
            return winning_move

        blocking_move = self.find_tactical_move(opponent_marker)
        if blocking_move is not None:
            return blocking_move

        center = 4
        if self.is_valid_move(center):
            return center

        corners = [0, 2, 6, 8]
        available_corners = [move for move in corners if self.is_valid_move(move)]
        if available_corners:
            return random.choice(available_corners)

        sides = [1, 3, 5, 7]
        available_sides = [move for move in sides if self.is_valid_move(move)]
        if available_sides:
            return random.choice(available_sides)

        return self.get_random_ai_move()

    def play_two_players(self):
        self.reset_board()
        current_marker = "X"

        while True:
            self.render_board()
            move = self.get_human_move(f"Player {current_marker}")

            if move == "quit":
                print("Game cancelled. The board will remember this.")
                return None

            self.make_move(move, current_marker)

            winner = self.check_winner()
            if winner:
                self.render_board()
                print(f"Player {winner} wins!")
                return winner

            if self.is_draw():
                self.render_board()
                print("It's a draw. The board remains undefeated.")
                return "draw"

            current_marker = "O" if current_marker == "X" else "X"

    def play_against_ai(self, smart_ai=False):
        self.reset_board()
        human_marker = "X"
        ai_marker = "O"
        current_marker = "X"

        while True:
            self.render_board()

            if current_marker == human_marker:
                move = self.get_human_move("Player X")

                if move == "quit":
                    print("Game cancelled. The machine accepts your tactical retreat.")
                    return None

            else:
                if smart_ai:
                    move = self.get_smart_ai_move(ai_marker, human_marker)
                    print("Computer chooses its move. Suspiciously confident.")
                else:
                    move = self.get_random_ai_move()
                    print("Computer chooses its move. Chaos has entered the board.")

            self.make_move(move, current_marker)

            winner = self.check_winner()
            if winner:
                self.render_board()

                if winner == human_marker:
                    print("You win!")
                else:
                    print("Computer wins!")

                return winner

            if self.is_draw():
                self.render_board()
                print("It's a draw. Nobody gets the crown today.")
                return "draw"

            current_marker = "O" if current_marker == "X" else "X"

    def play_wimbledon_mode_against_smart_ai(self):
        human_score = 0
        ai_score = 0

        while human_score < 3 and ai_score < 3:
            print()
            print("=== WIMBLEDON MODE ===")
            print(f"Score: Player {human_score} - {ai_score} Computer")
            print("First side to win 3 games takes the match.")
            print()

            result = self.play_against_ai(smart_ai=True)

            if result is None:
                return

            if result == "X":
                human_score += 1
            elif result == "O":
                ai_score += 1

        print()
        print("=== MATCH RESULT ===")
        print(f"Final score: Player {human_score} - {ai_score} Computer")

        if human_score == 3:
            print("You win the Wimbledon mode match!")
        else:
            print("Computer wins the Wimbledon mode match!")

    def print_rules(self):
        print()
        print("=== HOW TO PLAY ===")
        print("Choose fields using coordinates: A1, A2, A3, B1... C3.")
        print("You can also type coordinates backwards, for example 1A or 3C.")
        print("Three identical marks in a row, column or diagonal win the game.")
        print("Press Q during move selection to quit the current game.")
        print()

    def run_menu(self):
        while True:
            print()
            print("=== TIC TAC TOE ===")
            print("1. Two players")
            print("2. Player vs random computer")
            print("3. Player vs smart computer")
            print("4. Wimbledon mode: 3-set-win match: Player vs smart computer")
            print("5. How to play")
            print("6. Quit")
            print()

            choice = input("Choose option: ").strip()

            if choice == "1":
                self.play_two_players()
            elif choice == "2":
                self.play_against_ai(smart_ai=False)
            elif choice == "3":
                self.play_against_ai(smart_ai=True)
            elif choice == "4":
                self.play_wimbledon_mode_against_smart_ai()
            elif choice == "5":
                self.print_rules()
            elif choice == "6":
                print("Goodbye. The grid goes silent.")
                break
            else:
                print("Invalid option. Even chaos needs a menu number.")


if __name__ == "__main__":
    game = TicTacToeGame()
    game.run_menu()