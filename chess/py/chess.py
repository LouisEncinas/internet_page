from time import sleep
from termcolor import colored, cprint

"""
Code all moves of pieces that do not need to know other pieces moves in the pieces class
"""

ASCII_UPPER_START = 65
ASCII_LOWER_START = 97
BOARD_SIZE = 8

def add(*tpls) -> tuple:
    res = (0,0)
    for tpl in tpls:
        res = (res[0] + tpl[0], res[1] + tpl[1])
    return res

def time(a, tpl):
    return (a*tpl[0], a*tpl[1])

class Move:

    def __init__(self, _from, to, piece, take:bool=False, upgrade:bool=False, rook:bool=False, en_passant:bool=False, dir_rook:tuple=None, piece_rook=None, pot_threat:bool=True) -> None:
        self.piece = piece

        self._from = _from
        self.to = to

        self.take = take

        self.upgrade = upgrade
        self.en_passant = en_passant

        self.rook = rook
        self.dir_rook = dir_rook
        self.piece_rook = piece_rook

        self.pot_threat = pot_threat

    def __str__(self) -> str:
        tk = 'x' if self.take else ''
        up = '(up)' if self.upgrade else ''
        ro = '(rook)' if self.rook else ''
        return f'{self.piece} : {self._from}->{tk}{self.to} {up}{ro}'


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

    def __init__(self, id:str, color:str) -> None:
        self._id = id
        self._pos = ''
        self._color = color

        self.not_moved = True
        self.defended = False

        self.moves:list[Move] = []

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

    def __init__(self, color: str) -> None:
        super().__init__(Piece.PAWN, color)

    def _possible_moves(self, board:list[list]) -> list[Move]:

        psb_mv = []
        index = Piece._pos_to_index(self._pos)
        self.dir = -1 if self._color == Piece.WHITE else 1
        upgrade = True if ((self._color == Piece.WHITE and index[0] == 1) or (self._color == Piece.BLACK and index[0] == 6)) else False
        lim = 2 if self.not_moved else 1

        straight_movements = (self.dir,0)
        eating_movements = [(self.dir,-1),(self.dir,1)]
        ep_movements = [(0,-1),(0,1)]

        new_index = (index[0]+straight_movements[0],index[1]+straight_movements[1])
        while (-1 < new_index[0] < 8 and -1 < new_index[1] < 8) and board[new_index[0]][new_index[1]] == Chess._EMPTY_CASE and abs(new_index[0]-index[0]) <= lim:
            psb_mv.append(Move(Piece._index_to_pos(index), Piece._index_to_pos(new_index), self, upgrade=upgrade, pot_threat=False))
            new_index = (new_index[0]+straight_movements[0],new_index[1]+straight_movements[1])

        for em in eating_movements:
            new_index = (index[0]+em[0],index[1]+em[1])
            if -1 < new_index[0] < 8 and -1 < new_index[1] < 8:
                arrival_case = board[new_index[0]][new_index[1]]
                if isinstance(arrival_case, Piece):
                    if arrival_case._color != self._color: psb_mv.append(Move(Piece._index_to_pos(index), Piece._index_to_pos(new_index), self, take=True, upgrade=upgrade))
                    else: arrival_case.defended = True

        for epm in ep_movements:
            look_index = (index[0]+epm[0],index[1]+epm[1])
            arrival_index = (index[0]+epm[0]+self.dir,index[1]+epm[1])
            if (-1 < arrival_index[0] < 8 and -1 < arrival_index[1] < 8):
                look_case = board[look_index[0]][look_index[1]]
                arrival_case = board[arrival_index[0]][arrival_index[1]]
                if self._pos[1] == '5' and isinstance(look_case, Pawn) and look_case._color != self._color and len(look_case.moves) == 1:
                    psb_mv.append(Move(Piece._index_to_pos(index), Piece._index_to_pos(arrival_index), self, upgrade=upgrade, take=True, en_passant=True))

        return psb_mv

