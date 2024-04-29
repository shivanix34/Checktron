from tkinter import Canvas, Event, messagebox
from PIL import Image, ImageTk
from random import choice
from pathlib import Path
from time import sleep
from math import inf
from checkers.checkers import Field, Point, Move, Player
from checkers.checkers import CheckerType, SideType



class Game:
    def __init__(self, canvas: Canvas, x_field_size: int, y_field_size: int):
        self.__canvas = canvas
        self.__field = Field(x_field_size, y_field_size)
        self.__player = Player()  
        self.__player_turn = True
        self.__hovered_cell = Point()
        self.__selected_cell = Point()
        self.__animated_cell = Point()
        self.__init_images()
        self.__draw()
        if (self.__player.PLAYER_SIDE == SideType.BLACK):  
            self.__handle_enemy_turn()

    def __init_images(self):
        self.__images = {
            CheckerType.WHITE_REGULAR: ImageTk.PhotoImage(
                Image.open(Path('assets', 'white-regular.png')).resize((self.__player.CELL_SIZE, self.__player.CELL_SIZE), Image.LANCZOS)),
            CheckerType.BLACK_REGULAR: ImageTk.PhotoImage(
                Image.open(Path('assets', 'black-regular.png')).resize((self.__player.CELL_SIZE, self.__player.CELL_SIZE), Image.LANCZOS)),
            CheckerType.WHITE_QUEEN: ImageTk.PhotoImage(
                Image.open(Path('assets', 'white-queen.png')).resize((self.__player.CELL_SIZE, self.__player.CELL_SIZE), Image.LANCZOS)),
            CheckerType.BLACK_QUEEN: ImageTk.PhotoImage(
                Image.open(Path('assets', 'black-queen.png')).resize((self.__player.CELL_SIZE, self.__player.CELL_SIZE), Image.LANCZOS)),
        }

    def __animate_move(self, move: Move):
        self.__animated_cell = Point(move.from_x, move.from_y)
        self.__draw()
        self.__player = Player()
        animated_checker = self.__canvas.create_image(move.from_x * self.__player.CELL_SIZE, move.from_y * self.__player.CELL_SIZE,
                                                      image=self.__images.get(
                                                          self.__field.type_at(move.from_x, move.from_y)), anchor='nw',
                                                      tag='animated_checker')
        dx = 1 if move.from_x < move.to_x else -1
        dy = 1 if move.from_y < move.to_y else -1
        for distance in range(abs(move.from_x - move.to_x)):
            for _ in range(100 // self.__player.ANIMATION_SPEED):
                self.__canvas.move(animated_checker, self.__player.ANIMATION_SPEED / 100 * self.__player.CELL_SIZE * dx,
                                   self.__player.ANIMATION_SPEED / 100 * self.__player.CELL_SIZE * dy)
                self.__canvas.update()
                sleep(0.01)
        self.__animated_cell = Point()

    def __draw(self):
        self.__canvas.delete('all')
        self.__draw_field_grid()
        self.__draw_checkers()

    def __draw_field_grid(self):
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                self.__canvas.create_rectangle(x * self.__player.CELL_SIZE, y * self.__player.CELL_SIZE, x * self.__player.CELL_SIZE + self.__player.CELL_SIZE,
                                               y * self.__player.CELL_SIZE + self.__player.CELL_SIZE, fill=self.__player.FIELD_COLORS[(y + x) % 2], width=0,
                                               tag='boards')
                if (x == self.__selected_cell.x and y == self.__selected_cell.y):
                    self.__canvas.create_rectangle(x * self.__player.CELL_SIZE + self.__player.BORDER_WIDTH // 2, y * self.__player.CELL_SIZE + self.__player.BORDER_WIDTH // 2,
                                                   x * self.__player.CELL_SIZE + self.__player.CELL_SIZE - self.__player.BORDER_WIDTH // 2,
                                                   y * self.__player.CELL_SIZE + self.__player.CELL_SIZE - self.__player.BORDER_WIDTH // 2,
                                                   outline=self.__player.SELECT_BORDER_COLOR, width=self.__player.BORDER_WIDTH, tag='border')
                elif (x == self.__hovered_cell.x and y == self.__hovered_cell.y):
                    self.__canvas.create_rectangle(x * self.__player.CELL_SIZE + self.__player.BORDER_WIDTH // 2, y * self.__player.CELL_SIZE + self.__player.BORDER_WIDTH // 2,
                                                   x * self.__player.CELL_SIZE + self.__player.CELL_SIZE - self.__player.BORDER_WIDTH // 2,
                                                   y * self.__player.CELL_SIZE + self.__player.CELL_SIZE - self.__player.BORDER_WIDTH // 2,
                                                   outline=self.__player.HOVER_BORDER_COLOR, width=self.__player.BORDER_WIDTH, tag='border')
                if (self.__selected_cell):
                    player_moves_list = self.__get_moves_list(self.__player.PLAYER_SIDE)
                    for move in player_moves_list:
                        if (self.__selected_cell.x == move.from_x and self.__selected_cell.y == move.from_y):
                            self.__canvas.create_oval(move.to_x * self.__player.CELL_SIZE + self.__player.CELL_SIZE / 3,
                                                      move.to_y * self.__player.CELL_SIZE + self.__player.CELL_SIZE / 3,
                                                      move.to_x * self.__player.CELL_SIZE + (self.__player.CELL_SIZE - self.__player.CELL_SIZE / 3),
                                                      move.to_y * self.__player.CELL_SIZE + (self.__player.CELL_SIZE - self.__player.CELL_SIZE / 3),
                                                      fill=self.__player.POSIBLE_MOVE_CIRCLE_COLOR, width=0,
                                                      tag='posible_move_circle')

    def __draw_checkers(self):
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                if (self.__field.type_at(x, y) != CheckerType.NONE and not (
                        x == self.__animated_cell.x and y == self.__animated_cell.y)):
                    self.__canvas.create_image(x * self.__player.CELL_SIZE, y * self.__player.CELL_SIZE,
                                               image=self.__images.get(self.__field.type_at(x, y)), anchor='nw',
                                               tag='checkers')

    def mouse_move(self, event: Event):
        x, y = (event.x) // self.__player.CELL_SIZE, (event.y) // self.__player.CELL_SIZE
        if (x != self.__hovered_cell.x or y != self.__hovered_cell.y):
            self.__hovered_cell = Point(x, y)
            if (self.__player_turn):
                self.__draw()

    def mouse_down(self, event: Event):
        if not (self.__player_turn): return
        x, y = (event.x) // self.__player.CELL_SIZE, (event.y) // self.__player.CELL_SIZE
        if not (self.__field.is_within(x, y)): return
        if (self.__player.PLAYER_SIDE == SideType.WHITE):
            player_checkers = self.__player.WHITE_CHECKERS
        elif (self.__player.PLAYER_SIDE == SideType.BLACK):
            player_checkers = self.__player.BLACK_CHECKERS
        else:
            return
        if (self.__field.type_at(x, y) in player_checkers):
            self.__selected_cell = Point(x, y)
            self.__draw()
        elif (self.__player_turn):
            move = Move(self.__selected_cell.x, self.__selected_cell.y, x, y)
            if (move in self.__get_moves_list(self.__player.PLAYER_SIDE)):
                self.__handle_player_turn(move)
                if not (self.__player_turn):
                    self.__handle_enemy_turn()

    def __handle_move(self, move: Move, draw: bool = True) -> bool:
        if (draw): self.__animate_move(move)
        if (move.to_y == 0 and self.__field.type_at(move.from_x, move.from_y) == CheckerType.WHITE_REGULAR):
            self.__field.at(move.from_x, move.from_y).change_type(CheckerType.WHITE_QUEEN)
        elif (move.to_y == self.__field.y_size - 1 and self.__field.type_at(move.from_x,
                                                                            move.from_y) == CheckerType.BLACK_REGULAR):
            self.__field.at(move.from_x, move.from_y).change_type(CheckerType.BLACK_QUEEN)
        self.__field.at(move.to_x, move.to_y).change_type(self.__field.type_at(move.from_x, move.from_y))
        self.__field.at(move.from_x, move.from_y).change_type(CheckerType.NONE)
        dx = -1 if move.from_x < move.to_x else 1
        dy = -1 if move.from_y < move.to_y else 1
        has_killed_checker = False
        x, y = move.to_x, move.to_y
        while (x != move.from_x or y != move.from_y):
            x += dx
            y += dy
            if (self.__field.type_at(x, y) != CheckerType.NONE):
                self.__field.at(x, y).change_type(CheckerType.NONE)
                has_killed_checker = True
        if (draw): self.__draw()
        return has_killed_checker

    def __handle_player_turn(self, move: Move):
        self.__player_turn = False
        has_killed_checker = self.__handle_move(move)
        required_moves_list = list(
            filter(lambda required_move: move.to_x == required_move.from_x and move.to_y == required_move.from_y,
                   self.__get_required_moves_list(self.__player.PLAYER_SIDE)))
        if (has_killed_checker and required_moves_list):
            self.__player_turn = True
        self.__selected_cell = Point()

    def __handle_enemy_turn(self):
        self.__player_turn = False
        optimal_moves_list = self.__predict_optimal_moves(SideType.opposite(self.__player.PLAYER_SIDE))
        for move in optimal_moves_list:
            self.__handle_move(move)
        self.__player_turn = True
        self.__check_for_game_over()

    def __check_for_game_over(self):
        game_over = False
        white_moves_list = self.__get_moves_list(SideType.WHITE)
        if not (white_moves_list):
            answer = messagebox.showinfo('The end of the game', 'Black wins')
            game_over = True
        black_moves_list = self.__get_moves_list(SideType.BLACK)
        if not (black_moves_list):
            answer = messagebox.showinfo('The end of the game', 'White wins')
            game_over = True
        if (game_over):
            self.__init__(self.__canvas, self.__field.x_size, self.__field.y_size)

    def __predict_optimal_moves(self, side: SideType) -> list[Move]:
        best_result = 0
        optimal_moves = []
        predicted_moves_list = self.__get_predicted_moves_list(side)
        if (predicted_moves_list):
            field_copy = Field.copy(self.__field)
            for moves in predicted_moves_list:
                for move in moves:
                    self.__handle_move(move, draw=False)
                try:
                    if (side == SideType.WHITE):
                        result = self.__field.white_score / self.__field.black_score
                    elif (side == SideType.BLACK):
                        result = self.__field.black_score / self.__field.white_score
                except ZeroDivisionError:
                    result = inf
                if (result > best_result):
                    best_result = result
                    optimal_moves.clear()
                    optimal_moves.append(moves)
                elif (result == best_result):
                    optimal_moves.append(moves)
                self.__field = Field.copy(field_copy)
        optimal_move = []
        if (optimal_moves):
            for move in choice(optimal_moves):
                if (side == SideType.WHITE and self.__field.type_at(move.from_x, move.from_y) in self.__player.BLACK_CHECKERS):
                    break
                elif (side == SideType.BLACK and self.__field.type_at(move.from_x, move.from_y) in self.__player.WHITE_CHECKERS):
                    break
                optimal_move.append(move)
        return optimal_move

    def __get_predicted_moves_list(self, side: SideType, current_prediction_depth: int = 0,
                                   all_moves_list: list[Move] = [], current_moves_list: list[Move] = [],
                                   required_moves_list: list[Move] = []) -> list[Move]:
        if (current_moves_list):
            all_moves_list.append(current_moves_list)
        else:
            all_moves_list.clear()
        if (required_moves_list):
            moves_list = required_moves_list
        else:
            moves_list = self.__get_moves_list(side)
        if (moves_list and current_prediction_depth < self.__player.MAX_PREDICTION_DEPTH):
            field_copy = Field.copy(self.__field)
            for move in moves_list:
                has_killed_checker = self.__handle_move(move, draw=False)
                required_moves_list = list(filter(
                    lambda required_move: move.to_x == required_move.from_x and move.to_y == required_move.from_y,
                    self.__get_required_moves_list(side)))
                if (has_killed_checker and required_moves_list):
                    self.__get_predicted_moves_list(side, current_prediction_depth, all_moves_list,
                                                    current_moves_list + [move], required_moves_list)
                else:
                    self.__get_predicted_moves_list(SideType.opposite(side), current_prediction_depth + 1,
                                                    all_moves_list, current_moves_list + [move])
                self.__field = Field.copy(field_copy)
        return all_moves_list

    def __get_moves_list(self, side: SideType) -> list[Move]:
        moves_list = self.__get_required_moves_list(side)
        if not (moves_list):
            moves_list = self.__get_optional_moves_list(side)
        return moves_list

    def __get_required_moves_list(self, side: SideType) -> list[Move]:
        moves_list = []
        if (side == SideType.WHITE):
            friendly_checkers = self.__player.WHITE_CHECKERS
            enemy_checkers = self.__player.BLACK_CHECKERS
        elif (side == SideType.BLACK):
            friendly_checkers = self.__player.BLACK_CHECKERS
            enemy_checkers = self.__player.WHITE_CHECKERS
        else:
            return moves_list
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                if (self.__field.type_at(x, y) == friendly_checkers[0]):
                    for offset in self.__player.MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x * 2, y + offset.y * 2)): continue
                        if self.__field.type_at(x + offset.x, y + offset.y) in enemy_checkers and self.__field.type_at(
                                x + offset.x * 2, y + offset.y * 2) == CheckerType.NONE:
                            moves_list.append(Move(x, y, x + offset.x * 2, y + offset.y * 2))
                elif (self.__field.type_at(x, y) == friendly_checkers[1]):
                    for offset in self.__player.MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x * 2, y + offset.y * 2)): continue
                        has_enemy_checker_on_way = False
                        for shift in range(1, self.__field.size):
                            if not (self.__field.is_within(x + offset.x * shift, y + offset.y * shift)): continue
                            if (not has_enemy_checker_on_way):
                                if (self.__field.type_at(x + offset.x * shift, y + offset.y * shift) in enemy_checkers):
                                    has_enemy_checker_on_way = True
                                    continue
                                elif (self.__field.type_at(x + offset.x * shift,
                                                           y + offset.y * shift) in friendly_checkers):
                                    break
                            if (has_enemy_checker_on_way):
                                if (self.__field.type_at(x + offset.x * shift,
                                                         y + offset.y * shift) == CheckerType.NONE):
                                    moves_list.append(Move(x, y, x + offset.x * shift, y + offset.y * shift))
                                else:
                                    break
        return moves_list

    def __get_optional_moves_list(self, side: SideType) -> list[Move]:
        moves_list = []
        if (side == SideType.WHITE):
            friendly_checkers = self.__player.WHITE_CHECKERS
        elif (side == SideType.BLACK):
            friendly_checkers = self.__player.BLACK_CHECKERS
        else:
            return moves_list
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                if (self.__field.type_at(x, y) == friendly_checkers[0]):
                    for offset in self.__player.MOVE_OFFSETS[:2] if side == SideType.WHITE else self.__player.MOVE_OFFSETS[2:]:
                        if not (self.__field.is_within(x + offset.x, y + offset.y)): continue
                        if (self.__field.type_at(x + offset.x, y + offset.y) == CheckerType.NONE):
                            moves_list.append(Move(x, y, x + offset.x, y + offset.y))
                elif (self.__field.type_at(x, y) == friendly_checkers[1]):
                    for offset in self.__player.MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x, y + offset.y)): continue
                        for shift in range(1, self.__field.size):
                            if not (self.__field.is_within(x + offset.x * shift, y + offset.y * shift)): continue
                            if (self.__field.type_at(x + offset.x * shift, y + offset.y * shift) == CheckerType.NONE):
                                moves_list.append(Move(x, y, x + offset.x * shift, y + offset.y * shift))
                            else:
                                break
        return moves_list

    def __init_images(self):
        self.__images = {
            CheckerType.WHITE_REGULAR: ImageTk.PhotoImage(
                Image.open(Path('assets', 'white-regular.png')).resize((self.__player.CELL_SIZE, self.__player.CELL_SIZE), Image.LANCZOS)),
            CheckerType.BLACK_REGULAR: ImageTk.PhotoImage(
                Image.open(Path('assets', 'black-regular.png')).resize((self.__player.CELL_SIZE, self.__player.CELL_SIZE), Image.LANCZOS)),
            CheckerType.WHITE_QUEEN: ImageTk.PhotoImage(
                Image.open(Path('assets', 'white-queen.png')).resize((self.__player.CELL_SIZE, self.__player.CELL_SIZE), Image.LANCZOS)),
            CheckerType.BLACK_QUEEN: ImageTk.PhotoImage(
                Image.open(Path('assets', 'black-queen.png')).resize((self.__player.CELL_SIZE, self.__player.CELL_SIZE), Image.LANCZOS)),
        }

    def __draw(self):
        self.__canvas.delete('all')
        self.__draw_field_grid()
        self.__draw_checkers()

    def __draw_field_grid(self):
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                self.__canvas.create_rectangle(x * self.__player.CELL_SIZE, y * self.__player.CELL_SIZE, x * self.__player.CELL_SIZE + self.__player.CELL_SIZE,
                                               y * self.__player.CELL_SIZE + self.__player.CELL_SIZE, fill=self.__player.FIELD_COLORS[(y + x) % 2], width=0,
                                               tag='boards')
                if (x == self.__selected_cell.x and y == self.__selected_cell.y):
                    self.__canvas.create_rectangle(x * self.__player.CELL_SIZE + self.__player.BORDER_WIDTH // 2, y * self.__player.CELL_SIZE + self.__player.BORDER_WIDTH // 2,
                                                   x * self.__player.CELL_SIZE + self.__player.CELL_SIZE - self.__player.BORDER_WIDTH // 2,
                                                   y * self.__player.CELL_SIZE + self.__player.CELL_SIZE - self.__player.BORDER_WIDTH // 2,
                                                   outline=self.__player.SELECT_BORDER_COLOR, width=self.__player.BORDER_WIDTH, tag='border')
                elif (x == self.__hovered_cell.x and y == self.__hovered_cell.y):
                    self.__canvas.create_rectangle(x * self.__player.CELL_SIZE + self.__player.BORDER_WIDTH // 2, y * self.__player.CELL_SIZE + self.__player.BORDER_WIDTH // 2,
                                                   x * self.__player.CELL_SIZE + self.__player.CELL_SIZE - self.__player.BORDER_WIDTH // 2,
                                                   y * self.__player.CELL_SIZE + self.__player.CELL_SIZE - self.__player.BORDER_WIDTH // 2,
                                                   outline=self.__player.HOVER_BORDER_COLOR, width=self.__player.BORDER_WIDTH, tag='border')
                if (self.__selected_cell):
                    player_moves_list = self.__get_moves_list(self.__player.PLAYER_SIDE)
                    for move in player_moves_list:
                        if (self.__selected_cell.x == move.from_x and self.__selected_cell.y == move.from_y):
                            self.__canvas.create_oval(move.to_x * self.__player.CELL_SIZE + self.__player.CELL_SIZE / 3,
                                                      move.to_y * self.__player.CELL_SIZE + self.__player.CELL_SIZE / 3,
                                                      move.to_x * self.__player.CELL_SIZE + (self.__player.CELL_SIZE - self.__player.CELL_SIZE / 3),
                                                      move.to_y * self.__player.CELL_SIZE + (self.__player.CELL_SIZE - self.__player.CELL_SIZE / 3),
                                                      fill=self.__player.POSIBLE_MOVE_CIRCLE_COLOR, width=0,
                                                      tag='posible_move_circle')

    def __draw_checkers(self):
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                if (self.__field.type_at(x, y) != CheckerType.NONE and not (
                        x == self.__animated_cell.x and y == self.__animated_cell.y)):
                    self.__canvas.create_image(x * self.__player.CELL_SIZE, y * self.__player.CELL_SIZE,
                                               image=self.__images.get(self.__field.type_at(x, y)), anchor='nw',
                                               tag='checkers')

    def mouse_move(self, event: Event):
        x, y = (event.x) // self.__player.CELL_SIZE, (event.y) // self.__player.CELL_SIZE
        if (x != self.__hovered_cell.x or y != self.__hovered_cell.y):
            self.__hovered_cell = Point(x, y)
            if (self.__player_turn):
                self.__draw()

    def mouse_down(self, event: Event):
        if not (self.__player_turn): return
        x, y = (event.x) // self.__player.CELL_SIZE, (event.y) // self.__player.CELL_SIZE
        if not (self.__field.is_within(x, y)): return
        if (self.__player.PLAYER_SIDE == SideType.WHITE):
            player_checkers = self.__player.WHITE_CHECKERS
        elif (self.__player.PLAYER_SIDE == SideType.BLACK):
            player_checkers = self.__player.BLACK_CHECKERS
        else:
            return
        if (self.__field.type_at(x, y) in player_checkers):
            self.__selected_cell = Point(x, y)
            self.__draw()
        elif (self.__player_turn):
            move = Move(self.__selected_cell.x, self.__selected_cell.y, x, y)
            if (move in self.__get_moves_list(self.__player.PLAYER_SIDE)):
                self.__handle_player_turn(move)
                if not (self.__player_turn):
                    self.__handle_enemy_turn()

    def __init__(self, canvas: Canvas, x_field_size: int, y_field_size: int, player: Player):
        self.__canvas = canvas
        self.__field = Field(x_field_size, y_field_size)
        self.__player = player
        self.__player_turn = self.__player.PLAYER_SIDE == SideType.BLACK
        self.__hovered_cell = Point()
        self.__selected_cell = Point()
        self.__animated_cell = Point()
        self.__init_images()
        self.__draw()
        if not self.__player_turn:
            self.__handle_enemy_turn()
