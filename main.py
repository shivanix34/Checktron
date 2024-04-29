from tkinter import Tk, Canvas, PhotoImage
from checkers.game import Game
from checkers.checkers import Player

class ChecktronApp:
    def __init__(self):
        self.main_window = Tk()
        self.main_window.title('Checktron')
        self.main_window.resizable(0, 0)
        self.main_window.iconphoto(False, PhotoImage(file='icon.png'))

        self.player = Player()

        self.main_canvas = Canvas(self.main_window, width=self.player.CELL_SIZE * self.player.X_SIZE, height=self.player.CELL_SIZE * self.player.Y_SIZE)
        self.main_canvas.pack()

        self.game = Game(self.main_canvas, self.player.X_SIZE, self.player.Y_SIZE, self.player)

        self.main_canvas.bind("<Motion>", self.game.mouse_move)
        self.main_canvas.bind("<Button-1>", self.game.mouse_down)

    def run(self):
        self.main_window.mainloop()

if __name__ == '__main__':
    app = ChecktronApp()
    app.run()
