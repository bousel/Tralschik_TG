from random import sample as rt

class Cell:

    def __init__(self, is_mine:bool=False, around_mines:int=0) -> None:
        """
        Создание объекта ячейки
        """
        self.is_mine = is_mine
        self.around_mines = around_mines
        self.is_opened:bool = False
    
    def __str__(self) -> str:
        if not self.is_opened:
            return "#"
        else:
            if self.is_mine:
                return "*"
            else:
                return f"{self.around_mines}"


class GamePole:

    opened = 0

    def __init__(self, n=10, m=7) -> None:
        """
        Создает игровое поле размером n*n с m минами
        int n - размерность игрового поля
        int m - количество мин на поле
        """
        self.n = n
        self.m = m
        self.to_open = n*n - m
        self.pole = [[Cell() for _ in range(n)] for _ in range(n)]
        self.mines = rt(range(n*n), m)
        for mine in self.mines:
            row = mine // n
            col = mine % n
            self.pole[row][col].is_mine = True
            for r in range(row-1, row+2):
                for c in range(col-1, col+2):
                    if 0 <= r < n and 0 <= c < n and not self.pole[r][c].is_mine:
                        self.pole[r][c].around_mines += 1
    
    def show(self) -> str:
        return "\n".join([" ".join([str(cell) for cell in row]) for row in self.pole])

    def open(self, x, y):
        if self.to_open == self.opened:
            return self.gameover() + "\n\n" + "Вы открыли все ячейки. Игра окончена", False
        
        cell = self.pole[y][x]
        if cell.is_opened:
            return f"Ячейка ({x};{y}) уже открыта", True
        else:
            if cell.is_mine:
                return self.gameover() + "\n\n" + "Вы подорвались на мине. Игра окончена", False
            else:
                cell.is_opened = True
                self.opened += 1
                if cell.around_mines == 0:
                    for r in range(x-1, x+2):
                        for c in range(y-1, y+2):
                            if 0 <= r < self.n and 0 <= c < self.n and not self.pole[c][r].is_mine:
                                self.open(r, c)
                    return "Ячейки открыты", True
                if self.to_open == self.opened:
                    return self.gameover() + "\n\n" + "Вы открыли все ячейки. Игра окончена", False
                return "Ячейка открыта", True

    
    def gameover(self):
        for row in self.pole:
            for cell in row:
                cell.is_opened = True
        return self.show()
                    

def play(n, m):
    """
    Рабочая функция для игры. 
    Отсутствует только проверка неверно введенных координат.
    Позже это будет решаться непосредственно в файле бота
    """
    p = GamePole(n, m)
    cont:bool = True
    while cont:
        print(p.show())
        x, y = map(int, input("x y = ").split())
        txt, cont = p.open(x-1, y-1)
        print(txt)