class FiniteMovementPiece(Piece):

    def __init__(self, id: str, color: str) -> None:
        super().__init__(id, color)
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
                elif isinstance(arrival_case, Piece):
                    if arrival_case._color != self._color: psb_mv.append(Move(Piece._index_to_pos(index), Piece._index_to_pos(new_index), self, take=True))
                    else: arrival_case.defended = True
        return psb_mv

class Night(FiniteMovementPiece):

    def __init__(self, color:str) -> None:
        super().__init__(Piece.NIGHT, color)
        self.movements = [(2,-1),(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2)]

class King(FiniteMovementPiece):
    
    def __init__(self, color: str) -> None:
        super().__init__(Piece.KING, color)
        self.movements = [(1,1),(-1,1),(-1,-1),(1,-1),(0,1),(0,-1),(1,0),(-1,0)]
        self.pinned_pieces = []
        self.pos_move_to = []

    def _possible_moves(self, board: list[list]) -> list[Move]:
        psb_mv = super()._possible_moves(board)
        self.pinned_pieces = []
        self.pos_move_to = []
        # Check for rook possibilities
        dirs = [(0,1),(0,-1)]
        index = Piece._pos_to_index(self._pos)
        if self.not_moved:
            for dir in dirs:
                new_index = add(index,dir)
                while (0 < new_index[0] < 7 and 0 < new_index[1] < 7) and board[new_index[0]][new_index[1]] == Chess._EMPTY_CASE:
                    new_index = add(new_index,dir)
                look_case = board[new_index[0]][new_index[1]]
                if isinstance(look_case, Rook) and look_case.not_moved:
                    psb_mv.append(Move(Piece._index_to_pos(index), Piece._index_to_pos((index[0]+2*dir[0],index[1]+2*dir[1])), self, rook=True, dir_rook=dir, piece_rook=look_case))

        for dir in self.movements:
            pinned_piece = None
            pos_move_to = []
            new_index = (index[0]+dir[0],index[1]+dir[1])
            brk = True
            while (-1 < new_index[0] < 8 and -1 < new_index[1] < 8) and brk:
                new_case = board[new_index[0]][new_index[1]]
                pos_move_to.append(Piece._index_to_pos(new_index))
                if isinstance(new_case, Piece):
                    if new_case._color != self._color:
                        brk = False
                        if not isinstance(new_case,(Rook, Bishop, Queen)): pinned_piece = None
                    else: pinned_piece = new_case

                new_index = (new_index[0]+dir[0],new_index[1]+dir[1])

            # If any pinned piece is found, we keep the piece and all the case (to) where it can go
            if pinned_piece is not None and not brk: 
                self.pinned_pieces.append(pinned_piece)
                self.pos_move_to.append(pos_move_to)
        
        return psb_mv

class InfiniteMovementPiece(Piece):

    def __init__(self, id: str, color: str) -> None:
        super().__init__(id, color)
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
                if isinstance(board[new_index[0]][new_index[1]],Piece):
                    if board[new_index[0]][new_index[1]]._color != self._color: psb_mv.append(Move(Piece._index_to_pos(index), Piece._index_to_pos(new_index), self, take=True))
                    else: board[new_index[0]][new_index[1]].defended = True
        return psb_mv

class Bishop(InfiniteMovementPiece):

    def __init__(self, color:str) -> None:
        super().__init__(Piece.BISHOP, color)
        self.directions = [(1,1),(-1,1),(-1,-1),(1,-1)]

class Rook(InfiniteMovementPiece):

    def __init__(self, color: str) -> None:
        super().__init__(Piece.ROOK, color)
        self.directions = [(0,1),(0,-1),(1,0),(-1,0)]

class Queen(InfiniteMovementPiece):

    def __init__(self, color: str) -> None:
        super().__init__(Piece.QUEEN, color)
        self.directions = [(1,1),(-1,1),(-1,-1),(1,-1),(0,1),(0,-1),(1,0),(-1,0)]

