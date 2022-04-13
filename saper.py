from random import sample

# size board, Don't set X>10!!
X = 8

# amount bombs
BOMBS = 5


def where_is_bomb(tab_game):
    """
    Wstawiamy na każdej pole liczbę min, które bezpośrednio stykają się z danym polem (0-8)
    """

    tab_len = len(tab_game) - 1  # maksymalna pozycja
    for x in range(tab_len + 1):
        for y in range(tab_len + 1):
            bombs = 0
            if tab_game[x][y] == 'X' or tab_game[x][y] == 'O':   continue
            # check top: czemu -1 bo jest to lista a lista zaczyna się od 0 czyli żeby iść w górę to trzeba dać -1
            if x - 1 >= 0:
                if tab_game[x - 1][y] == 'X':    bombs += 1
            # check top right
            if x - 1 >= 0 and y + 1 <= tab_len:
                if tab_game[x - 1][y + 1] == 'X':    bombs += 1
            # check right
            if y + 1 <= tab_len:
                if tab_game[x][y + 1] == 'X':      bombs += 1
            # check bot right
            if x + 1 <= tab_len and y + 1 <= tab_len:
                if tab_game[x + 1][y + 1] == 'X':   bombs += 1
            # check bot
            if x + 1 <= tab_len:
                if tab_game[x + 1][y] == 'X':     bombs += 1
            # check bot-left
            if x + 1 <= tab_len and y - 1 >= 0:
                if tab_game[x + 1][y - 1] == 'X':   bombs += 1
            # check lef
            if y - 1 >= 0:
                if tab_game[x][y - 1] == 'X':     bombs += 1
            # check top left
            if x - 1 >= 0 and y - 1 >= 0:
                if tab_game[x - 1][y - 1] == 'X':   bombs += 1

            if bombs > 0:
                GREEN = '\33[92m'
                ENDGREEN = '\33[0m'
                tab_game[x][y] = GREEN + str(bombs) + ENDGREEN

    return tab_game


def exposure_boar(tab_game, tab_game_show, your_click):
    len_tab = len(tab_game) - 1
    x, y = your_click
    if tab_game[x][y] == 'X':   return False
    tab_game_show[x][y] = ' '
    # top
    if x - 1 >= 0:
        if tab_game_show[x - 1][y] == '?':
            if tab_game[x - 1][y] == '?':
                tab_game_show[x - 1][y] = ' '
                tab_game_show = exposure_boar(tab_game, tab_game_show, (x - 1, y))
            elif tab_game[x - 1][y] != 'X':
                tab_game_show[x - 1][y] = tab_game[x - 1][y]
    # bot
    if x + 1 <= len_tab:
        if tab_game_show[x + 1][y] == '?':
            if tab_game[x + 1][y] == '?':
                tab_game_show[x + 1][y] = ' '
                tab_game_show = exposure_boar(tab_game, tab_game_show, (x + 1, y))
            elif tab_game[x + 1][y] != 'X':
                tab_game_show[x + 1][y] = tab_game[x + 1][y]
    # right
    if y + 1 <= len_tab:
        if tab_game_show[x][y + 1] == '?':
            if tab_game[x][y + 1] == '?':
                tab_game_show[x][y + 1] = ' '
                tab_game_show = exposure_boar(tab_game, tab_game_show, (x, y + 1))
            elif tab_game[x][y + 1] != 'X':
                tab_game_show[x][y + 1] = tab_game[x][y + 1]
    # left
    if y - 1 >= 0:
        if tab_game_show[x][y - 1] == '?':
            if tab_game[x][y - 1] == '?':
                tab_game_show[x][y - 1] = ' '
                tab_game_show = exposure_boar(tab_game, tab_game_show, (x, y - 1))
            elif tab_game[x][y - 1] != 'X':
                tab_game_show[x][y - 1] = tab_game[x][y - 1]
    return tab_game_show


