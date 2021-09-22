# Author: Neil Nautiyal
# Date: 8/2/21
# Description: Writing a class named QuoridorGame (and additional classes for playing a board game called Quoridor)

class QuoridorGame:
    """
    Class that initializes the board, keeps track of the rules, and the win state
    Calls Pawn and fence classes in its implementation
    """
    def __init__(self):
        """Initializes the game board, everything on it, and the game state"""
        self._p1 = Pawn1()  # initializes player 1's pawn
        self._p2 = Pawn2()  # initializes player 2's pawn
        self._current_player = self._p1  # initializes first player to be p1
        self._board = [[" ", " ", " ", " ", "P1", " ", " ", " ", " "],  # stores information about the game board
                       [" ", " ", " ", " ", " ",  " ", " ", " ", " "],  # stores information about pawns and fences
                       [" ", " ", " ", " ", " ",  " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ",  " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ",  " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ",  " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ",  " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ",  " ", " ", " ", " "],
                       [" ", " ", " ", " ", "P2", " ", " ", " ", " "]]

    def move_pawn(self, player, coordinates):
        """Allows the pawn to make a move -- calls move_pawn method within the pawn class"""
        new_x, new_y = coordinates  # separates x and y coordinates from the tuple so they can be accessed separately
        if not self.check_move_pawn(player, coordinates):  # checks if pawn move is valid
            return False
        else:  # if the move is valid...
            if player == 1:
                if self._board[new_y][new_x] == " ":  # if moving to an empty space...
                    self._board[new_y][new_x] = "P1"  # set it equal to the pawn identifier
                else:
                    self._board[new_y][new_x] += "P1"   # if moving to a space with fences, append it to cell
                old_x, old_y = self._p1.get_position()  # making each coordinate accessible
                self._board[old_y][old_x] = self._board[old_y][old_x].replace("P1", "")  # remove pawn from OG cell
                self._p1.set_position(coordinates)  # setting new coordinates in pawn object
            if player == 2:  # same as above but for P2 instead of P1
                if self._board[new_y][new_x] == " ":
                    self._board[new_y][new_x] = "P2"
                else:
                    self._board[new_y][new_x] += "P2"
                old_x, old_y = self._p2.get_position()
                self._board[old_y][old_x] = self._board[old_y][old_x].replace("P2", "")
                self._p2.set_position(coordinates)
            self.change_turn()  # changes turn if the move is valid and pawn was moved
            return True

    def check_move_pawn(self, player, coordinates):
        """Checks if pawn move is valid"""
        new_x_co, new_y_co = coordinates  # pulling out coordinates so they can be used to index into the board
        x_co, y_co = self._current_player.get_position()  # takes starting position for the current pawn
        if (  # return false if...
            (self._current_player.get_player_num() != player) or  # player making move is not current player
            (self.is_winner(1) or self.is_winner(2) is True) or  # there is a winner already
            (new_x_co < 0 or new_x_co > 8) or (new_y_co < 0 or new_y_co > 8) or  # move is out of bounds
            ("P" in self._board[new_y_co][new_x_co]) or  # space is occupied
                (abs(new_x_co - x_co) > 2) or (abs(new_y_co - y_co) > 2)):  # move is greater than 2
            return False
        else:
            if (abs(new_x_co - x_co) == 1 and new_y_co == y_co) or (abs(new_y_co - y_co) == 1 and new_x_co == x_co):
                return self.check_move_pawn_standard(new_x_co, new_y_co, x_co, y_co)  # checks if standard move is valid
            if (abs(new_x_co - x_co) == 2 and new_y_co == y_co) or (abs(new_y_co - y_co) == 2 and new_x_co == x_co):
                return self.check_move_pawn_jump(new_x_co, new_y_co, x_co, y_co)  # checks if jump move is valid
            if abs(new_x_co - x_co) == abs(new_y_co - y_co):
                return self.check_move_pawn_diagonal(new_x_co, new_y_co, x_co, y_co)  # checks if diagonal move is valid

    def check_move_pawn_standard(self, new_x_co, new_y_co, x_co, y_co):
        """Validates a move that is orthogonal (up, down, left, right) by one space"""
        # if move is UP and current coordinates have a h fence:
        if (new_x_co == x_co and new_y_co == y_co - 1) and ("h" in self._board[y_co][x_co]):
            return False
        # if move is LEFT and current coordinates have a v fence:
        if (new_y_co == y_co and new_x_co == x_co - 1) and ("v" in self._board[y_co][x_co]):
            return False
        # if move is DOWN and new coordinates have a h fence:
        if (new_x_co == x_co and new_y_co == y_co + 1) and ("h" in self._board[new_y_co][new_x_co]):
            return False
        # if move is RIGHT and new coordinates have a v fence:
        if (new_y_co == y_co and new_x_co == x_co + 1) and ("v" in self._board[new_y_co][new_x_co]):
            return False
        return True

    def check_move_pawn_jump(self, new_x_co, new_y_co, x_co, y_co):
        """Checks a move that jumps another pawn"""
        # if move is UP x2 (jumping pawn above), return false if space to jump has h fence
        if new_x_co == x_co and new_y_co == y_co - 2:
            if "h" in self._board[y_co][x_co]:  # checks if adjacent space has a fence
                return False
            else:
                if "P" not in self._board[y_co - 1][x_co]:  # checks that a player is being jumped
                    return False
                else:
                    if "h" in self._board[y_co - 1][x_co]:  # checks if a fence is behind player to be jumped
                        return False
                    else:
                        return True
        # if move is DOWN x2 (jumping pawn below), return false if space below space to jump has h fence
        elif new_x_co == x_co and new_y_co == y_co + 2:
            if "h" in self._board[y_co + 1][x_co]:  # checks if adjacent space has a fence
                return False
            else:
                if "P" not in self._board[y_co + 1][x_co]:  # checks that a player is being jumped
                    return False
                else:
                    if "h" in self._board[new_y_co][new_x_co]:  # checks if a fence is behind player to be jumped
                        return False
                    else:
                        return True

    def check_move_pawn_diagonal(self, new_x_co, new_y_co, x_co, y_co):
        """Checks a move that is diagonal to see if it is valid"""
        # if move is UP+RIGHT or UP+LEFT
        if ((new_x_co == x_co - 1 or new_x_co == x_co + 1) and new_y_co == y_co - 1) \
                and ("P" in self._board[y_co - 1][x_co] and "h" in self._board[y_co - 1][x_co]):
            return True  # if there is a player and a fence above the current player's position, return True
        # elif move is DOWN+RIGHT OR DOWN+LEFT
        elif ((new_x_co == x_co - 1 or new_x_co == x_co + 1) and new_y_co == y_co + 1) \
                and ("P" in self._board[y_co + 1][x_co] and (y_co + 2 > 8 or "h" in self._board[y_co + 2][x_co])):
            return True
        # else return False
        else:  # if there is a player under the pawn attempting to make a diag move, and a h fence under that, return T.
            return False

    def place_fence(self, player, orientation, coordinates):
        """Places a fence on the board"""
        x_co, y_co = coordinates  # Assigns coordinate values to separate variables
        if not self.check_place_fence(player, orientation, coordinates):  # separate function checks if move is valid
            return False
        else:  # otherwise...
            self._current_player.add_fence(orientation + str(coordinates))  # adds fence to player's placed fence list
            if self._board[y_co][x_co] == " ":
                self._board[y_co][x_co] = orientation  # if string has whitespace, set equal to the fence orientation
            else:
                self._board[y_co][x_co] += orientation  # otherwise append it to existing string
            self.change_turn()  # changes turn
            return True

    def check_place_fence(self, player, orientation, coordinates):
        """Checks if place_fence is valid"""
        x_co, y_co = coordinates
        if ((orientation == 'v' and x_co == 0) or  # no vertical fences on left most spaces
            (orientation == 'h' and y_co == 0) or  # no horizontal fences on top most spaces
            (self._current_player.get_player_num() != player) or  # if player making move is not current player
            (x_co < 0 or x_co > 8) or (y_co < 0 or y_co > 8) or  # if move is is beyond boundaries
            ((orientation + str(coordinates)) in self._p1.get_placed_fences()) or  # if fence of orientation is placed
            ((orientation + str(coordinates)) in self._p2.get_placed_fences()) or  # if fence of orientation is placed
            self.is_winner(self._p1.get_player_num()) is True or  # if a player has won
            self.is_winner(self._p2.get_player_num()) is True or  # if a player has won
                self._current_player.get_num_placed_fences() == 10):  # if a player has already placed 10 fences
            return False
        else:
            return True

    def change_turn(self):
        """Changes which player's turn it is"""
        if self._current_player == self._p1:  # if current player is player 1, change to player 2
            self._current_player = self._p2
        else:  # vice versa
            self._current_player = self._p1

    def is_winner(self, player):
        """Returns true if the player number passed has won"""
        if player == 1:
            for index in range(9):  # iterates through player 2's baseline/ starting row
                if "P1" in self._board[8][index]:  # if P1 is found...
                    return True
                else:
                    continue
            return False
        if player == 2:
            for index in range(9):  # iterates through player 1's baseline/ starting row
                if "P2" in self._board[0][index]:  # if P2 is found...
                    return True
                else:
                    continue
            return False

    def print_board(self):
        """prints game board"""
        for row in self._board:
            print(row)