def convertir(piece:Piece, new_type_piece:str) -> Piece:

    dic_pieces = {
        Piece.NIGHT: Night,
        Piece.BISHOP: Bishop,
        Piece.ROOK: Rook,
        Piece.QUEEN: Queen
    }

    new_piece:Piece = dic_pieces[new_type_piece](piece._color)
    new_piece._pos = piece._pos
    new_piece._color = piece._color
    new_piece.not_moved = piece.not_moved
    new_piece.defended = piece.defended
    new_piece.moves = piece.moves

    return new_piece

class Chess:

    _EMPTY_CASE:str = '_'

    _INIT = [[Rook(Piece.BLACK),Night(Piece.BLACK),Bishop(Piece.BLACK),Queen(Piece.BLACK),King(Piece.BLACK),Bishop(Piece.BLACK),Night(Piece.BLACK),Rook(Piece.BLACK)],
            [Pawn(Piece.BLACK) for _ in range(8)],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [Pawn(Piece.WHITE) for _ in range(8)],
            [Rook(Piece.WHITE),Night(Piece.WHITE),Bishop(Piece.WHITE),Queen(Piece.WHITE),King(Piece.WHITE),Bishop(Piece.WHITE),Night(Piece.WHITE),Rook(Piece.WHITE)]]

    _TEST = [[_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,Rook(Piece.BLACK),_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,Bishop(Piece.BLACK),_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,Queen(Piece.WHITE),_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE],
            [Rook(Piece.WHITE),_EMPTY_CASE,_EMPTY_CASE,_EMPTY_CASE,King(Piece.WHITE),_EMPTY_CASE,_EMPTY_CASE,Rook(Piece.WHITE)]]

    def __init__(self) -> None:
        self._board = self._INIT
        self.initialize_pos()
        self.turn = Piece.WHITE

        self.moves:list[Move] = []

        self.check = False
        self.check_mate = False

        self.psb_mv = self._possible_moves()

    def board(self, case:str):
        index = Piece._pos_to_index(case)
        return self._board[index[0]][index[1]]

    def initialize_pos(self) -> None:
        for i, row in enumerate(self._board):
            for j, case in enumerate(row):
                if isinstance(case, Piece):
                    case._pos = Piece._index_to_pos((i,j))
    
    def show(self):
        print('')
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

        cprint('\nTurn : ', end='')
        col = 'red' if self.turn == Piece.WHITE else 'blue'
        opp_col = 'blue' if col == 'red' else 'red'
        cprint(f'{self.turn}', col, end='\n')

        if self.check:
            cprint('\nCheck', opp_col, end='\n')

        if self.check_mate:
            cprint(f'\nVictory for {self.turn}', opp_col, end='\n')

        print('')
        for move in self.psb_mv:
            print(move)
    

    def _possible_moves(self) -> list[Move]:
        self.check = False
        check_pieces = []
        check_king = None
        # Create two lists, one containing the player moves and another containing the ennemy moves
        psb_mv_player = []
        psb_mv_holder = []
        for row in self._board:
            for case in row:
                if isinstance(case, Piece): 
                    if case._color == self.turn:
                        psb_mv_player += case._possible_moves(self._board)
                    else: psb_mv_holder += case._possible_moves(self._board)

        # rm_mv is the list that will contain all moves that are illegal
        rm_mv = []
        for player_move in psb_mv_player:
            # Particular case for the king
            if isinstance(player_move.piece, King):
                # Check if the piece is defended, in which case the king can not eat the piece.
                arrival_case = self.board(player_move.to)
                if isinstance(arrival_case, Piece) and arrival_case.defended: rm_mv.append(player_move)

                for holder_move in psb_mv_holder:
                    # Check the case that are controlled by ennemy pieces
                    if player_move.to == holder_move.to and holder_move.pot_threat and player_move not in rm_mv: rm_mv.append(player_move)
                    # Check if the king is in Check and keep the pieces
                    if holder_move.to == player_move.piece._pos and holder_move.pot_threat and holder_move.piece not in check_pieces: 
                        self.check = True
                        check_pieces.append(holder_move.piece)
                    # Check for rook
                    if player_move.rook and Piece._index_to_pos((Piece._pos_to_index(player_move.to)[0]-player_move.dir_rook[0],Piece._pos_to_index(player_move.to)[1]-player_move.dir_rook[1])) == holder_move.to and holder_move.pot_threat and player_move not in rm_mv: rm_mv.append(player_move)
                # Keep the king if it is checked
                if self.check: 
                    check_king = player_move.piece

                # Pinned pieces
                for ind, pp in enumerate(player_move.piece.pinned_pieces):
                    for pm in psb_mv_player:
                        if pp == pm.piece and pm.to not in player_move.piece.pos_move_to[ind] and pm not in rm_mv:
                            rm_mv.append(pm)

        # Actions when a king is checked
        if self.check:
            defend_case:list[str] = []
            if len(check_pieces) == 1:
                # If only 1 piece is threatening the king, keep the cases where the threatening piece is and between the piece
                # and the king, and check if any ohter piece the same color as the king can defend it.
                threatening_piece = check_pieces[0]
                king_index = Piece._pos_to_index(check_king._pos)
                threat_index = Piece._pos_to_index(threatening_piece._pos)
                diff_tpl = (king_index[0]-threat_index[0],king_index[1]-threat_index[1])
                diff = abs(diff_tpl[0]) if not diff_tpl[1] else abs(diff_tpl[1])
                diff_tpl = (diff_tpl[0]//diff,diff_tpl[1]//diff)
                for i in range(diff):
                    defend_case.append(Piece._index_to_pos(add(threat_index, time(i,diff_tpl))))
                # Only keep the moves of other pieces than can defend the king
                for move in psb_mv_player:
                    if not isinstance(move.piece,King) and move.to not in defend_case and move not in rm_mv:
                        rm_mv.append(move)
            else:
                # If 2 pieces are threatening the king, the only possible action is to move this king
                for move in psb_mv_player:
                    if not isinstance(move.piece, King):
                        rm_mv.append(move)
        
        # rm_mv = list(set(rm_mv))
        # It is important that rm_mv does not contain any moves multiple time, list(set(.)) is a way to erase all the double moves
        # however, it is not used here because it is checked in the conditions before adding a move to rm_mv that rm_mv does not already
        # contain the move

        # Erase all moves that are not legal
        for move in rm_mv:
            psb_mv_player.remove(move)

        if not psb_mv_player: self.check_mate = True
                        
        return psb_mv_player

    def move(self, _from:str, to:str) -> None:
        save_move = None
        for move in self.psb_mv:
            if move._from == _from and move.to == to:
                save_move = move
        if save_move is not None:
            save_move.piece.moves.append(save_move)
            self.moves.append(save_move)
            for row in self._board:
                for case in row:
                    if isinstance(case, Piece): case.defended = False
            findex = Piece._pos_to_index(save_move._from)
            fto = Piece._pos_to_index(save_move.to)
            save_move.piece._pos = save_move.to
            if save_move.piece.not_moved: save_move.piece.not_moved = False

            if save_move.upgrade:
                print('')
                print('New type of piece : (n, b, r, q)')
                ask_new = input()
                self._board[fto[0]][fto[1]] = convertir(save_move.piece, ask_new)
            else:
                self._board[fto[0]][fto[1]] = save_move.piece

            if save_move.rook:
                rook_index = Piece._pos_to_index(save_move.piece_rook._pos)
                new_rook_index = (fto[0]-save_move.dir_rook[0],fto[1]-save_move.dir_rook[1])
                self._board[rook_index[0]][rook_index[1]] = self._EMPTY_CASE
                self._board[new_rook_index[0]][new_rook_index[1]] = save_move.piece_rook
                save_move.piece_rook._pos = Piece._index_to_pos(new_rook_index)
                save_move.piece_rook.not_moved = False # If the rook has already moved, not rook is possible
            
            self._board[findex[0]][findex[1]] = self._EMPTY_CASE
            if save_move.en_passant:
                self._board[fto[0]-save_move.piece.dir][fto[1]] = self._EMPTY_CASE

            self.turn = Piece.BLACK if save_move.piece._color == Piece.WHITE else Piece.WHITE
            self.psb_mv = self._possible_moves()
