from random import randint

# распечатываем доску
def print_board(board):
    x = {'-1': ' ', '1': 'X'}
    for board_line in board:
        print_b = (' | '.join([str(i) for i in board_line]))
        for i in x.keys():
            print_b = print_b.replace(i, x[i])
        print("----" * b_size)
        print(' ', print_b)
    print("----"*b_size)
    G_Rate = game_rating(board)
    if G_Rate == 0: print('Победа! Выиграли нолики')
    if G_Rate == 1: print('Победа! Выиграли крестики')
    if G_Rate == 2: print('Ничья')
    if G_Rate == 3: print('Игра продолжается')
    if G_Rate == 4: print('Игра началась')
    print()

# Кто ходит первым
def who_move_first():
    global user
    global comp
    level = input('Введите уровень сложности \"1\" либо \"2\":')
    if level != '1' and level != '2':
        print("Вы не ввели нужного значения, попробуйте ещё раз")
        return who_move_first()
    text_choose = ("Выберите чем будете ходить. Крестики ходят первыми. Введите X ли 0: ")
    userinp = input(text_choose)
    if userinp == "x"  or userinp == "X" or userinp == "х" or userinp == "Х":
        user = 1
        print("Вы играете крестиками")
    elif userinp == "0" or userinp == "o" or userinp == "O" or userinp == "о" or userinp == "О":
        user = 0
        print("Вы играете ноликами, первым ходит компьютер")
    else:
        print("Вы не ввели нужного значения, попробуйте ещё раз")
        return who_move_first()
    if user == 1:  # user - чем играет человек
        comp = 0   # comp - чем играет комп
        user_move(level)  # крестики - цифра 1, нолики - 0
    else:
        comp = 1
        comp_play(board, level)

# Ход человека
def user_move(level):
    if game_rating(board) == 3 or game_rating(board) == 4:
        text_for_user = (f"Введите номер ячейки от 00 до {b_size}{b_size}, чтобы сделать свой ход ")
        userinp = list(input(text_for_user))
        board[int(userinp[0])][int(userinp[1])] = user
        comp_play(board, level)
    else: print("Игра закончена")

# ход компа
def comp_play(board, level):
    # Запрашиваем лучший ход у рекурсивной функции
    if level == '1': bs = game_lite(board)
    if level == '2': bs = smart_game(board, user)
    # Компьютер делает свой ход
    if bs != 0: board[bs[0]][bs[1]] = comp
    print_board(board)
    user_move(level)

# Ход компа простой
def game_lite(board):
    mas_move = []
    if game_rating(board) <= 2:  # Проверка доски перед ходом
        return 0
    else:
        for player_move in range(0, 2):
            for i in range(b_size):
                for j in range(b_size):
                    if board[i][j] == -1:
                        board[i][j] = player_move  # Поочередно присваиваем ходы человека и компа
                        list_user_move = [i, j, game_rating(board)]  # Ход ij, чем ходим и результат хода человека
                        mas_move.append(list_user_move)  # Выводим в список
                        board[i][j] = -1
        # Разбиваем массив с ходами на выигрышные, проигрышные и ничьи
        mas_move_u = []
        mas_move_c = []
        mas_move3 = []
        for move in mas_move:
            if move[2] == user: mas_move_u.append(move)
            if move[2] == comp: mas_move_c.append(move)
            if move[2] == 3 or move[2] == 2: mas_move3.append(move)
        # Выбираем лучший ход и ходим рандомным из лучших
        best_move = []
        if mas_move_c != []: best_move = mas_move_c
        elif mas_move_c == [] and mas_move_u != []: best_move = mas_move_u
        elif mas_move_c == [] and mas_move_u == []: best_move = mas_move3
        rand = best_move[randint(0, len(best_move) - 1)]
        return rand

# Рекурсивная функция умного хода
def smart_game(board, t):
    mas_move = []
    t += 1  # Счетчик кол-ва рекурсий
    if t % 2 == 0: player_move = 0  # Четное кол-во рекурсий = ход 0
    else: player_move = 1           # нечетное = x

    if game_rating(board) <= 2:  # Проверка доски перед ходом
        return 0
    else:
        for i in range(b_size):
            for j in range(b_size):
                if board[i][j] == -1:   # Если на доске есть пустые ячейки
                    board[i][j] = player_move  # Делаем ход за игрока (компа либо человека)
                    status = game_rating(board)
                    # Если результат хода "игра продолжается",
                    # рекурсивным методом запрашиваем результат будущих ходов
                    if status == 3:
                        status = smart_game(board, t)[2]
                    list_user_move = [i, j, status]  # Записываем в массив результат хода игрока
                    mas_move.append(list_user_move)  # Добавляем ходы в массив
                    board[i][j] = -1
        # Выбираем рандомный из лучших ходов и возвращаем его
        best_move = []
        best_move = [i for i in mas_move if i[2] == player_move]
        if best_move == []: best_move = [i for i in mas_move if i[2] == 2]
        if best_move == []: best_move = mas_move
        rand = best_move[randint(0, len(best_move) - 1)]
        return rand

# анализ хода, функция возвращает:
# 0 = Выиграли нолики 1 = Выиграли крестики
# 2 = Ничья, 3 = Игра продолжается, 4 = Игра началась
def game_rating(board):
    mas_of_lines = []
    # добавляем в brd_temp строки
    for i in range(b_size):
        mas_of_lines.append(board[i])

    # добавляем в brd_temp столбцы в виде строк
    for i in range(len(board)):
        brd_temp_line = []
        for j in range(len(board)):
            brd_temp_line.append(board[j][i])
        mas_of_lines.append(brd_temp_line)

    # добавляем в brd_temp диагонали
    mas_of_lines.append([])
    mas_of_lines.append([])
    for i in range(b_size):
        mas_of_lines[b_size * 2].append(board[i][i])
        mas_of_lines[b_size * 2 + 1].append(board[b_size - i - 1][i])

    # к этому моменту в массиве brd_temp содержится массив одномерных массивов
    # сначала строка, потом столбцы и потом две диагонали
    win1 = [1 for i in range(b_size)]  # = массив из единичек равный размеру доски
    win0 = [0 for i in range(b_size)]  # = массив из ноликов равный размеру доски

    # смотрим все линии на предмет выигрышных
    number_line = 0
    minus_one_quantity = 0
    for line in mas_of_lines:
        # ---------------------------------------------------
        if (number_line < b_size):
            for i in range(b_size):
                if (line[i] == -1): minus_one_quantity += 1
        number_line += 1
        # ---------------------------------------------------
        if line == win1:  # = если победили крестики
            return 1
        if line == win0:  # = если победили нолики
            return 0
    # к этому моменту мы точно знаем, что никто не выиграл
    # если все -1, тогда вернём 4 (игра началась)
    if (minus_one_quantity == b_size * b_size):
        return 4
    # осталось выдать 2 или 3
    # если ни одной -1, тогда вернём 2 (ничья)
    if (minus_one_quantity == 0):
        return 2
    # осталось выдать 3 (игра продолжается)
    return 3

b_size = 3
# Формируем пустую доску в виде двумерного массива
board = []
for i in range(b_size):
    board.append([-1] * b_size)

print_board(board)
who_move_first()
