from Chess.ChessBoardClass import ChessBoard
from IPython.display import clear_output


chess_board = ChessBoard()
chess_board.place_pieces()
chess_board.display()

colors = ["white", "black"]
turn_index = 0
while True: 
    turn = colors[turn_index]
    print(f"the turn is for {turn}")
    start, end = chess_board.convert_input()
    if chess_board.board[start[0]][start[1]].color != turn:
        clear_output()
        chess_board.display()
        print(f"that's not {chess_board.board[start[0]][start[1]].color}'s turn")
    else:
        if chess_board.move_any_pieces(start, end):
            clear_output()
            chess_board.display()
            white_row, white_col = chess_board.find_king("white")
            black_row, black_col = chess_board.find_king("black")
            if not chess_board.check_board.checkmate(chess_board.board, (white_row, white_col), "white"):
                print("The white is checkmate")
                print("The black player has won")
                break
            elif not chess_board.check_board.checkmate(chess_board.board, (black_row, black_col), "black"):
                print("The black is checkmate")
                print("The white player has won")
                break
            elif chess_board.is_draw(turn):
                print("A draw is happened")
                break

            turn_index = (turn_index + 1) % 2 
        else:
            clear_output()
            chess_board.display()
            print("Invalid Movement")    

