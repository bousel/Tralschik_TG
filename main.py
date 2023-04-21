from random import sample as rt

class Cell:

    def __init__(self, is_mine:bool=False, around_mines:int=0) -> None:
        self.is_mine = is_mine
        self.around_mines = around_mines
        self.is_opened:bool = False


class GamePole:

    def __init__(self, n, m) -> None:
        """
        Создает игровое поле размером n*n с m минами
        int n - размерность игрового поля
        int m - количество мин на поле
        """
        self.pole = [[Cell() for i in range(n)] for j in range(n)]
        mns = [[i%n, i//n] for i in rt(range(n*n),m)]