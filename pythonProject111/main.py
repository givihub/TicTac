# Инициализация игрового поля
board = [[" " for _ in range(3)] for _ in range(3)]

# Функция для отрисовки игрового поля
def draw_board():
    for row in board:
        print("|".join(row))
        print("-----")

# Функция для проверки выигрышной комбинации
def check_winner(player):
    # Проверка по горизонтали и вертикали
    for i in range(3):
        if all(cell == player for cell in board[i]) or all(row[i] == player for row in board):
            return True
    # Проверка по диагоналям
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# Функция для осуществления хода игрока
def make_move(player, row, col):
    if board[row][col] == " ":
        board[row][col] = player
        return True
    return False

# Основной игровой цикл
def play_game():
    current_player = "X"
    draw_board()
    while True:
        print("Ходит игрок", current_player)
        row = int(input("Введите номер строки (0-2): "))
        col = int(input("Введите номер столбца (0-2): "))
        if make_move(current_player, row, col):
            draw_board()
            if check_winner(current_player):
                print("Игрок", current_player, "победил!")
                break
            if all(all(cell != " " for cell in row) for row in board):
                print("Ничья!")
                break
            current_player = "O" if current_player == "X" else "X"
        else:
            print("Неверный ход. Попробуйте ещё раз.")0

# Запуск игры
play_game()