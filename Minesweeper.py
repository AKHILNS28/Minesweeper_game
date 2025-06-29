import tkinter as tk
import random
def create_board(size, num_mines):
    board = [[0 for _ in range(size)] for _ in range(size)]
    mine_positions = set()
    while len(mine_positions) < num_mines:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        mine_positions.add((row, col))

    for row, col in mine_positions:
        board[row][col] = 'M'
        for r in range(max(0, row - 1), min(size, row + 2)):
            for c in range(max(0, col - 1), min(size, col + 2)):
                if board[r][c] != 'M':
                    board[r][c] += 1
    return board, mine_positions
def reveal_cell(board, buttons, revealed, row, col):
    if revealed[row][col]:
        return
    revealed[row][col] = True

    if board[row][col] == 'M':
        buttons[row][col].config(text='M', bg='red', state='disabled')
        end_game(False, buttons)
        return
    buttons[row][col].config(text=str(board[row][col]) if board[row][col] > 0 else '', state='disabled')
    if board[row][col] == 0:
        for r in range(max(0, row - 1), min(len(board), row + 2)):
            for c in range(max(0, col - 1), min(len(board), col + 2)):
                if not revealed[r][c]:
                    reveal_cell(board, buttons, revealed, r, c)
def end_game(won, buttons):
    for row in buttons:
        for btn in row:
            btn.config(state='disabled')
    if won:
        print("Congratulations! You cleared the board.")
    else:
        print("BOOM! You hit a mine! Game over.")
def check_win(board, revealed, mine_positions):
    size = len(board)
    return all(revealed[r][c] or (r, c) in mine_positions for r in range(size) for c in range(size))

def on_cell_click(board, buttons, revealed, row, col, mine_positions):
    if revealed[row][col]:
        return
    reveal_cell(board, buttons, revealed, row, col)
    if check_win(board, revealed, mine_positions):
        end_game(True, buttons)
def create_gui(size, board, mine_positions):
    root = tk.Tk()
    root.title("Minesweeper")

    buttons = [[None for _ in range(size)] for _ in range(size)]
    revealed = [[False for _ in range(size)] for _ in range(size)]

    for row in range(size):
        for col in range(size):
            btn = tk.Button(root, text="", width=3, height=1,
                            command=lambda r=row, c=col: on_cell_click(board, buttons, revealed, r, c, mine_positions))
            btn.grid(row=row, column=col)
            buttons[row][col] = btn
    root.mainloop()
def main():
    size = 8
    num_mines = 10
    board, mine_positions = create_board(size, num_mines)
    create_gui(size, board, mine_positions)
if __name__ == "__main__":
    main()