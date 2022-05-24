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
    def __init__(self, board):
        self.board = numpy.matrix(board, int)
        self.history = []

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board.item(row, col)

    def set_number(self, row: int, col: int, n: int):
        """Altera uma posicao do tabuleiro sem adiciona-la ao historico"""
        self.board.itemset((row, col), n)

    def set_number_recorded(self, row: int, col: int, n: int):
        """Altera uma posicao do tabuleiro adicionando-a ao historico"""
        self.board.itemset((row, col), n)
        self.history.append((row, col, n))

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        a = None
        b = None
        try:
            a = self.board.item(row + 1, col)
        except:
            pass
        try:
            b = self.board.item(row - 1, col)
        except:
            pass

        return a, b

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        a = None
        b = None
        try:
            a = self.board.item(row, col - 1)
        except:
            pass
        try:
            b = self.board.item(row, col + 1)
        except:
            pass

        return a, b

    def size(self):
        """returns the size of the board nxn (returning n)"""
        return int(self.board.size ** 0.5)

    def game_over(self):
        return 2 not in self.board

    def all_rows_and_columns_are_different(self):
        return numpy.unique(self.board, axis=0).all() == numpy.unique(self.board, axis=1).all() == self.board.all()

    def there_are_no_more_than_two_adjacent_numbers(self):
        size = self.size()
        for row in range(size):
            for col in range(size):
                number = self.get_number(row, col)
                if number != 2 and \
                        (number == self.adjacent_vertical_numbers(row, col) and
                         self.adjacent_horizontal_numbers(row, col) == number):
                    return False
        return True


    def possible_move(self, row: int, col: int, n: int):
        """Returns True if it is a possible move and False otherwise"""

        saved_number = self.get_number(row, col)
        self.board.set_number(row, col, n)
        res = self.solvable()
        self.board.set_number(row, col, saved_number)

        return res

    def possible_moves(self):
        """Returns a list of possible moves, every possible move is like (row, col, number)"""
        n = self.size()
        res = []
        for row in range(n):
            for col in range(n):
                if self.empty_square(row, col):
                    if self.possible_move(row, col, 0):
                        res.append((row, col, 0))
                    if self.possible_move(row, col, 1):
                        res.append((row, col, 1))
        return res




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
        matrix = ''
        for i in range(rows - 1):
            matrix += sys.stdin.readline().strip() + ';'
        matrix += sys.stdin.readline().strip()

        return Board(matrix)

    # TODO: outros metodos da classe

    def __copy__(self):
        return Board(self.board.copy())

    def __repr__(self):
        return str(self.board).replace('\n ', '\n').replace('[', '').replace(']', '').replace(' ', '\t')


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(TakuzuState(board))


    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        size = state.board.size()
        res = []
        for row in range(size):
            for col in range(size):
                if state.board.get_number(row, col) == 2:
                    state.board.set_number(row, col, 0)
                    if state.board.there_are_no_more_than_two_adjacent_numbers() and \
                        state.board.all_rows_and_columns_are_different():
                        res.append((row, col, 0))
                        state.board.set_number(row, col, 2)

                    state.board.set_number(row, col, 1)
                    if state.board.there_are_no_more_than_two_adjacent_numbers() and \
                        state.board.all_rows_and_columns_are_different():
                        res.append((row, col, 1))
                        state.board.set_number(row, col, 2)
        return res


    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        s = TakuzuState(state.board.__copy__())
        s.board.set_number(action[0], action[1], action[2])
        return s



    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        return state.board.game_over()


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

