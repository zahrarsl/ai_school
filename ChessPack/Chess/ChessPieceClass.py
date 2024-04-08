class ChessPiece:
    def __init__(self, color, symbol):
        """
        Initialize a chess piece with the given color and symbol.

        Args:
            color (str): The color of the chess piece (e.g., 'white' or 'black').
            symbol (str): The symbol representing the piece (e.g., '♚' for black king).

        Attributes:
            color (str): The color of the chess piece.
            symbol (str): The symbol representing the piece.
        """
        self.color = color
        self.symbol = symbol


class King(ChessPiece):
    """
    A class representing the king chess piece.

    Attributes:
        counter (int): Keeps track of the number of movements for the king (used for castling).
        check_board (CheckBoard): An object from the CheckBoard class to detect check conditions.
    """

    def __init__(self, color, symbol):
        super().__init__(color, symbol)
        self.counter = 0

    def move(self, board, start, end):
        """
        Validate whether a move is acceptable for the king.

        Args:
            board (list): The chessboard.
            start (tuple): The starting position (row, column).
            end (tuple): The ending position (row, column).

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        # Check conditions for castling
        if (
            self.counter == 0
            and abs(start[1] - end[1]) == 2
            and start[0] == end[0]
        ):
            return True
        # Check conditions for normal movement
        elif (
                (abs(start[0] - end[0]) == 1 and start[1] == end[1])
                or (abs(start[1] - end[1]) == 1 and start[0] == end[0])
                or (abs(start[0] - end[0]) == 1 and abs(start[1] - end[1]) == 1)
        ):
            return True
        else:
            return False      

class Queen(ChessPiece):
    """
    A class representing the queen chess piece.

    Attributes:
        None

    Methods: 
        validate_move
        move
    """

    def validate_move(self, start, end):
        """
        Validate whether a move is acceptable for the queen based on the queen movement logic 

        Args:
            start (tuple): The starting position (row, column).
            end (tuple): The ending position (row, column).

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if abs(end[0] - start[0]) == abs(end[1] - start[1]):
            return True
        elif start[1] == end[1]:
            return True
        elif start[0] == end[0]:
            return True
        else:
            return False

    def move(self, board, start, end):
        """
        Check the path of move to be free of pieces

        Args:
            board (list): The chessboard.
            start (tuple): The starting position (row, column).
            end (tuple): The ending position (row, column).

        Returns:
            bool: True if the move is possible, False otherwise.
        """
        if not self.validate_move(start, end):
            return False

        # Check path for obstacles
        step_row = -1 if start[0] > end[0] else 1 if start[0] < end[0] else 0
        step_col = -1 if start[1] > end[1] else 1 if start[1] < end[1] else 0

        row, col = start[0] + step_row, start[1] + step_col
        while row != end[0] or col != end[1]:
            if board[row][col]:
                return False

            row += step_row
            col += step_col
        return True
  

class Rook(ChessPiece):
    """
    A class representing the rook chess piece.

    Attributes:
        counter (int): Keeps track of the number of movements for the rook (used for castling).
        promote (bool): Indicates whether the rook was promoted from a pawn (affects castling).
    """

    def __init__(self, color, symbol):
        super().__init__(color, symbol)
        #To count the number of movement for rook. we need this attribute for castling
        self.counter = 0
        #this attribute is used for castling. if the rook was a pawn promoted, we can't do castling
        self.promote = False   

    """
    Check whether the path between start and end positions is clear for the rook.

    Args:
        board (list): The chessboard.
        start (tuple): The starting position (row, column).
        end (tuple): The ending position (row, column).

    Returns:
        bool: True if the path is clear, False if there are obstacles.
    """
    
    def check_path(self, board, start, end):
        max_col = max (start[1], end[1])
        max_row = max (start[0], end[0])
        min_col = min (start[1], end[1])
        min_row = min (start[0], end[0])
        if start[0] == end[0]:
            for cell in range(min_col + 1, max_col):
                if board[start[0]][cell]:
                    return False
            else:
                return True
        elif start[1] == end[1]:
            for cell in range(min_row + 1, max_row):
                if board[cell][start[1]]:
                    return False
            else:
                return True

    def move(self, board, start, end):
        
        if (start[0] == end[0] or start[1] == end[1]) and self.check_path(board, start, end):
            return True
        else:
            return False 
        

