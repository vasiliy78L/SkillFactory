import sys # проверял отладку и вставлял sys.exit() где мне нужно было
# === Декораторы ===

def with_separator(func):
    """Добавляет разделители сверху и снизу вывода"""
    def wrapper(*args, **kwargs):
        print("\n" + "-" * 15)
        result = func(*args, **kwargs)
        print("-" * 15 + "\n")
        return result
    return wrapper


def log_move(func):
    """Логирует ходы игроков"""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[LOG] Игрок {args[0]} сделал ход: {chr(result[0] + 97)}{result[1] + 1}")
        return result
    return wrapper


def validate_move(func):
    """Проверяет корректность ввода и занятость клетки"""
    def wrapper(player):
        while True:
            move = input(f"Ход игрока {player} (например a1, b3) или 'q' для выхода:").strip().lower()
            if move.lower() =="q":
                print("игра прервана игроком")
                return None
            # Проверка длины и допустимых символов
            if len(move) != 2 or move[0] not in "abc" or move[1] not in "123":
                print("Ошибка ввода! Используйте формат a1, b2, c3.")
                continue

            row, col = ord(move[0]) - 97, int(move[1]) - 1

            if board[row][col] == " ":
                return row, col
            else:
                print("Ошибка: клетка занята. Попробуйте снова.")
    return wrapper

# === Игровое поле ===
board = [[" " for _ in range(3)] for _ in range(3)]


# === Функции ===
@with_separator
def print_board():
    # Отображение поля с буквами и цифрами
    print("  1 2 3")
    for i, row in enumerate(board):
        # заменяем пробелы на точки только при выводе
        display = [cell if cell != " " else "." for cell in row]
        print(chr(97+i), " ".join(display))


def check_win(player):
    for i in range(3):
        # берем строку с индексом i
        # проверяем все ее элементы (j= 0...2)
        #если все три клетки строки равны player (X или O),то это победа
        if all(board[i][j] == player for j in range(3)):
            return True
        # проверка столбцов.Берем столбец с индексом j и проверяем также как и строку
        if all(board[j][i] == player for j in range(3)):
            return True
        # проверка главной диагонали (слева сверху -> вправо вниз)
    if all(board[i][i] == player for i in range(3)):
        return True
        # проверка побочной диагонали (справа с верху -> влево вниз)
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    # ни одно условие не выполнено
    return False


#def no_win_possible():
    """
     Проверяем, может хотя бы один игрок еще победить.
     Если нет - возвращается True (нинья)
    """
 #   for i in range(3):
 #      for j in range(3):
  #         if board[i][j] == " ":
                # временно пробуем ставить Х
  #              board[i][j] = "X"
  #              if check_win("X"):
   #                 board[i][j] = " "
   #                 return False
  #              # временно пробуем ставить O
   #             board[i][j] = "O"
   #             if check_win("O"):
    #                board[i][j] = " "
     #               return False
   #         board[i][j] = " "
   # return True
# пытался проанализировать возможность досрочной ничьей у меня не 
#получилось, если подскажите как буду рад

@validate_move
@log_move
def get_move(player):
    row, col = -1, -1  # заглушки, реальные значения вернёт validate_move
    return row, col
    
# ===основная функция игры===
def main():
    current_player = "X"
    moves = 0

    print_board()  # первое отображение пустого поля

    while True:
        # ход игрока
        result = get_move(current_player)
        if result is None:
            break
        row, col = result
        board[row][col] = current_player

        # вывод поля
        print_board()

        # проверка победы
        if check_win(current_player):
            print(f"🎉 Игрок {current_player} победил!")
            break

        # обновление счётчика и проверка ничьи
        moves += 1
        if moves == 9:
            print("🤝 Ничья!")
            break

        # смена игрока
        current_player = "O" if current_player == "X" else "X"


# условие корректности запуска,чтобы при необходимости импортирования кода в другой файл не произошел автозапуск
if __name__ == "__main__":
    main()