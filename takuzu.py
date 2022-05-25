# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 01:
# 00000 Nome1
# 00000 Nome2

import sys, numpy
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
        """Altera uma posicao do tabuleiro sem adiciona-la ao historico"""
        self.board[row][col] = n


    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""

        if row == 0:
            up = None
        else:
            up = self.get_number(row - 1, col)
        if row == self.size-1:
            down = None
        else:
            down = self.get_number(row + 1, col)

        return down, up

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        if col == 0:
            left = None
        else:
            left = self.get_number(row, col - 1)
        if col == self.size-1:
            right = None
        else:
            right = self.get_number(row, col+1)

        return left, right

    def there_are_no_more_than_two_adjacent_numbers(self):
        for row in range(self.size):
            for col in range(self.size):
                number = self.get_number(row, col)
                if self.adjacent_vertical_numbers(row, col).count(number) == 2 or \
                        self.adjacent_horizontal_numbers(row, col).count(number) == 2:
                    return False
        return True


    def possible_moves(self):
        """Returns a list of possible moves, every possible move is like (row, col, number)"""
        #TODO
        #mal feito
        res = []
        for row in range(self.size):
            for col in range(self.size):
                if self.get_number(row, col) == 2:
                    res.append((row, col, 0))
                    res.append((row, col, 1))
        return res

    def all_positions_are_filled(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 2:
                    return False
        return True

    def all_rows_are_different(self):
        for row1 in range(self.size):
            for row2 in range(row1+1, self.size):
                for col in range(self.size):
                    if self.get_number(row1, col) != self.get_number(row2, col):
                        break
                    if col == self.size-1:
                        return False
        return True

    def all_columns_are_different(self):
        for col1 in range(self.size):
            for col2 in range(col1+1, self.size):
                for row in range(self.size):
                    if self.get_number(row, col1) != self.get_number(row, col2):
                        break
                    if row == self.size - 1:
                        return False
        return True

    def difference_between_number_of_1s_and_0s_per_row_and_column_is_fine(self):
        if self.size % 2 == 0:
            for row in range(self.size):
                if self.board.count(1) != self.board.count(0):
                    return False
            for col in range(self.size):
                counter = {0: 0, 1: 0}
                for row in range(self.size):
                    counter[self.get_number(row, col)] += 1
                if counter[0] != counter[1]:
                    return False
        else:
            for row in range(self.size):
                if abs(self.board.count(1) - self.board.count(0)) > 1:
                    return False
            for col in range(self.size):
                counter = {0: 0, 1: 0}
                for row in range(self.size):
                    counter[self.get_number(row, col)] += 1
                if abs(counter[0] - counter[1]) > 1:
                    return False

        return True

    def copy(self):
        b = []
        for i in range(self.size):
            b.append(self.board[i].copy())
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
                res += str(self.board[i][j])+'\t'
            res += '\n'
        return res[:len(res)-1]


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(TakuzuState(board))

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
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        return state.board.all_positions_are_filled() and \
                state.board.there_are_no_more_than_two_adjacent_numbers() and \
                state.board.all_rows_are_different() and \
                state.board.all_columns_are_different() and \
                state.board.difference_between_number_of_1s_and_0s_per_row_and_column_is_fine()

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


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



