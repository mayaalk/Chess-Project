# Author: Mayaal Khan
# GitHub username: mayaalk
# Date: 6/9/24
# Description: This project creates atomic chess game where each piece moves to explode the king of the opposite team.


class ChessVar:
    def __init__(self):
        """"gives all ChessVar data members an initial value, including setting the initial board position and initial
        game state"""
        self.board = self.game_board()
        self.white_turn = True
        self.game_state = 'UNFINISHED'

    def game_board(self):
        """Sets up the game board by creating columns and rows and labeling chess pieces and returns
        a dictionary representing the board with positions as keys and pieces as values."""
        initial_board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        board = {}
        columns = 'abcdefgh'
        rows = '87654321'
        for r in range(8):
            for c in range(8):
                piece = initial_board[r][c]
                board[columns[c] + rows[r]] = piece if piece != '.' else None
        return board

    def get_game_state(self):
        """Returns the current state of the game."""
        return self.game_state

    def make_move(self, start, end):
        """This function correctly handles turn order (black or white) and handles making a move if valid."""
        if self.game_state != 'UNFINISHED':
            return False

        piece = self.board.get(start)
        if piece is None or (self.white_turn and piece.islower()) or (not self.white_turn and piece.isupper()):
            return False

        if not self.is_valid_move(start, end):
            return False

        captured = self.move_piece(start, end)
        self.remove_captured_pieces(captured)
        self.check_game_state()
        self.white_turn = not self.white_turn
        return True

    def is_valid_move(self, start, end):
        """Checks if a move from start to end is valid."""
        piece = self.board[start]
        target = self.board[end]

        # Ensure coordinates are within the valid range
        if start[0] not in 'abcdefgh' or start[1] not in '12345678' or end[0] not in 'abcdefgh' or end[
            1] not in '12345678':
            return False

        col_diff = abs(self.col_to_index(start[0]) - self.col_to_index(end[0]))
        row_diff = abs(int(start[1]) - int(end[1]))

        if piece.lower() == 'k':
            return col_diff <= 1 and row_diff <= 1 and (
                target is None or target.islower() if piece.isupper() else (target is None or target.isupper()))

        if piece.lower() == 'q':
            if start[0] == end[0] or start[1] == end[1] or col_diff == row_diff:
                return self.path_clear(start, end)

        if piece.lower() == 'r':
            if start[0] == end[0] or start[1] == end[1]:
                return self.path_clear(start, end)

        if (piece.lower() == 'b' and col_diff == row_diff):
            return self.path_clear(start, end)

        if piece.lower() == 'n':
            return (col_diff, row_diff) in [(1, 2), (2, 1)]

        if piece.lower() == 'x':
            if piece.isupper():
                if start[1] == '2' and end[1] == '4' and start[0] == end[0] and target is None:
                    return self.board[start[0] + '3'] is None
                return end[1] == str(int(start[1]) + 1) and (
                            start[0] == end[0] and target is None or col_diff == 1 and target and target.islower())
            else:
                if start[1] == '7' and end[1] == '5' and start[0] == end[0] and target is None:
                    return self.board[start[0] + '6'] is None
                return end[1] == str(int(start[1]) - 1) and (
                            start[0] == end[0] and target is None or col_diff == 1 and target and target.isupper())

        return False

    def col_to_index(self, col):
        """Converts a column letter to an index (0-7)."""
        return 'abcdefgh'.index(col)

    def path_clear(self, start, end):
        """This method checks if the path is clear for a piece to move from the start position to the end position."""
        start_col_idx = self.col_to_index(start[0])
        end_col_idx = self.col_to_index(end[0])
        col_diff = end_col_idx - start_col_idx
        row_diff = int(end[1]) - int(start[1])
        col_step = (col_diff and int(col_diff / abs(col_diff))) or 0
        row_step = (row_diff and int(row_diff / abs(row_diff))) or 0

        current_col_idx = start_col_idx + col_step
        current_row = int(start[1]) + row_step
        while current_col_idx != end_col_idx or current_row != int(end[1]):
            if self.board['abcdefgh'[current_col_idx] + str(current_row)] is not None:
                return False
            current_col_idx += col_step
            current_row += row_step
        return True

    def move_piece(self, start, end):
        """This method moves a piece from the start position to the end position."""
        captured = []
        if self.board[end] is not None:
            captured.append(end)
        self.board[end] = self.board[start]
        self.board[start] = None
        return captured

    def remove_captured_pieces(self, captured):
        """This method removes captured pieces after explosion from the board."""
        for square in captured:
            self.board[square] = None
            self.explode(square)

    def explode(self, square):
        """This method lead to an explosion the king and pieces near king."""
        col, row = square[0], int(square[1])
        for i in range(max(1, row - 1), min(9, row + 2)):
            for j in range(self.col_to_index(col) - 1, self.col_to_index(col) + 2):
                if 0 <= j < 8:  # Ensure column index is within valid range
                    pos = 'abcdefgh'[j] + str(i)
                    if pos != square and self.board.get(pos) and self.board[pos].lower() != 'x':
                        self.board[pos] = None

    def check_game_state(self):
        """This function checks the game state after moves and explosions."""
        white_king, black_king = False, False
        for square in self.board:
            piece = self.board[square]
            if piece == 'K':
                white_king = True
            elif piece == 'k':
                black_king = True
        if not white_king:
            self.game_state = 'BLACK_WON'
        elif not black_king:
            self.game_state = 'WHITE_WON'

    def print_board(self):
        """This function prints out the board."""
        for row in range(8, 0, -1):
            for col in 'abcdefgh':
                piece = self.board[col + str(row)]
                print(piece if piece else '.', end=' ')
            print()

# Example usage:
# game = ChessVar()
# print(game.make_move('d2', 'd4'))  # output True
# print(game.make_move('g7', 'g5'))  # output True
# print(game.make_move('c1', 'g5'))  # output True
# game.print_board()
# print(game.get_game_state())  # output UNFINISHED
