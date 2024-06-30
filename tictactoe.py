import tkinter as tk
from tkinter import messagebox

# Constants
PLAYER = 'O'
AI = 'X'
EMPTY = ' '

# Initialize the board
board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]

def is_moves_left(board):
    for row in board:
        if EMPTY in row:
            return True
    return False

def evaluate(board):
    # Check rows for victory
    for row in board:
        if row[0] == row[1] == row[2]:
            if row[0] == AI:
                return 10
            elif row[0] == PLAYER:
                return -10
    
    # Check columns for victory
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == AI:
                return 10
            elif board[0][col] == PLAYER:
                return -10
    
    # Check diagonals for victory
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == AI:
            return 10
        elif board[0][0] == PLAYER:
            return -10

    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == AI:
            return 10
        elif board[0][2] == PLAYER:
            return -10

    return 0

def minimax(board, depth, is_max):
    score = evaluate(board)

    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if not is_moves_left(board):
        return 0

    if is_max:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    best = max(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = EMPTY
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER
                    best = min(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = EMPTY
        return best

def find_best_move(board):
    best_val = -1000
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                move_val = minimax(board, 0, False)
                board[i][j] = EMPTY
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move

def check_winner():
    score = evaluate(board)
    if score == 10:
        return AI
    elif score == -10:
        return PLAYER
    elif not is_moves_left(board):
        return 'Draw'
    return None

# Initialize the GUI
def reset_board():
    global board
    board = [[EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    for button in buttons:
        button.config(text=EMPTY, state=tk.NORMAL)

def on_click(row, col):
    if board[row][col] == EMPTY:
        board[row][col] = PLAYER
        buttons[row * 3 + col].config(text=PLAYER, state=tk.DISABLED)
        winner = check_winner()
        if winner:
            game_over(winner)
        else:
            ai_move()

def ai_move():
    best_move = find_best_move(board)
    if best_move != (-1, -1):
        row, col = best_move
        board[row][col] = AI
        buttons[row * 3 + col].config(text=AI, state=tk.DISABLED)
        winner = check_winner()
        if winner:
            game_over(winner)

def game_over(winner):
    if winner == 'Draw':
        messagebox.showinfo("Tic Tac Toe", "It's a draw!")
    else:
        messagebox.showinfo("Tic Tac Toe", f"The winner is {winner}!")
    reset_board()

root = tk.Tk()
root.title("Tic Tac Toe")

buttons = []
for i in range(3):
    for j in range(3):
        button = tk.Button(root, text=EMPTY, font=('normal', 40), width=5, height=2,
                           command=lambda row=i, col=j: on_click(row, col))
        button.grid(row=i, column=j)
        buttons.append(button)

reset_button = tk.Button(root, text='Reset', command=reset_board)
reset_button.grid(row=3, column=0, columnspan=3)

reset_board()
root.mainloop()