class Bishop(ChessPiece):
    """
    A class representing the bishop chess piece.

    Attributes:
        None

    Methods:
        check_path 
        move    
    """
   # Check if the path is empty
    def check_path(self, board, start, end):
        dr = end[0] - start[0]
        dc = end[1] - start[1]

        # Determining the direction of vertical movement        
        if dr > 0: r_sign = 1 
        else: r_sign = -1

        # Determining the direction of horizontal movement
        if dc > 0: c_sign = 1 
        else: c_sign = -1 

        # Checking that all the squares in line with the destination square are empty
        for step in range(1, abs(dr)):
            row = start[0] + step * r_sign
            col = start[1] + step * c_sign
            if board[row][col]:
                return False
        return True
    
    def move(self, board, start, end):

        # Movement is allowed if the row and column distance of the origin and destination squares are equal 
        if abs(end[0] - start[0]) != abs(end[1] - start[1]):
            return False
        
        return self.check_path(board, start, end)


class Knight(ChessPiece):
    """ 
        A class representing the Knight chess piece.
        Methods:
            move
    """
    # Knight's movement logic
    def move(self, board, start, end):
        if (abs(start[1] - end[1]) == 1 and abs(start[0] - end[0]) == 2) or (abs(start[0] - end[0]) == 1 and abs(start[1] - end[1]) == 2):
            return True
        else:
            return False   


class Pawn(ChessPiece):

    # Pawn's movement logic
    def move(self, board, start, end, EnPassant_previous_move):
        capture = False     # Specifying the move along with capturing the opponent's piece to send to the move_piece method
        EnPassant = False

    # Move one square forward
        if self.color == "white":
            dir = -1        # The white pawn moves upwards
            start_row = 6   # The white pawn first location
        else:
            dir = 1         # The black pawn moves downwards
            start_row = 1   # The black pawn first location

        dr = end[0] - start[0] 
        dc = abs(end[1] - start[1])

        # Checking the permitted direction of movement and the difference between the origin and destination columns and rows
        if dr * dir < 0 or abs(dr) > 2 or dc > 1:
            return False, capture, EnPassant
        if dc == 1:
            if abs(dr) == 0:
                return False, capture, EnPassant 

        # Check if the destination square is not empty and the movement is not capturing
        if board[end[0]][end[1]] and dc == 0:
            return False, capture, EnPassant

    # Move two squares forward
        if dr == 2 * dir:
            # This movement is valid only in first move
            if start[0] == start_row:
                # check if it is the first move and the emptiness of the middle square
                if dc != 0 or board[start[0] + dir][start[1]]:
                    return False, capture, EnPassant
            else:
                return False, capture, EnPassant  

    # Diagonal movement along with capturing the opponent's piece (EnPassant or usual)
        if dc == 1 and dir == dr:
            capture = True

            # Is the destination square empty of any pieces?
            if board[end[0]][end[1]] is None:

                # Check for EnPassant possibility
                if EnPassant_previous_move[0]:
                    previous_pawn_row, previous_pawn_col = EnPassant_previous_move[1]

                    if (
                        board[previous_pawn_row][previous_pawn_col].color != self.color
                        and (
                            (board[previous_pawn_row][previous_pawn_col].color == "white" and previous_pawn_row == 4)
                            or (board[previous_pawn_row][previous_pawn_col].color == "black" and previous_pawn_row == 3)
                        )
                        and abs(start[1] - previous_pawn_col) == 1
                        and start[0] == previous_pawn_row
                        and end[1] == previous_pawn_col
                    ):
                        EnPassant = True
                    else:
                        return False, capture, EnPassant                       

                else:
                    return False, capture, EnPassant
                
            # Is the piece located in the destination square the opponent's piece?    
            elif board[end[0]][end[1]].color == self.color:
                return False, capture, EnPassant               

        # All conditions are met, so movement is valid
        return True, capture, EnPassant
