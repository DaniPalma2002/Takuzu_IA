# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 001:
# 99194 Daniel Pereira
# 99245 Joao Santos

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, board, size):
        self.board = board
        self.size = size

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def make_move(self, row: int, col: int, n: int):
        """Altera uma posicao do tabuleiro"""
        self.board[row][col] = n

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        up = None
        if row != 0:
            up = self.get_number(row - 1, col)
        down = None
        if row != self.size - 1:
            down = self.get_number(row + 1, col)

        return down, up

    def number_of_free_spaces_in_the_same_row_and_column(self, row: int, col: int) -> int:
        res = self.number_of_empty_squares() * 10 + self.number_of

        for j in range(self.size):
            if self.get_number(row, j) == 2:
                res += 1
        for i in range(self.size):
            if self.get_number(i, col) == 2:
                res += 1

        return res

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        left = None
        if col != 0:
            left = self.get_number(row, col - 1)
        right = None
        if col != self.size - 1:
            right = self.get_number(row, col + 1)

        return left, right

    def there_are_no_more_than_two_adjacent_numbers(self):
        for row in range(self.size):
            for col in range(self.size):
                number = self.get_number(row, col)
                if self.adjacent_vertical_numbers(row, col).count(number) == 2 or \
                        self.adjacent_horizontal_numbers(row, col).count(number) == 2:
                    return False
        return True

    def there_are_no_more_than_two_adjacent_numbers_2(self):
        for row in range(self.size):
            for col in range(self.size):
                number = self.get_number(row, col)
                l0 = self.adjacent_vertical_numbers(row, col)
                l1 = self.adjacent_horizontal_numbers(row, col)
                if number != 2 and ((l0[0] == l0[1] == number) or (l1[0] == l1[1] == number)):
                    return False
        return True

    def there_are_no_more_than_2_adjacent_near_by(self, row, col):
        start_row = max(row - 1, 0)
        stop_row = min(row + 2, self.size)
        start_col = max(col - 1, 0)
        stop_col = min(col + 2, self.size)

        for i in range(start_row, stop_row):
            for j in range(start_col, stop_col):
                number = self.get_number(i, j)
                avn = self.adjacent_vertical_numbers(i, j)
                ahn = self.adjacent_horizontal_numbers(i, j)
                if (avn[0] == avn[1] == number != 2) or (ahn[0] == ahn[1] == number != 2):
                    return False
        return True

    def solvable(self):
        return self.difference_between_number_of_1s_and_0s_per_row_and_column_is_fine_2() and \
               self.all_rows_are_different_2() and \
               self.all_columns_are_different_2()

    def two_adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""

        if row <= 1:
            up = None
            upup = None
        else:
            up = self.get_number(row - 1, col)
            upup = self.get_number(row - 2, col)
        if row >= self.size - 2:
            down = None
            downdown = None
        else:
            down = self.get_number(row + 1, col)
            downdown = self.get_number(row + 2, col)

        return downdown, down, up, upup

    def two_adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        if col <= 1:
            left = None
            leftleft = None
        else:
            left = self.get_number(row, col - 1)
            leftleft = self.get_number(row, col - 2)
        if col >= self.size - 2:
            right = None
            rightright = None
        else:
            right = self.get_number(row, col + 1)
            rightright = self.get_number(row, col + 2)

        return left, leftleft, right, rightright

    def correct_move(self, row: int, col: int, number: int) -> bool:
        l3 = self.adjacent_vertical_numbers(row, col)
        l4 = self.adjacent_horizontal_numbers(row, col)
        l1 = self.two_adjacent_horizontal_numbers(row, col)
        l2 = self.two_adjacent_vertical_numbers(row, col)
        return (number != l1[0] == l1[1] != 2 and l1[0] != None) or \
               (number != l1[2] == l1[3] != 2 and l1[2] != None) or \
               (number != l2[0] == l2[1] != 2 and l2[0] != None) or \
               (number != l2[1] == l2[2] != 2 and l2[2] != None) or \
               number != l3[0] == l4[1] != 2

    def possible_moves(self):
        """Returns a list of possible moves, every possible move is like (row, col, number)"""
        res = []
        for row in range(self.size):
            for col in range(self.size):
                if self.get_number(row, col) == 2:
                    self.make_move(row, col, 0)
                    a = self.there_are_no_more_than_2_adjacent_near_by(row, col) and self.solvable()

                    self.make_move(row, col, 1)
                    b = self.there_are_no_more_than_2_adjacent_near_by(row, col) and self.solvable()


                    self.make_move(row, col, 2)

                    if a and not b:
                        return [(row, col, 0)]
                    elif b and not a:
                        return [(row, col, 1)]
                    elif a and b:
                        res.append((row, col, 0))
                        res.append((row, col, 1))
                    else:
                        return []
        return res

    def all_rows_are_different_2(self):
        for row1 in range(self.size):
            for row2 in range(row1 + 1, self.size):
                for col in range(self.size):
                    if self.get_number(row1, col) != self.get_number(row2, col) or self.get_number(row1, col) == 2:
                        break
                    if col == self.size - 1:
                        return False
        return True

    def all_positions_are_filled(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.get_number(row, col) == 2:
                    return False
        return True

    def all_rows_are_different(self):
        for row1 in range(self.size):
            for row2 in range(row1 + 1, self.size):
                for col in range(self.size):
                    if self.get_number(row1, col) != self.get_number(row2, col):
                        break
                    if col == self.size - 1:
                        return False
        return True

    def all_columns_are_different_2(self):
        for col1 in range(self.size):
            for col2 in range(col1 + 1, self.size):
                for row in range(self.size):
                    if self.get_number(row, col1) != self.get_number(row, col2) or self.get_number(row, col1) == 2:
                        break
                    if row == self.size - 1:
                        return False
        return True

    def all_columns_are_different(self):
        for col1 in range(self.size):
            for col2 in range(col1 + 1, self.size):
                for row in range(self.size):
                    if self.get_number(row, col1) != self.get_number(row, col2):
                        break
                    if row == self.size - 1:
                        return False
        return True

    def number_of_empty_squares_in_row(self, row):
        counter = 0
        for col in range(self.size):
            if self.get_number(row, col) == 2:
                counter += 1
        return counter

    def number_of_empty_squares_in_col(self, col):
        counter = 0
        for row in range(self.size):
            if self.get_number(row, col) == 2:
                counter += 1
        return counter

    def difference_between_number_of_1s_and_0s_per_row_and_column_is_fine_2(self):
        if self.size % 2 == 0:
            for row in range(self.size):
                if self.difference_between_0s_and_1s_in_row(row) > self.number_of_empty_squares_in_row(row):
                    return False
            for col in range(self.size):
                if self.difference_between_0s_and_1s_in_col(col) > self.number_of_empty_squares_in_col(col):
                    return False
        else:
            for row in range(self.size):
                if self.difference_between_0s_and_1s_in_row(row) > self.number_of_empty_squares_in_row(row) + 1:
                    return False
            for col in range(self.size):
                if self.difference_between_0s_and_1s_in_col(col) > self.number_of_empty_squares_in_col(col) + 1:
                    return False

        return True

    def difference_between_number_of_1s_and_0s_per_row_and_column_is_fine(self):
        if self.size % 2 == 0:
            for row in range(self.size):
                if self.difference_between_0s_and_1s_in_row(row) != 0:
                    return False
            for col in range(self.size):
                if self.difference_between_0s_and_1s_in_col(col) != 0:
                    return False
        else:
            for row in range(self.size):
                if self.difference_between_0s_and_1s_in_row(row) > 1:
                    return False
            for col in range(self.size):
                if self.difference_between_0s_and_1s_in_col(col) > 1:
                    return False

        return True

    def number_of_empty_squares(self):
        res = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.get_number(row, col) == 2:
                    res += 1
        return res

    def number_of_1s_in_row(self, row):
        count = 0
        for i in range(self.size):
            if self.get_number(row, i) == 1:
                count += 1
        return count

    def number_of_1s_in_col(self, col):
        count = 0
        for i in range(self.size):
            if self.get_number(i, col) == 1:
                count += 1
        return count

    def number_of_0s_in_row(self, row):
        count = 0
        for i in range(self.size):
            if self.get_number(row, i) == 0:
                count += 1
        return count

    def number_of_0s_in_col(self, col):
        count = 0
        for i in range(self.size):
            if self.get_number(i, col) == 0:
                count += 1
        return count

    def difference_between_0s_and_1s_in_col(self, col):
        return abs(self.number_of_0s_in_col(col) - self.number_of_1s_in_col(col))

    def difference_between_0s_and_1s_in_row(self, row):
        return abs(self.number_of_0s_in_row(row) - self.number_of_1s_in_row(row))

    def imbalance_value(self):
        imbalance = 0
        for i in range(self.size):
            imbalance += self.difference_between_0s_and_1s_in_row(i)
            imbalance += self.difference_between_0s_and_1s_in_col(i)
        return imbalance

    def number_of_rows_and_columns_done(self):
        res = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.get_number(i, j) == 2:
                    break
                if j == self.size - 1:
                    res += 1
        for i in range(self.size):
            for j in range(self.size):
                if self.get_number(j, i) == 2:
                    break
                if j == self.size - 1:
                    res += 1
        return res

    def is_empty_square(self, row, col):
        return self.get_number(row, col) == 2

    def number_of_empty_squares_with_adjacent_numbers(self):
        res = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.is_empty_square(row, col):
                    l = self.adjacent_vertical_numbers(row, col)
                    if l[0] == l[1] != 2:
                        res += 1
                    l = self.adjacent_horizontal_numbers(row, col)
                    if l[0] == l[1] != 2:
                        res += 1
        return res

    def copy(self):
        b = []
        for row in range(self.size):
            b.append([])
            for col in range(self.size):
                b[row].append(self.get_number(row, col))
        return Board(b, self.size)

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        Por exemplo:
            $ python3 takuzu.py < input_T01
            > from sys import stdin
            > stdin.readline()
        """
        rows = int(sys.stdin.readline())
        matrix = []
        for i in range(rows):
            row = sys.stdin.readline().strip().split('\t')
            for j in range(rows):
                row[j] = int(row[j])
            matrix.append(row)

        return Board(matrix, rows)

    def __repr__(self):
        res = ''
        for i in range(self.size):
            for j in range(self.size):
                res += str(self.board[i][j]) + '\t'
            res += '\n'
        return res[:len(res) - 1]


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(TakuzuState(board))
        self.aux = 0

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        return state.board.possible_moves()

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new_state = TakuzuState(state.board.copy())
        new_state.board.make_move(action[0], action[1], action[2])
        return new_state

    def goal_test(self, state: TakuzuState):
        self.aux += 1
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        return state.board.all_positions_are_filled()

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return node.state.board.number_of_empty_squares()


if __name__ == "__main__":
    # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    # $ python3 takuzu < i1.txt
    board = Board.parse_instance_from_stdin()
    # Criar uma instância de Takuzu:
    problem = Takuzu(board)
    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board, sep="")
