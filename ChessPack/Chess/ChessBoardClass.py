from Chess.CheckBoardClass import CheckBoard
from Chess.ChessPieceClass import King
from Chess.ChessPieceClass import Queen
from Chess.ChessPieceClass import Rook
from Chess.ChessPieceClass import Knight
from Chess.ChessPieceClass import Bishop
from Chess.ChessPieceClass import Pawn


class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        # storing captured pieces
        self.white_captured_pieces = []
        self.black_captured_pieces = []

        # storing the EnPassant possibility and the position of the target pawn 
        self.EnPassant_previous_move = [False, [0, 0]]

        # Saving the moves to check that if there are five the same, a draw occurs
        # *** It has to be actually three same moves to declare a draw but in online games a draw is called after five repetitions
        self.moves = []

        # for counting consecutive moves where neither player has moved a pawn or captured a piece
        self.fifty_moves_count = 0

        # Place pieces on the board at first
        self.place_pieces()

        self.check_board = CheckBoard()


    # Place pieces on the board at first
    def place_pieces(self):
        self.board[7][0] = Rook("white", "♖")
        self.board[7][1] = Knight("white", "♘")
        self.board[7][2] = Bishop("white", "♗")
        self.board[7][3] = Queen("white", "♕")
        self.board[7][4] = King("white", "♔")
        self.board[7][5] = Bishop("white", "♗")
        self.board[7][6] = Knight("white", "♘")
        self.board[7][7] = Rook("white", "♖")
        for i in range(8):
            self.board[6][i] = Pawn("white", "♙")

        self.board[0][0] = Rook("black", "♜")
        self.board[0][1] = Knight("black", "♞")
        self.board[0][2] = Bishop("black", "♝")
        self.board[0][3] = Queen("black", "♛")
        self.board[0][4] = King("black", "♚")
        self.board[0][5] = Bishop("black", "♝")
        self.board[0][6] = Knight("black", "♞")
        self.board[0][7] = Rook("black", "♜")
        for i in range(8):
            self.board[1][i] = Pawn("black", "♟")

    # Move a piece on the board
    def move_any_pieces(self, start, end):
        piece = self.board[start[0]][start[1]]
        # if the piece is a pawn
        if isinstance(piece, Pawn):
            legal_move, capture, EnPassant = piece.move(self.board, start, end, self.EnPassant_previous_move)
            if legal_move and self.check_board.valid_movement(self.board, start, end, piece.color):
                # Reset the EnPassant boolean to be ready to update in the move_pawn method
                self.EnPassant_previous_move[0] = False
                # We are looking for fifty consecutive moves where neither player has moved a pawn or captured a piece to declare a draw, and every pawn move breaks this sequence
                self.fifty_moves_count = 0
                # store the move symbol with the end position as a str to use in five_same_moves method in CheckBoard class
                self.moves.append(self.board[start[0]][start[1]].symbol + str(end[0]) + str(end[1]))
                self.move_pawn(piece, start, end, capture, EnPassant)
                return True
            else:
                return False
            

        elif isinstance(piece, King):  # if the piece is king
            legal_move = piece.move(self.board, start, end)
            if legal_move and self.check_board.valid_movement(self.board, start, end, piece.color):
                # store the move symbol with the end position as a str to use in five_same_moves method in the CheckBoard class
                self.moves.append(self.board[start[0]][start[1]].symbol + str(end[0]) + str(end[1]))

                self.move_king(piece, start, end)
                piece.counter += 1
                return True
            else:
                return False
            
        elif isinstance(piece, Rook):
            legal_move = piece.move(self.board, start, end)
            if legal_move and self.check_board.valid_movement(self.board, start, end, piece.color):
                self.move_some_pieces(piece, start, end)
                piece.counter += 1
                return True
            else:
                return False 

        else: # other pieces 
            legal_move = piece.move(self.board, start, end)
            if legal_move and self.check_board.valid_movement(self.board, start, end, piece.color):
                if self.move_some_pieces(piece, start, end):
                    return True
                else:
                    return False
            else:
                return False
    
    def move_pawn(self, piece, start, end, capture, EnPassant):

        if end[0] == 7 and piece.color == "black":
            self.promote_pawn(start, "black", ['♛', '♜', '♞', '♝'])
        elif end[0] == 0 and piece.color == "white":
            self.promote_pawn(start, "white", ['♕', '♖', '♘', '♗'])
            
        if capture:
            if EnPassant:
                if piece.color == "white":
                    self.black_captured_pieces.append(self.board[self.EnPassant_previous_move[1][0]][self.EnPassant_previous_move[1][1]].symbol) 
                else:
                    self.white_captured_pieces.append(self.board[self.EnPassant_previous_move[1][0]][self.EnPassant_previous_move[1][1]].symbol)    
                self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
                self.board[start[0]][start[1]] = None
                self.board[self.EnPassant_previous_move[1][0]][self.EnPassant_previous_move[1][1]] = None  
            else:   
                if piece.color == "white": 
                    self.black_captured_pieces.append(self.board[end[0]][end[1]].symbol) 
                else:
                    self.white_captured_pieces.append(self.board[end[0]][end[1]].symbol)    
                self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
                self.board[start[0]][start[1]] = None    
        else:
            self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
            self.board[start[0]][start[1]] = None
            # The else block runs when the move is not a capture one. Then, if it is a two-square move, we can have En Passant in the next move with some conditions that will checked in Pawn's class.
            if abs(end[0] - start[0]) == 2: 
                self.EnPassant_previous_move[0] = True
                self.EnPassant_previous_move[1] = end 

    def move_some_pieces(self, piece, start, end):

        # store the move symbol with the end position as a str to use in five_same_moves method in the CheckBoard class
        self.moves.append(self.board[start[0]][start[1]].symbol + str(end[0]) + str(end[1]))

        if self.check_board.empty_square(self.board, end):
            self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
            self.board[start[0]][start[1]] = None

            # We are looking for fifty consecutive moves where neither player has moved a pawn or captured a piece to declare a draw and this move is counting in 
            self.fifty_moves_count += 1
            return True

        elif self.check_board.capture(self.board, piece.color, end):  
            if piece.color == "white":
                self.black_captured_pieces.append(self.board[end[0]][end[1]].symbol)
            else:
                self.white_captured_pieces.append(self.board[end[0]][end[1]].symbol)    
            self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
            self.board[start[0]][start[1]] = None 

            # We are looking for fifty consecutive moves where neither player has moved a pawn or captured a piece to declare a draw, and every capture breaks this sequence
            self.fifty_moves_count = 0
            return True
        else:
            return False

    def promote_pawn(self, start, color, symbols):
        new_piece = "new_piece"
        while new_piece.lower() not in ["queen", "rook", "knight", "bishop"]:
            new_piece = input(
                "Which piece would you like your pawn to become: queen, rook, knight, or bishop?"
            )
        if new_piece.lower() == "queen":
            self.board[start[0]][start[1]] = Queen(color, symbols[0])
        elif new_piece.lower() == "rook":
            self.board[start[0]][start[1]] = Rook(color, symbols[1])
            self.board[start[0]][start[1]].promote = True  # if the pawn promote to rook, we can't do castling
        elif new_piece.lower() == "knight":
            self.board[start[0]][start[1]] = Knight(color, symbols[2])
        else:
            self.board[start[0]][start[1]] = Bishop(color, symbols[3])

    # This function specifies that if the king's move is a castle,
    # it will determine the location of the king and rook, and if it is a normal move, it will return it.
    def move_king(self, piece, start, end):
        # First, we have to make sure that two kings are not together
        for row in range(8):
            for col in range(8):
                if (
                    isinstance(self.board[row][col], King)
                    and self.board[row][col].color != piece.color
                    and abs(end[0] - row) <= 1
                    and abs(end[1] - col) <= 1
                ):
                    return False 
                
        # Castling checks
        if abs(start[1] - end[1]) == 2:
            if (
                (start[1] - end[1]) < 0
                and self.check_board.empty_square(self.board, end)
                and self.check_board.empty_square(self.board, (end[0], min(start[1], end[1]) + 1))
                and not self.check_board.check(self.board, end, piece.color)
                and not self.check_board.check(self.board, (end[0], min(start[1], end[1]) + 1), piece.color)
                ):

             # if player wants to do castling with the right rook
                if (
                    piece.color == "white"
                    and isinstance(self.board[7][7], Rook)
                    and self.board[7][7].counter == 0
                    and not self.board[7][7].promote
                ):
                    self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
                    self.board[start[0]][start[1]] = None
                    self.board[end[0]][end[1] - 1] = self.board[7][7]
                    self.board[7][7] = None
                    self.fifty_moves_count += 1
                    return True

                elif (
                    piece.color == "black"
                    and isinstance(self.board[0][7], Rook)
                    and self.board[0][7].counter == 0
                    and not self.board[0][7].promote
                ):
                    self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
                    self.board[start[0]][start[1]] = None
                    self.board[end[0]][end[1] - 1] = self.board[0][7]
                    self.board[0][7] = None
                    self.fifty_moves_count += 1
                    return True
            elif (
                (start[1] - end[1]) > 0
                and self.check_board.empty_square(self.board, end)
                and self.check_board.empty_square(self.board, (end[0], min(start[1], end[1]) + 1))
                and not self.check_board.check(self.board, end, piece.color)
                and not self.check_board.check(self.board, (end[0], min(start[1], end[1]) + 1), piece.color)
                ):  # if player wants to do castling with the left rook
                if (
                    piece.color == "white"
                    and isinstance(self.board[7][0], Rook)
                    and self.board[7][0].counter == 0
                    and not self.board[7][0].promote
                ):
                    self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
                    self.board[start[0]][start[1]] = None
                    self.board[end[0]][end[1] + 1] = self.board[7][0]
                    self.board[7][0] = None
                    self.fifty_moves_count += 1
                    return True

                elif (
                    piece.color == "black"
                    and isinstance(self.board[0][0], Rook)
                    and self.board[0][0].counter == 0
                    and not self.board[7][0].promote
                ):
                    self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
                    self.board[start[0]][start[1]] = None
                    self.board[end[0]][end[1] + 1] = self.board[0][0]
                    self.board[0][0] = None
                    self.fifty_moves_count += 1
                    return True

        # Normal moves and captures
        else:
            if self.check_board.empty_square(self.board, end) and not self.check_board.check(self.board, end, piece.color):
                self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
                self.board[start[0]][start[1]] = None

                # We are looking for fifty consecutive moves where neither player has moved a pawn or captured a piece to declare a draw and this move is counting in 
                self.fifty_moves_count += 1
                return True

            elif self.check_board.capture(self.board, piece.color, end) and not self.check_board.check(self.board, end, piece.color):  
                if piece.color == "white":
                    self.black_captured_pieces.append(self.board[end[0]][end[1]].symbol)
                else:
                    self.white_captured_pieces.append(self.board[end[0]][end[1]].symbol)    
                self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
                self.board[start[0]][start[1]] = None 

                # We are looking for fifty consecutive moves where neither player has moved a pawn or captured a piece to declare a draw, and every capture breaks this sequence
                self.fifty_moves_count = 0
                return True
            else:
                return False


    def find_king(self, piece_color):
        for row in range(8):  
            for col in range(8):
                if isinstance(self.board[row][col], King) and self.board[row][col].color == piece_color:
                    return row, col    
                 

    def is_draw(self, piece_color):
        if (
            self.check_board.fifty_moves(self.fifty_moves_count) 
            or self.check_board.five_same_moves(self.moves)
            or self.check_board.stalemate(self.board, self.find_king(piece_color), piece_color)
            or self.check_board.insufficient_material(self.board)
        ):
            return True
        else:
            return False


    def convert_input(self):
    
        # to convert column letter to index
        col_map = {'a': 0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        
        # get the valid input
        while True:
            user_input = input("Enter the movement. For example, your input can be like \"a7 a5\" to move the left-most white pawn in the first movement ")
            posistions = user_input.lower().split()
            if (
                len(posistions) == len(posistions[0]) == len(posistions[1]) == 2 
                and posistions[0][0] in "abcdefgh" and posistions[0][1] in "12345678" 
                and posistions[1][0] in "abcdefgh" and posistions[1][1] in "12345678"
                and posistions[0] != posistions[1]
            ):
                posistions[0] = posistions[0].strip()
                posistions[1] = posistions[1].strip()
                # convert input to board array indices
                start = (int(posistions[0][1]) - 1, col_map[posistions[0][0]])
                end = (int(posistions[1][1]) - 1, col_map[posistions[1][0]])
                if self.board[start[0]][start[1]]:
                    break
            
        return start, end
    
    
    # Display the current state of the board
    def display(self):
        if self.black_captured_pieces:
            print("captured pieces: ", self.black_captured_pieces)
        print("   ---------------------------------")
        for row in range(8):
            print(row + 1, " ", end="|")
            for col in range(8):
                if self.board[row][col]:
                    print("", self.board[row][col].symbol, "|", end="")
                else:
                    print("  ", "|", end="")    
            print("\n   ---------------------------------")
        print("     a   b   c   d   e   f   g   h  ")
        if self.white_captured_pieces:
            print("captured pieces: ", self.white_captured_pieces, '\n')