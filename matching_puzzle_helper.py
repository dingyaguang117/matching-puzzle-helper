
class Board(object):
    """表示一个棋盘"""
    COLUMNS = 4
    ROWS = 3
    def __init__(self, target):
        """
        :param target: 目标状态. e.g. ["++E*", "D*DO", "E*  "]
        """
        self.target = []
        self.state = [[Symbol(' ') for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        self.subassemblies = [[None for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        if len(target) != self.ROWS:
            raise Exception('The board must have %d rows' % self.ROWS)
        for row in target:
            if len(row) != self.COLUMNS:
                raise Exception('The board must have %d columns' % self.COLUMNS)
            self.target.append([Symbol(symbol) for symbol in row])

    def __repr__(self):
        s = f"""
--- target ---
{self.get_target_description()}
--- state ---
{self.get_state_description()}
--- result ---
{self.get_result_description()}
"""
        return s.strip()

    def finished(self):
        """检查是否完成"""
        # TODO: 可以优化下，通过记录已经放置的部件数量，来判断是否完成
        for row in range(self.ROWS):
            for column in range(self.COLUMNS):
                if self.state[row][column] != self.target[row][column]:
                    return False
        return True

    def place_subassembly(self, subassembly, row, column, direction):
        """在棋盘上放置一个部件
        :param subassembly: Subassembly
        :param row: int 行
        :param column: int 列
        :param direction: int 方向
        :return: bool 是否放置成功
        """
        neighbor = self.get_neighbor(row, column, direction)

        # 尝试放置每一个面
        for symbol1, symbol2 in subassembly:
            if not self.check_available(row, column, symbol1) or not self.check_available(neighbor[0], neighbor[1], symbol2):
                continue
            self.state[row][column] = symbol1
            self.state[neighbor[0]][neighbor[1]] = symbol2
            self.subassemblies[row][column] = subassembly
            self.subassemblies[neighbor[0]][neighbor[1]] = subassembly
            return True
        return False

    def remove_subassembly(self, row, column, direction):
        """移除棋盘上的一个部件
        :param row: int
        :param column: int
        :param direction: int
        """
        neighbor = self.get_neighbor(row, column, direction)
        self.state[row][column] = Symbol(' ')
        self.state[neighbor[0]][neighbor[1]] = Symbol(' ')
        self.subassemblies[row][column] = None
        self.subassemblies[neighbor[0]][neighbor[1]] = None

    @staticmethod
    def get_neighbor(row, column, direction):
        """获取一个位置的邻居"""
        neighbors = [(row, column + 1), (row + 1, column), (row, column-1), (row-1, column)]
        return neighbors[direction]

    def check_available(self, row, column, symbol):
        """检查棋盘上的一个位置是否可用"""
        # 检查是否可以被放置
        if not self.can_placed(row, column):
            return False
        # 判断 symbol 是否相同
        if self.target[row][column] != symbol:
            return False
        return True

    def can_placed(self, row, column):
        """检查棋盘上的一个位置是否可以被放置"""
        # 检查超出边界
        if row < 0 or row >= self.ROWS or column < 0 or column >= self.COLUMNS:
            return False
        # target 不可以放置
        if self.target[row][column] == Symbol(' '):
            return False
        # 当前已被放置
        if self.state[row][column] != Symbol(' '):
            return False
        return True

    def get_target_description(self):
        """打印目标"""
        result = []
        for row in range(self.ROWS):
            result.append(''.join([symbol.symbol for symbol in self.state[row]]))
        return '\n'.join(result)

    def get_state_description(self):
        """打印当前状态"""
        result = []
        for row in range(self.ROWS):
            result.append(''.join([symbol.symbol for symbol in self.state[row]]))
        return '\n'.join(result)

    def get_result_description(self):
        """打印当前放置请求"""
        result = []
        for row in range(self.ROWS):
            result.append(''.join([str(subassembly.identity) if subassembly else ' ' for subassembly in self.subassemblies[row]]))
        return '\n'.join(result)

class Symbol(object):
    """表示棋盘上的一个符号, 空格表示空白"""
    available_symbols = [' ', '+', '', '*', 'O', 'D', 'E']
    def __init__(self, symbol: str):
        if symbol not in self.available_symbols:
            raise Exception('Symbol %s not available' % symbol)
        self.symbol = symbol

    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        return self.symbol == other.symbol


class Subassembly(object):
    """标识一个部件，由 1x2 的 Symbol 构成 """
    def __init__(self, identity, face1, face2, face3, face4):
        self.identity = identity
        self.faces = [
            (Symbol(face1[0]), Symbol(face1[1])),
            (Symbol(face2[0]), Symbol(face2[1])),
            (Symbol(face3[0]), Symbol(face3[1])),
            (Symbol(face4[0]), Symbol(face4[1])),
        ]

    def __repr__(self):
        return f"Symbol {self.identity}: {self.faces}"

    def __iter__(self):
        """返回一个迭代器，枚举每个面的 symbol 组合
        注意: 由于部件是 1x2 的，所以每个面有两种放置方式
        """
        for face in self.faces:
            yield face[0], face[1]
            yield face[1], face[0]

class MatchingPuzzleHelper(object):
    def __init__(self, target = None, debug=False):
        self.debug = debug
        self.steps = 0 # 总步数(放置次数)
        if target:
            self.board = Board(target)
        else:
            self.board = None

        self.subassemblies = [
            Subassembly(1, '++', '*E', 'D*', 'OE'),
            Subassembly(2, 'OO', '*D', '+*', 'DE'),
            Subassembly(3, 'EE', 'O+', 'DO', '+*'),
            Subassembly(4, 'DD', '*O', 'E+', 'OE'),
            Subassembly(5, '**', 'O+', 'DE', '+D'),
        ]
        self.subassemblies_used = {subassembly.identity: False for subassembly in self.subassemblies}

    def input_board(self):
        """输入棋盘目标状态"""
        target = []
        print("Please input the target board:")
        print("D: 八边形, O: 原型, E: 方形, +: 加号, *: 星型, 空格: 空白")
        for i in range(Board.ROWS):
            target.append(input('Please input row %d: ' % (i+1)))
        self.board = Board(target)
        self.steps = 0


    def solve(self):
        """解决问题, 回溯法"""
        for row in range(Board.ROWS):
            for column in range(Board.COLUMNS):
                # 优化: 如果已经不能放了，就跳过
                if not self.board.can_placed(row, column):
                    continue
                # 优化: 因为是从左到右从上到下的遍历的，所以可以只考虑向右、向下2个方向
                for direction in range(4):
                    for subassembly in self.subassemblies:
                        # 已经使用过了
                        if self.subassemblies_used[subassembly.identity]:
                            continue
                        if self.board.place_subassembly(subassembly, row, column, direction):
                            self.steps += 1
                            if self.debug:
                                print("Placed subassembly %d at (%d, %d) direction %d" % (subassembly.identity, row, column, direction))
                                print(self.board)
                            if self.board.finished():
                                return True
                            self.subassemblies_used[subassembly.identity] = True
                            if self.solve():
                                return True
                            # 如果这一步不正确的话，恢复状态
                            self.subassemblies_used[subassembly.identity] = False
                            self.board.remove_subassembly(row, column, direction)
        return False

