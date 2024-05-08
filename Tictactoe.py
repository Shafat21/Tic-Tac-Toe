import tkinter as tk
import tkinter.messagebox as mbox
import random as rm

def main():
    game = TicTacToe()
    game.window.mainloop()

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Tic-Tac-Toe')
        self.window.configure(bg='#333333')
        self.choose_mode()

    def choose_mode(self):
        self.mode_frame = tk.Frame(self.window, bg='#333333')
        self.mode_frame.pack(pady=50)

        tk.Label(self.mode_frame, text="Choose game mode:", font=('Helvetica', 16, 'bold'), fg='white', bg='#333333').pack(side=tk.TOP, pady=10)
        tk.Button(self.mode_frame, text="Human vs AI", font=('Helvetica', 14), command=lambda: self.start_game(False), relief=tk.FLAT, bg='#555555', fg='white', padx=10, pady=10).pack(side=tk.LEFT, padx=100)
        tk.Button(self.mode_frame, text="AI vs AI", font=('Helvetica', 14), command=lambda: self.start_game(True), relief=tk.FLAT, bg='#555555', fg='white', padx=10, pady=10).pack(side=tk.LEFT, padx=100)

    def start_game(self, ai_vs_ai):
        self.ai_vs_ai = ai_vs_ai
        self.mode_frame.destroy()
        self.current_player = rm.choice(['X', 'O'])
        self.board = [[None] * 3 for _ in range(3)]
        self.buttons = [[None] * 3 for _ in range(3)]
        self.create_board()

        if self.ai_vs_ai:
            self.window.after(100, self.ai_move)

    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.window, text='', font=('Helvetica', 24), relief=tk.RAISED,
                                               borderwidth=2, bg='#4D4D4D', fg='white', activebackground='#666666', activeforeground='white',
                                               command=lambda row=i, col=j: self.make_move(row, col, True))
                self.buttons[i][j].grid(row=i, column=j, sticky='nsew', ipadx=30, ipady=30)

        for i in range(3):
            self.window.grid_columnconfigure(i, weight=1)
            self.window.grid_rowconfigure(i, weight=1)

    def make_move(self, row, col, human):
        if self.buttons[row][col]['text'] == '' and not self.check_win() and not self.check_tie():
            self.buttons[row][col]['text'] = self.current_player
            self.board[row][col] = self.current_player
            self.print_board_state()

            if self.check_win():
                mbox.showinfo('Game Over', f'{self.current_player} wins!')
                self.reset_game()
                return
            elif self.check_tie():
                mbox.showinfo('Game Over', 'It\'s a tie!')
                self.reset_game()
                return

            self.current_player = 'O' if self.current_player == 'X' else 'X'
            if (human and not self.ai_vs_ai) or self.ai_vs_ai:
                self.window.after(100, self.ai_move)

    def ai_move(self):
        if not self.check_win() and not self.check_tie():
            move = self.find_best_move()
            if move:
                self.make_move(move[0], move[1], False)

    def check_win(self):
        for line in self.board:
            if line.count(line[0]) == 3 and line[0] is not None:
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return True
        return False

    def check_tie(self):
        return all(self.board[i][j] is not None for i in range(3) for j in range(3))

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='')
                self.board[i][j] = None
        self.current_player = 'X'
        if self.ai_vs_ai:
            self.window.after(2000, self.ai_move)

    def find_best_move(self):
        best_score = float('-inf')
        best_moves = []
        alpha = float('-inf')
        beta = float('inf')
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    self.board[i][j] = self.current_player
                    score = self.alphabeta(0, False, alpha, beta)
                    self.board[i][j] = None
                    if score > best_score:
                        best_score = score
                        best_moves = [(i, j)]
                    elif score == best_score:
                        best_moves.append((i, j))
        return rm.choice(best_moves) if best_moves else None

    def alphabeta(self, depth, is_maximizing, alpha, beta):
        if self.check_win():
            return 1 if not is_maximizing else -1
        if self.check_tie():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] is None:
                        self.board[i][j] = 'O' if self.current_player == 'X' else 'X'
                        score = self.alphabeta(depth + 1, False, alpha, beta)
                        self.board[i][j] = None
                        best_score = max(score, best_score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] is None:
                        self.board[i][j] = 'X' if self.current_player == 'O' else 'O'
                        score = self.alphabeta(depth + 1, True, alpha, beta)
                        self.board[i][j] = None
                        best_score = min(score, best_score)
                        beta = min(beta, score)
                        if beta <= alpha:
                            break
            return best_score

    def print_board_state(self):
        for row in self.board:
            print(row)
        print()

if __name__ == '__main__':
    main()
