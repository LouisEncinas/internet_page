from termcolor import colored, cprint

ASCII_UPPER_START = 65
ASCII_LOWER_START = 97
BOARD_SIZE = 8

class Move:

    def __init__(self, _from, to, piece, take:bool=False, upgrade:bool=False) -> None:
        self._from = _from
        self.to = to
        self.piece = piece
        self.take = take
        self.upgrade = upgrade

    def __str__(self) -> str:
        tk = 'x' if self.take else ''
        up = '(up)' if self.upgrade else ''
        return f'{self._from}->{tk}{self.to} {up}'

class Piece:

    """
    No object of class "Piece" is supposed to be created
    """

    PAWN = 'p'
    BISHOP = 'b'
    NIGHT = 'n'
    ROOK = 'r'
    QUEEN = 'q'
    KING = 'k'

    WHITE = 'w'
    BLACK = 'b'

    def __init__(self, id:str, pos:str, color:str) -> None:
        self._id = id
        self._pos = pos
        self._color = color

        self.not_moved = True

    def __str__(self) -> str:
        return self._id

    @staticmethod
    def _index_to_pos(tpl:tuple[int]) -> str:
        # i -> digit backward
        # j -> letter
        return f'{chr(ASCII_LOWER_START+tpl[1])}{BOARD_SIZE-tpl[0]}'

    @staticmethod
    def _pos_to_index(pos:str) -> tuple[int]:
        return (BOARD_SIZE-int(pos[1]),ord(pos[0])-ASCII_LOWER_START)

    @staticmethod
    def _on_edge(index:tuple[int]) -> bool:
        return index[0] == 0 or index[0] == 7 or index[1] == 0 or index[1] == 7

    def _possible_moves(self, board:list[list]) -> list[Move]:
        pass

class Pawn(Piece):

    def __init__(self, pos: str, color: str) -> None:
        super().__init__(Piece.PAWN, pos, color)

    def _possible_moves(self, board:list[list]) -> list[Move]:

        psb_mv = []
        index = Piece._pos_to_index(self._pos)
        dir = -1 if self._color == Piece.WHITE else 1
        upgrade = True if ((self._color == Piece.WHITE and index[0] == 1) or (self._color == Piece.BLACK and index[0] == 6)) else False

        straight_movements = [(dir,0)]
        if self.not_moved: straight_movements.append((2*dir,0))
        eating_movements = [(dir,-1),(dir,1)]

        for sm in straight_movements:
            new_index = (index[0]+sm[0],index[1]+sm[1])
            if -1 < new_index[0] < 8 and -1 < new_index[1] < 8:
                arrival_case = board[new_index[0]][new_index[1]]
                if arrival_case == Chess._EMPTY_CASE:
                    psb_mv.append(Move(Piece._index_to_pos(index), Piece._index_to_pos(new_index), self, upgrade=upgrade))

        for em in eating_movements:
            new_index = (index[0]+em[0],index[1]+em[1])
            if -1 < new_index[0] < 8 and -1 < new_index[1] < 8:
                arrival_case = board[new_index[0]][new_index[1]]
                if isinstance(arrival_case, Piece) and arrival_case._color != self._color:
                    psb_mv.append(Move(Piece._index_to_pos(index), Piece._index_to_pos(new_index), self, upgrade=upgrade))

        return psb_mv

class FiniteMovementPiece(Piece):

    def __init__(self, id: str, pos: str, color: str) -> None:
        super().__init__(id, pos, color)
        self.movements:list[tuple] = []

    def _possible_moves(self, board: list[list]) -> list[Move]:
        psb_mv = []
        index = Piece._pos_to_index(self._pos)
        for movement in self.movements:
            new_index = (index[0]+movement[0],index[1]+movement[1])
            if -1 < new_index[0] < 8 and -1 < new_index[1] < 8:
                arrival_case = board[new_index[0]][new_index[1]]
                if arrival_case == Chess._EMPTY_CASE:
                    psb_mv.append(Move(Piece._index_to_pos(index), Piece._index_to_pos(new_index), self))
                elif isinstance(arrival_case, Piece) and arrival_case._color != self._color:
                    psb_mv.append(Move(Piece._index_to_pos(index), Piece._index_to_pos(new_index), self, take=True))
        return psb_mv

class Night(FiniteMovementPiece):

    def __init__(self, pos:str, color:str) -> None:
        super().__init__(Piece.NIGHT, pos, color)
        self.movements = [(2,-1),(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2)]

class King(FiniteMovementPiece):
    def __init__(self, pos: str, color: str) -> None:
        super().__init__(Piece.KING, pos, color)
        self.movements = [(1,1),(-1,1),(-1,-1),(1,-1),(0,1),(0,-1),(1,0),(-1,0)]

