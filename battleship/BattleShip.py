import random

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.length = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        cur_x, cur_y = self.bow.x, self.bow.y
        for i in range(self.length):
            ship_dots.append(Dot(cur_x, cur_y))
            cur_x += self.o.x
            cur_y += self.o.y
        return ship_dots


class Board:
    def __init__(self, size, hid=False):
        self.size = size
        self.hid = hid
        self.field = [['O' for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.busy = set()

    def __str__(self):
        res = '   | ' + ' | '.join(map(str, range(1, self.size + 1))) + ' |'
        for i, row in enumerate(self.field):
            res += f'\n{i + 1:2} | ' + ' | '.join(row) + ' |'
        if self.hid:
            res = res.replace('■', 'O')
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2)]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not self.out(cur) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.add(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                return False
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.add(d)

        self.ships.append(ship)
        self.contour(ship)
        return True

    def add_ships_randomly(self):
        ships = [3, 2, 2, 1, 1, 1, 1]
        for l in ships:
            while True:
                ship = Ship(Dot(random.randint(0, self.size), random.randint(0, self.size)), l, Dot(random.randint(-1, 1), random.randint(-1, 1)))
                if self.add_ship(ship):
                    break


class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                if repeat:
                    continue
                else:
                    break
            except ValueError:
                print("Некорректные координаты! Введите координаты выстрела еще раз.")


class AI(Player):
    def ask(self):
        return Dot(random.randint(0, 5), random.randint(0, 5))


class User(Player):
    def ask(self):
        coords = input("Введите координаты выстрела (например, 1 3): ").split()
        if len(coords) != 2:
            raise ValueError("Неверный формат ввода! Введите две координаты через пробел.")
        x, y = map(int, coords)
        return Dot(x - 1, y - 1)


class Game:
    def __init__(self):
        size = 6
        self.player = User(Board(size), Board(size, hid=True))
        self.ai = AI(Board(size), Board(size, hid=True))

    def greet(self):
        print("Добро пожаловать в игру Морской бой!")
        print("Формат ввода координат выстрела: x y (например, 1 3)")

    def loop(self):
        num_ships = len(self.player.board.ships) + len(self.ai.board.ships)
        while True:
            print("-" * 20)
            print("Ваша доска:")
            print(self.player.board)
            print("-" * 20)
            print("Доска врага:")
            print(self.player.enemy_board)
            print("-" * 20)
            if len(self.player.board.ships) < num_ships and len(self.ai.board.ships) < num_ships:
                print("Ваш ход!")
                self.player.move()
            else:
                break

            print("-" * 20)
            print("Ваша доска:")
            print(self.player.board)
            print("-" * 20)
            print("Доска врага:")
            print(self.player.enemy_board)
            print("-" * 20)
            if len(self.player.board.ships) < num_ships and len(self.ai.board.ships) < num_ships:
                print("Ход компьютера!")
                self.ai.move()
            else:
                break

    def start(self):
        self.greet()
        self.player.board.add_ships_randomly()
        self.ai.board.add_ships_randomly()
        self.loop()


if __name__ == '__main__':
    game = Game()
    game.start()