def show_board(board):
    """
    Funkcja, która wyświetla widoczną tablice dla gracza
    """
    global X
    CRED = '\033[100m'
    CEND = '\033[0m'
    print(CRED + '  ', end='')
    for i in range(X):
        print(str(i), end='  ')
    print(CEND)
    for i in range(X):
        print(CRED + str(i), end=' ')
        print(CEND + ' |'.join(board[i]))


def make_save_position(position):
    """
    Funkcja która zwraca listę bezpiecznych pozycji na której nie powinno być bomby
    :return: list of number save positions
    """
    global X
    if position[0] == 0:
        position = position[1]
    else:
        position = position[0] * (X - 1) + position[1] + 1
    save_position = [position - X - 1, position - X, position - X + 1,
                     position - 1, position, position + 1,
                     position + X - 1, position + X, position + X + 1]
    return save_position


def create_bomb(first_position):
    """
    Funkcja, tworząca pozycje bomb
    :return: lista z pozycjami bomb
    """
    global X, BOMBS
    save_position = make_save_position(first_position)
    range_position = [i for i in range(0, (X * X)) if i not in save_position]

    position = sorted(list(sample(range_position, BOMBS)))
    f = lambda x: divmod(x, X)
    return list(map(f, position))


def put_bombs(board, bomb_position):
    """
    funkcja, która umieszcza bomby na tablicy która nie jest widoczna dla gracza

    """
    for bomb in bomb_position:
        board[bomb[0]][bomb[1]] = 'X'


def movement():
    # wpisz liczbe od 0,X-1 dla x i y
    # zrobić zabezpieczenie
    position = input("X, Y: ").split(',')
    if len(position) == 3:
        return True, int(position[0]), int(position[1])
    else:
        return False, int(position[0]), int(position[1])


def probably_bomb(prob_position, prob, tab_game, tab_game_show):
    # pozycje prawdopodobną, tablica z prawdopodobną bombą,
    x, y = prob_position
    # color
    RED = '\33[41m'
    ENDRED = '\33[0m'
    if prob_position in prob:
        print("Odznaczono bombe")
        tab_game_show[x][y] = '?'
        prob.remove((x, y))

    elif tab_game_show[x][y] == '?':
        prob.append((x, y))
        tab_game_show[x][y] = RED + 'X' + ENDRED

    return tab_game_show, prob


def is_not_quetion_tag(tab_game_show, no_bombs):
    """
    Funkcja sprawdzająca ile zostało znaków ?
    :param tab_game_show: tablica którą widzi gracz
    :param no_bombs: liczba bomb
    :return:
    """
    len_tab = len(tab_game_show)
    count_q_t = 0
    for i in range(len_tab):
        for j in range(len_tab):
            if tab_game_show[i][j] == '?':
                count_q_t += 1
            if count_q_t > no_bombs:      return False
    return True


if __name__ == '__main__':

    # tworzenie 2 podobnych tablic: tab_game - pomocnicza, tab_game_show - widoczna dla gracza
    tab_game = [['?' for j in range(X)] for i in range(X)]
    tab_game_show = [['?' for j in range(X)] for i in range(X)]

    print('Jeśli chcesz zaznaczyć miejsce bomby wpisz: X, Y,b')
    # lista prawdopodobnych bomb zaznaczona przez gracza
    prob_bombs = []
    # first step
    b, *m = movement()
    # tworzenie i umieszczanie bomb
    bombs = create_bomb(m)
    put_bombs(tab_game, bombs)
    tab_game = where_is_bomb(tab_game)
    tab_game_show = exposure_boar(tab_game, tab_game_show, m)

    while True:
        # if win, it breaks loop
        if prob_bombs == bombs or is_not_quetion_tag(tab_game_show, BOMBS):
            print("You win!")
            break

        print(f"\nZaznaczono {len(prob_bombs)}/{BOMBS} bomb.")

        show_board(tab_game_show)

        b, *m = movement()

        if b:
            # zaznaczyć bombe
            tab_game_show, prob_bombs = probably_bomb(m, prob_bombs, tab_game, tab_game_show)
        else:
            tab_game_show = exposure_boar(tab_game, tab_game_show, m)

            if not tab_game_show:
                print("Lost")
                break
