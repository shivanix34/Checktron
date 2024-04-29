from enum import Enum, auto
from functools import reduce

class SideType(Enum):
    WHITE = auto()
    BLACK = auto()

    def opposite(side):
        if side == SideType.WHITE:
            return SideType.BLACK
        elif side == SideType.BLACK:
            return SideType.WHITE
        else:
            raise ValueError()

class CheckerType(Enum):
    NONE = auto()
    WHITE_REGULAR = auto()
    BLACK_REGULAR = auto()
    WHITE_QUEEN = auto()
    BLACK_QUEEN = auto()

class Point:
    def __init__(self, x: int = -1, y: int = -1):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __eq__(self, other):
        if isinstance(other, Point):
            return (
                self.x == other.x and
                self.y == other.y
            )
        return NotImplemented

class Checker:
    def __init__(self, type: CheckerType = CheckerType.NONE):
        self.__type = type

    @property
    def type(self):
        return self.__type

    def change_type(self, type: CheckerType):
        self.__type = type

class Player:
    def __init__(self):
        self.PLAYER_SIDE = SideType.WHITE
        self.X_SIZE = self.Y_SIZE = 8
        self.CELL_SIZE = 75
        self.ANIMATION_SPEED = 4
        self.MAX_PREDICTION_DEPTH = 3
        self.BORDER_WIDTH = 2 * 2

        self.FIELD_COLORS = ['#E7CFA9', '#927456']
        self.HOVER_BORDER_COLOR = '#54b346'
        self.SELECT_BORDER_COLOR = '#944444'
        self.POSIBLE_MOVE_CIRCLE_COLOR = '#944444'

        self.MOVE_OFFSETS = [
            Point(-1, -1),
            Point(1, -1),
            Point(-1, 1),
            Point(1, 1)
        ]

        self.WHITE_CHECKERS = [CheckerType.WHITE_REGULAR, CheckerType.WHITE_QUEEN]
        self.BLACK_CHECKERS = [CheckerType.BLACK_REGULAR, CheckerType.BLACK_QUEEN]

class Field:
    def __init__(self, x_size: int, y_size: int):
        self.__x_size = x_size
        self.__y_size = y_size
        self.__generate()

    @property
    def x_size(self) -> int:
        return self.__x_size

    @property
    def y_size(self) -> int:
        return self.__y_size

    @property
    def size(self) -> int:
        return max(self.x_size, self.y_size)

    @classmethod
    def copy(cls, field_instance):
        field_copy = cls(field_instance.x_size, field_instance.y_size)
        for y in range(field_instance.y_size):
            for x in range(field_instance.x_size):
                field_copy.at(x, y).change_type(field_instance.type_at(x, y))
        return field_copy

    def __generate(self):
        self.__checkers = [[Checker() for x in range(self.x_size)] for y in range(self.y_size)]
        for y in range(self.y_size):
            for x in range(self.x_size):
                if (y + x) % 2:
                    if y < 3:
                        self.__checkers[y][x].change_type(CheckerType.BLACK_REGULAR)
                    elif y >= self.y_size - 3:
                        self.__checkers[y][x].change_type(CheckerType.WHITE_REGULAR)

    def type_at(self, x: int, y: int) -> CheckerType:
        return self.__checkers[y][x].type

    def at(self, x: int, y: int) -> Checker:
        return self.__checkers[y][x]

    def is_within(self, x: int, y: int) -> bool:
        return 0 <= x < self.x_size and 0 <= y < self.y_size

    @property
    def white_checkers_count(self) -> int:
        return sum(
            reduce(lambda acc, checker: acc + (checker.type in self.WHITE_CHECKERS), checkers, 0)
            for checkers in self.__checkers
        )

    @property
    def black_checkers_count(self) -> int:
        return sum(
            reduce(lambda acc, checker: acc + (checker.type in self.BLACK_CHECKERS), checkers, 0)
            for checkers in self.__checkers
        )
    @property
    def white_score(self) -> int:
        return sum(
            reduce(
                lambda acc, checker: acc + (checker.type == CheckerType.WHITE_REGULAR) +
                (checker.type == CheckerType.WHITE_QUEEN) * 3,
                checkers, 0
            )
            for checkers in self.__checkers
        )

    @property
    def black_score(self) -> int:
        return sum(
            reduce(
                lambda acc, checker: acc + (checker.type == CheckerType.BLACK_REGULAR) +
                (checker.type == CheckerType.BLACK_QUEEN) * 3,
                checkers, 0
            )
            for checkers in self.__checkers
        )

class Move:
    def __init__(self, from_x: int = -1, from_y: int = -1, to_x: int = -1, to_y: int = -1):
        self.__from_x = from_x
        self.__from_y = from_y
        self.__to_x = to_x
        self.__to_y = to_y

    @property
    def from_x(self):
        return self.__from_x

    @property
    def from_y(self):
        return self.__from_y

    @property
    def to_x(self):
        return self.__to_x

    @property
    def to_y(self):
        return self.__to_y

    def __str__(self):
        return f'{self.from_x}-{self.from_y} -> {self.to_x}-{self.to_y}'

    def __repr__(self):
        return f'{self.from_x}-{self.from_y} -> {self.to_x}-{self.to_y}'

    def __eq__(self, other):
        if isinstance(other, Move):
            return (
                self.from_x == other.from_x and
                self.from_y == other.from_y and
                self.to_x == other.to_x and
                self.to_y == other.to_y
            )
        return NotImplemented