class InfiniteMovementPiece(Piece):

    def __init__(self, id: str, pos: str, color: str) -> None:
        super().__init__(id, pos, color)
        self.directions:list[tuple] = []

    def _possible_moves(self, board: list[list]) -> list[Move]:
        psb_mv = []
        index = Piece._pos_to_index(self._pos)
        for tpl in self.directions:
            new_index = (index[0]+tpl[0],index[1]+tpl[1])
            while -1 < new_index[0] < 8 and -1 < new_index[1] < 8 and board[new_index[0]][new_index[1]] == Chess._EMPTY_CASE:
                psb_mv.append(Move(Piece._index_to_pos(index), Piece._index_to_pos(new_index), self))
                new_index = (new_index[0]+tpl[0],new_index[1]+tpl[1])
            if not self._on_edge((new_index[0]-tpl[0],new_index[1]-tpl[1])):
                if isinstance(board[new_index[0]][new_index[1]],Piece) and board[new_index[0]][new_index[1]]._color != self._color:
                    psb_mv.append(Move(Piece._index_to_pos(index), Piece._index_to_pos(new_index), self, take=True))
        return psb_mv

class Bishop(InfiniteMovementPiece):

    def __init__(self, pos:str, color:str) -> None:
        super().__init__(Piece.BISHOP, pos, color)
        self.directions = [(1,1),(-1,1),(-1,-1),(1,-1)]

class Rook(InfiniteMovementPiece):

    def __init__(self, pos: str, color: str) -> None:
        super().__init__(Piece.ROOK, pos, color)
        self.directions = [(0,1),(0,-1),(1,0),(-1,0)]

class Queen(InfiniteMovementPiece):

    def __init__(self, pos: str, color: str) -> None:
        super().__init__(Piece.QUEEN, pos, color)
        self.directions = [(1,1),(-1,1),(-1,-1),(1,-1),(0,1),(0,-1),(1,0),(-1,0)]

class Chess:

    _EMPTY_CASE:str = '_'

    _INIT = [[Rook('a8', Piece.BLACK),Night('b8', Piece.BLACK),Bishop('c8',Piece.BLACK),Queen('d8', Piece.BLACK),King('e8', Piece.BLACK),Bishop('f8',Piece.BLACK),Night('g8', Piece.BLACK),Rook('h8', Piece.BLACK)],
            [Pawn(f'{chr(i+ASCII_LOWER_START)}7', Piece.BLACK) for i in range(8)],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [Pawn(f'{chr(i+ASCII_LOWER_START)}2', Piece.WHITE) for i in range(8)],
            [Rook('a1', Piece.WHITE),Night('b1', Piece.WHITE),Bishop('c1',Piece.WHITE),Queen('d1', Piece.WHITE),King('e1', Piece.WHITE),Bishop('f1',Piece.WHITE),Night('g1', Piece.WHITE),Rook('h1', Piece.WHITE)]]

    _TEST = [[_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,Pawn('d7', Piece.WHITE),_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE]]

    def __init__(self) -> None:
        self._board = self._INIT
        self.turn = Piece.WHITE
    
    def show(self):
        print('   * * * * * * * * * *')
        for index_lst, lst in enumerate(self._board):
            cprint(f' {BOARD_SIZE-index_lst} *', end=' ')
            for case in lst:
                if isinstance(case, Piece): 
                    col = 'red' if case._color == Piece.WHITE else 'blue'
                    cprint(case._id, col, end=' ')
                else:
                    cprint(f'{case}', end=' ')
            print('*')
        print('   * * * * * * * * * *\n     a b c d e f g h')

    def _possible_moves(self) -> list[Move]:
        psb_mv = []
        for row in self._board:
            for case in row:
                if isinstance(case, Piece) and case._color == self.turn:
                    psb_mv += case._possible_moves(self._board)
        return psb_mv

    def _show_possible_moves(self):
        for row in self._board:
            for case in row:
                if isinstance(case, Piece) and case._possible_moves(self._board):
                    print(f'{case._color} {case._id} in {case._pos} :')
                    string = ''
                    for move in case._possible_moves(self._board):
                        string += f'{move}, '
                    string += '\n'
                    print(string)
        print(f'Number of moves : {len(self._possible_moves())}')

    def move(self, _from:str, to:str) -> None:
        save_move = None
        for move in self._possible_moves():
            if move._from == _from and move.to == to:
                save_move = move
        if save_move is not None:
            findex = Piece._pos_to_index(save_move._from)
            fto = Piece._pos_to_index(save_move.to)
            save_move.piece._pos = save_move.to
            if save_move.piece.not_moved: save_move.piece.not_moved = False
            self._board[fto[0]][fto[1]] = save_move.piece
            self._board[findex[0]][findex[1]] = self._EMPTY_CASE
            self.turn = Piece.BLACK if save_move.piece._color == Piece.WHITE else Piece.WHITE