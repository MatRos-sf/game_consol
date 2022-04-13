import time
from math import sqrt, ceil
from random import choice, randint

# size board
X = 5
Y = 10


def commentator(distans):
    distans = ceil(distans)
    comments = ''
    say = {
        1: 'THE HOTTEST',
        2: 'Hotter',
        3: 'hot',
        4: 'cold',
        5: 'Colder',
        6: 'The Coldest'
    }
    if distans == 1:
        comments = say[1]
    elif distans == 2:
        comments = say[2]
    elif distans == 3:
        comments = say[3]
    elif distans == 4:
        comments = say[4]
    elif distans == 5:
        comments = say[5]
    else:
        comments = say[6]

    return comments


def set_key(board, position_player):
    x = randint(0, X - 1)
    y = randint(0, Y - 1)

    if position_player[0] == x and position_player[1] == y:
        y_rang = list(range(0, Y + 1))
        x_rang = list(range(0, X + 1))
        print(x_rang, y_rang, position_player[0], position_player[1])
        y_rang.remove(position_player[1])
        x_rang.remove(position_player[0])
        x = choice(x_rang)
        y = choice(y_rang)
    board[x][y] = 1
    return board, [x, y]


def show_board(board, player_position=[-1, -1]):
    x, y = player_position
    # frame top
    print(' -', end='-')
    for i in range(Y):
        print('-', end='--')
    print()
    # mid board
    for i in range(X):
        print('|', end=' ')
        for j in range(Y):
            if x == i and y == j:
                print('X', end='  ')
            else:
                print(' ', end='  ')
        print('|')
    # frame bot
    print(' ', end='')
    for i in range(Y):
        print('-', end='--')
    print()


def set_board():
    board = []
    for i in range(X):
        tab = []
        for j in range(Y):
            tab.append(0)
        board.append(tab)

    return board


def check_player_position():
    while True:
        try:
            position = input("Wpisz pozycje startu X, Y: ").split(',')
            if len(position) == 2:
                position = [int(i) for i in position]
                if position[0] >= 0 and position[0] < X and position[1] >= 0 and position[1] < Y:
                    break
                else:
                    print("Poza skale")
            else:
                print("Za dużo liczb wpisałeś")
        except ValueError:
            print("Liczby oddzielone ',' !!!")
    return position


def movement(current_position):
    x, y = current_position
    while True:
        move = input("Your move: ")
        if move.lower() == 'w' and x - 1 >= 0:
            current_position = [x - 1, y]
            break
        elif move.lower() == 'd' and y + 1 < Y:
            current_position = [x, y + 1]
            break
        elif move.lower() == 's' and x + 1 < X:
            current_position = [x + 1, y]
            break
        elif move.lower() == 'a' and y - 1 >= 0:
            current_position = [x, y - 1]
            break
        else:
            print("Zły zmienn kierunkowa lub wyszedłeś poza zakres mapy. Ifon: możesz poruszać się tylko: w,s,a,d")
    return current_position


def distance(key, player):
    x_key, y_key = key
    x_player, y_player = player
    return sqrt(pow((x_key - x_player), 2) + pow((y_key - y_player), 2))


def main_game():
    board = set_board()
    show_board(board)
    player_position = check_player_position()

    board, position_key = set_key(board, player_position)
    steps = 0
    start = time.time()
    while True:
        show_board(board, player_position)
        player_position = movement(player_position)
        steps += 1
        if player_position == position_key:
            print("You found key ;)")
            break
        else:
            d = distance(position_key, player_position)
            print(commentator(d))
    print(f"Wykonałeś {steps} ruchów.\n"
          f"Twój czas to: {round(time.time() - start)}s")


if __name__ == '__main__':
    main_game()
