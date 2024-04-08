from Chess.ChessPieceClass import King
from Chess.ChessPieceClass import Knight
from Chess.ChessPieceClass import Bishop
from Chess.ChessPieceClass import Pawn
import copy


class CheckBoard:
    # to check the destination square is empty or not
    def empty_square(self, board, position):
        if not board[position[0]][position[1]]:
            return True
        return False
            
    def capture(self, board, piece_color, position):
        """
        check an opponent's piece can be captured in current move or not 
        """
        if board[position[0]][position[1]].color != piece_color and not isinstance(board[position[0]][position[1]], King):
            return True
        return False
    

    def check(self, board, king_position, piece_color):
        """A method to check whether the king is check by opponent's pieces"""
        for row in range(8):
            for col in range(8):
                if isinstance(board[row][col], Pawn):
                    if board[row][col] and board[row][col].move(board, (row,col), king_position, [False, [0,0]])[0] and board[row][col].color != piece_color:
                        return True
                elif not isinstance(board[row][col], King):
                    if board[row][col] and board[row][col].move(board, (row,col), king_position) and board[row][col].color != piece_color:
                        return True
        
        return False
            
    def checkmate(self, board, king_position, piece_color):
        """A method to check whether the king is checkmate by opponent's pieces"""
        if self.check(board, king_position, piece_color):
            possible_position_for_king = []
            # Define possible movements for the king
            king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            
            # Iterate through possible movements
            for move in king_moves:
                # Calculate new position
                new_position = (king_position[0] + move[0], king_position[1] + move[1])
                
                # Check if new position is within the board boundaries
                if 0 <= new_position[0] < 8 and 0 <= new_position[1] < 8:
                    # Check if the new position is empty or occupied by an opponent's piece
                    if ((
                        board[new_position[0]][new_position[1]] == None 
                        or board[new_position[0]][new_position[1]].color != piece_color
                        ) 
                        and not self.check(board, new_position, piece_color)
                    ):
                        possible_position_for_king.append(new_position)
            
            if len(possible_position_for_king) > 0:
                return True
            elif len(possible_position_for_king) == 0:    
                # If the king couldn't make a move, come and check if there is a piece to fix the king.
                for row in range(8):
                    for col in range(8):
                        if board[row][col] and board[row][col].color == piece_color and not isinstance(board[row][col], King):
    
                            for row2 in range(8):
                                for col2 in range(8):
                                    if isinstance(board[row][col], Pawn):
                                        if (
                                            not isinstance(board[row2][col2], King)
                                            and board[row][col].move(board, (row,col), (row2,col2), [False, [0, 0]])[0]
                                            and (self.empty_square(board, (row2,col2)) or self.capture(board,piece_color, (row2,col2)))
                                        ):
                                            copy_of_board = copy.deepcopy(board)
                                            copy_of_board[row2][col2] = copy_of_board[row][col]
                                            copy_of_board[row][col] = None
                                            if not self.check(copy_of_board, king_position,piece_color):
                                                return True
                                    else:
                                        if (
                                            not isinstance(board[row2][col2], King)
                                            and board[row][col].move(board, (row,col), (row2,col2))
                                            and (self.empty_square(board, (row2,col2)) or self.capture(board,piece_color, (row2,col2)))
                                        ):
                                            copy_of_board = copy.deepcopy(board)
                                            copy_of_board[row2][col2] = copy_of_board[row][col]
                                            copy_of_board[row][col] = None
                                            if not self.check(copy_of_board, king_position,piece_color):
                                                return True

                return False
        else:
            return True


    def insufficient_material(self, board):
        """It is a method that measures the lack of enough force for matting.
          In this case, two players do not have enough power to checkmate the chess game. This happens in three situations:
            1- The king against the king
            2- The king and the knight against the king alone
            3- The king and the bishop against the king alone
        """
        white_pieces = []
        black_pieces = []
        # we want to count the number of white pieces and black pieces
        for row in range(8):
            for col in range(8):
                if board[row][col]:
                    if board[row][col].color == "white":
                        white_pieces.append(board[row][col])
                    elif board[row][col].color == "black":
                        black_pieces.append(board[row][col])
         # Check if there are only kings or one side has only king and the other side has king and one minor piece
        if len(white_pieces) == 1 and len(black_pieces) == 1:
            return True
        elif len(white_pieces) == 1 and len(black_pieces) == 2 and any(isinstance(piece, (Bishop, Knight)) for piece in black_pieces):
            return True
        elif len(black_pieces) == 1 and len(white_pieces) == 2 and any(isinstance(piece, (Bishop, Knight)) for piece in white_pieces):
            return True
        elif len(black_pieces) == 2 and len(white_pieces) == 2 and any(isinstance(piece, Bishop) for piece in white_pieces) and any(isinstance(piece, Bishop) for piece in black_pieces):
            return True
        return False

      
    def stalemate(self, board, king_position, piece_color):#logic
        """A stalemate is a position in which the player whose turn it is to move
        has no legal move and his king is not in check. 
        A stalemate results in an immediate draw."""
        if not self.check(board, king_position,piece_color):
            possible_position_for_king = []
            # Define possible movements for the king
            king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            
            # Iterate through possible movements
            for move in king_moves:
                # Calculate new position
                new_position = (king_position[0] + move[0], king_position[1] + move[1])
                
                # Check if new position is within the board boundaries
                if 0 <= new_position[0] < 8 and 0 <= new_position[1] < 8:
                    # Check if the new position is empty or occupied by an opponent's piece
                    if ((
                        board[new_position[0]][new_position[1]] == None 
                        or board[new_position[0]][new_position[1]].color != piece_color
                        ) 
                        and not self.check(board, new_position, piece_color)
                    ):
                        possible_position_for_king.append(new_position)

            if len(possible_position_for_king) == 0:            # TO check that the king has choice or not
                # To check that the player has legal move for other pieces or not
                
                for row in range(8):
                    for col in range(8):
                        if board[row][col] and board[row][col].color == piece_color and not isinstance(board[row][col], King):
    
                            for row2 in range(8):
                                for col2 in range(8):
                                    if isinstance(board[row][col], Pawn):
                                        if (
                                            not isinstance(board[row2][col2], King)
                                            and board[row][col].move(board, (row,col), (row2,col2), [False, [0, 0]])[0]
                                            and (self.empty_square(board, (row2,col2)) or self.capture(board,piece_color, (row2,col2)))
                                        ):
                                            copy_of_board = copy.deepcopy(board)
                                            copy_of_board[row2][col2] = copy_of_board[row][col]
                                            copy_of_board[row][col] = None
                                            if not self.check(copy_of_board, king_position,piece_color):
                                                return False #continue the game
                                    else:
                                        if (
                                            not isinstance(board[row2][col2], King)
                                            and board[row][col].move(board, (row,col), (row2,col2))
                                            and (self.empty_square(board, (row2,col2)) or self.capture(board,piece_color, (row2,col2)))
                                        ):
                                            copy_of_board = copy.deepcopy(board)
                                            copy_of_board[row2][col2] = copy_of_board[row][col]
                                            copy_of_board[row][col] = None
                                            if not self.check(copy_of_board, king_position,piece_color):
                                                return False  #continue the game
                            
                return True    # game ends without victory for either player
            else:
                return False #continue the game
        else:
            return False #continue the game   
    
    def five_same_moves(self, moves):
        if moves.count(moves[-1]) == 5 :
            return True
        return False
    
    def fifty_moves(self, fifty_moves_count):
        if fifty_moves_count == 50:
            return True
        return False    

    #to check after this move the king will not be in check and 
    #also it's not in check already and to check is the game ended (checkmate or draw occured) or not
    def valid_movement(self, board, start, end, piece_color):
        copy_of_board = copy.deepcopy(board)
        copy_of_board[end[0]][end[1]] = copy_of_board[start[0]][start[1]]
        copy_of_board[start[0]][start[1]] = None
        for row in range(8):
            for col in range(8):
                if (
                    isinstance(copy_of_board[row][col], King)
                    and copy_of_board[row][col].color == piece_color
                    and self.check(copy_of_board, (row, col), piece_color)
                ):
                    return False   # if after the movement King is in check return False
        return True  # if after the movement King isn't in check return True 