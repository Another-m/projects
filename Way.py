# Генератор пустого поля
def field_gen(field):
    for i in range(field_vertical):
        field.append([-1] * field_horizont)

# размер поля (можно изменить в коде)
field_horizont = 8
field_vertical = 4

# массив поля
field = []
field_gen(field)

# Доп. данные (меняются в коде)
# Точки А и В на маршруте, А = -2, В = -3, пустые поля = -1 (стоят по умолчанию)
field[3][1] = -2
field[1][-1] = -3
# Преграды на пути, обозначаются буквой П = -4
field[1][2] = -4
field[2][3] = -4
field[3][3] = -4

# Глобальные переменные
mas_of_way = []
mas_of_ways = []
variant = 0

# Основное вычисление
def calculate(field):
    new_step = 0
    for i in range(len(field)):
        for y in range(len(field[i])):
            if field[i][y] == -2:
                A = [i, y]   # Место старта, клетка А
            if field[i][y] == -3:
                B = [i, y]   # Место прибытия, клетка В
    steps_func(A, new_step)
    calculate_part2(field, B)

# Вторая часть функции (разбита на 2 части для оптимизации скорости загрузки доп.вариантов)
def calculate_part2(field, B):
    temp_mas_m = []
    temp_mas = []
    temp_place = []
    result_mas = []
    for i in range(len(mas_of_ways)-1, -1, -1):
        temp_mas.append(mas_of_ways[i])
        if mas_of_ways[i][2] == 1: temp_mas_m.append(mas_of_ways[i][3])
    try: min_stp = min(temp_mas_m)
    except: return print('\n В данных условиях проложить маршрут невозможно!')
    for y in range(len(temp_mas)):
        if temp_mas[y][2] == 1 and temp_mas[y][3] == min_stp:
            temp_place.append(y)
    N_var = len(temp_place)
    for y in range(len(temp_mas)):
        if y >= temp_place[variant]:
            if result_mas == [] or temp_mas[y][3] < result_mas[-1][3]:
                result_mas.append(temp_mas[y])
                if temp_mas[y][3] == 1: break
    for y in range(len(result_mas)):
        if y > 0:
            field[result_mas[y][0]][result_mas[y][1]] = result_mas[y][3]
    result_way(field, B)
    for y in range(len(result_mas)):
        if y > 0: field[result_mas[y][0]][result_mas[y][1]] = -1
    input_var(N_var, B)

# перебор ходов (рекурсивная функция)
def steps_func(A, new_step):
    global mas_of_ways
    variants_of_step = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    steps_of_way = []
    new_step += 1
    for j in variants_of_step:
        newstep_v = A[0]+j[0]   # новый предполагаемый вертикальный шаг
        newstep_h = A[1]+j[1]   # новый предполагаемый горизонтальный шаг
        if newstep_v < 0 or newstep_h < 0 or newstep_v > field_vertical-1 or newstep_h > field_horizont-1: pass
        else:
            # Отбор возможных вариантов маршрутов
            if field[newstep_v][newstep_h] == -3:
                step = [newstep_v, newstep_h, 1]
                steps_of_way.append(step)
                steps_of_way.append('B')
            elif field[newstep_v][newstep_h] != -1: pass
            else:
                step = [newstep_v, newstep_h, 0]
                steps_of_way.append(step)
    if "B" in steps_of_way:
        for i in steps_of_way:
            if i != "B" and i[2] == 1:
                i.append(new_step)
                mas_of_ways.append(i)
    else:
        for i in steps_of_way:
            if i[2] == 0:
                field[i[0]][i[1]] = new_step
                i.append(new_step)
                mas_of_ways.append(i)
                A = [i[0], i[1]]
                steps_func(A, new_step)
                field[i[0]][i[1]] = -1

# Ввод данных с клавиатуры (выбор варианта)
def input_var(N_var, B):
    global variant
    print(f'Найдено {N_var} кратчайших варианта. Если хотите выбрать другой вариант')
    variant = int(input('Введите номер следующего варианта: '))
    if variant > 0 and variant <= N_var:
        variant -= 1
        calculate_part2(field, B)
    else:
        print('Вы ввели неверное число')
        input_var(N_var, B)

# результат
def result_way(field, B):
    count_steps = 0
    step_mas = []
    for i in range(len(field)):
        for y in range(len(field[i])):
            if field[i][y] > 0:
                count_steps += 1
                step_mas.append([i, y])
    step_mas.append(B)
    count_steps += 1
    print_field(field, count_steps, step_mas)

# Функция печати
def print_field(field, count_steps, step_mas):
    x = {'-1': '*', '-4': 'П', '-2': 'A', '-3': 'B'}
    for print_f in field:
        print_f = ' | '.join([str(i) for i in print_f])
        for i in x.keys():
            print_f = print_f.replace(i, x[i])
        print("----" * field_horizont)
        print(' ', print_f)
    print("----" * field_horizont)
    print()
    print(f'Вариант №{variant+1}')
    print("Количество шагов:", count_steps)
    print('Шаги:', step_mas)
    print()

calculate(field)