class Pawn:
    """Initializes pawn objects that are placed and moved around the board
    Called by QuoridorGame Class"""
    def __init__(self):
        """Initializes a pawn"""
        self._placed_fences = []  # keeps track of each player's placed fences

    def add_fence(self, fence):
        """Adds passed fence type and coordinates to placed fences"""
        self._placed_fences.append(fence)

    def get_num_placed_fences(self):
        """Returns number of placed fences for pawn"""
        return len(self._placed_fences)

    def get_placed_fences(self):
        """Returns the list of placed fences by a pawn"""
        return self._placed_fences


class Pawn1(Pawn):
    """Pawn class for P1"""
    def __init__(self):
        """Initializes pawn 1's P1"""
        super().__init__()
        self._position = (4, 0)  # initializes starting position for P1

    def get_player_num(self):
        """Returns int used to reference pawn 1"""
        return 1

    def get_position(self):
        """Returns current position of P1"""
        return self._position

    def set_position(self, new_position):
        """Sets new position of P1"""
        self._position = new_position

    def __repr__(self):
        """Used to represent Pawn1 object"""
        return "P1"


class Pawn2(Pawn):
    """Pawn class for P2"""
    def __init__(self):
        """Initializes pawn 2's P2"""
        super().__init__()
        self._position = (4, 8)  # initializes starting position for P2

    def get_player_num(self):
        """Returns int used to reference pawn 2"""
        return 2

    def get_position(self):
        """Returns position of P2"""
        return self._position

    def set_position(self, new_position):
        """Sets new position of P2"""
        self._position = new_position

    def __repr__(self):
        """Used to represent Pawn2 object"""
        return "P2"


# TEST GAME BELOW
# q = QuoridorGame()
# print(q.move_pawn(1, (4,1)))
# q.print_board()
# print(q.move_pawn(2, (4,7)))
# q.print_board()
# print(q.move_pawn(1, (4,2)))
# q.print_board()
# print(q.move_pawn(2, (4,6)))
# q.print_board()
# print(q.move_pawn(1, (4,3)))
# q.print_board()
# print(q.move_pawn(2, (4,5)))
# q.print_board()
# print(q.move_pawn(1, (4,4)))
# q.print_board()
# print(q.place_fence(2, "h", (4,4)))
# q.print_board()
# print(q.move_pawn(1, (4,6)))
# q.print_board()
# print(q.place_fence(2, "v", (4,4)))
# q.print_board()
# print(q.move_pawn(1, (4,7)))
# q.print_board()
# print(q.is_winner(2))
# print(q.place_fence(2, "v", (8,4)))
# q.print_board()
# print(q.move_pawn(1, (4,8)))
# q.print_board()
# print(q.is_winner(2))
# print(q._p1.get_placed_fences(), "p1 fences")
# print(q._p2.get_placed_fences(), "p2 fences")
