class BoardOutException(Exception):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x + i * self.o.x
            cur_y = self.bow.y + i * self.o.y
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.field = [['O'] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardOutException()
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)

    def __str__(self):
        res = ''
        res += ' | 1 | 2 | 3 | 4 | 5 | 6 |\n'
        for i, row in enumerate(self.field):
            res += f'{i + 1} | ' + ' | '.join(row) + ' |\n'
        if self.hid:
            res = res.replace('■', 'O')
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль подбит!")
                    return True

        self.field[d.x][d.y] = 'T'
        print("Промах!")
        return False
class BoardUsedException(Exception):
    pass

class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                result = self.enemy_board.shot(target)
                return result
            except BoardOutException:
                print("Аут!")
            except BoardUsedException:
                print("Вы уже стреляли сюда!")
            except Exception as e:
                print(e)

class User(Player):
    def ask(self):
        while True:
            try:
                x, y = map(int, input("Введите координаты выстрела (например, 1 3): ").split())
                return Dot(x - 1, y - 1)
            except ValueError:
                print("Введите корректные координаты!")

class AI(Player):
    def ask(self):
        x, y = random.randint(0, 5), random.randint(0, 5)
        return Dot(x, y)

class Game:
    def __init__(self):
        self.size = 6
        self.board = Board()
        self.enemy_board = Board(hid=True)
        self.player = User(self.board, self.enemy_board)
        self.ai = AI(self.enemy_board, self.board)

    def greet(self):
        print("Добро пожаловать в игру Морской бой!")
        print("Формат ввода координат выстрела: x y (например, 1 3)")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Ваша доска:")
            print(self.board)
            print("-" * 20)
            print("Доска противника:")
            print(self.enemy_board)
            if num % 2 == 0:
                if self.player.move():
                    num -= 1
            else:
                if self.ai.move():
                    num -= 1

            if self.enemy_board.ships == 0:
                print("Вы победили!")
                break
            if self.board.ships == 0:
                print("Компьютер победил!")
                break

            num += 1

    def start(self):
        self.greet()
        self.board.random_board()
        self.enemy_board.random_board()
        self.loop()

if __name__ == "__main__":
    game = Game()
    game.start()