import copy
import state

white_king = None
black_king = None

class Pawn:

    def __init__(self, color, x, y):
        
        self.color = color
        self.x = x
        self.y = y
        self.moved = False
        self.first_moved = False
        self.possible_moves = []
        self.en_passant = {}
        self.first_double = False

    def __str__(self):
        
        if self.color == 'W':

            return "♙"
        
        else:

            return "♟"

    def move(self):

        direcoes = [1, 2]

        self.possible_moves = []

        self.en_passant = {}

        d = {}

        # one or two foward

        if not self.moved:

            if self.color == 'W':

                #captrua diagonal
                    
                if self.x + 1 < 8 and self.y + 1 < 8 and state.board[self.x + 1][self.y +1] != '.':

                    if state.board[self.x + 1][self.y +1].color != self.color:

                        d[(self.x + 1, self.y + 1)] = "capture"

                        self.possible_moves.append(d)

                        d = {}
                
                if 0 <= self.x - 1 and self.y + 1 < 8 and state.board[self.x - 1][self.y +1] != '.':

                    if state.board[self.x - 1][self.y +1].color != self.color:

                        d[(self.x - 1, self.y + 1)] = "capture"

                        self.possible_moves.append(d)

                        d = {}
            
            else:

                if self.x + 1 < 8 and 0 <= self.y - 1 and state.board[self.x + 1][self.y -1] != '.':

                    if state.board[self.x + 1][self.y -1].color != self.color:

                        d[(self.x + 1, self.y - 1)] = "capture"

                        self.possible_moves.append(d)

                        d = {}

                if 0 <= self.x - 1 and 0 <= self.y - 1 and state.board[self.x - 1][self.y -1] != '.':

                    if state.board[self.x - 1][self.y -1].color != self.color:

                        d[(self.x - 1, self.y - 1)] = "capture"

                        self.possible_moves.append(d)

                        d = {}
            
            for dy in direcoes:

                d = {}

                x = self.x
                y = self.y

                if self.color == 'W':

                    y += dy
                
                else:

                    y -= dy

                casa = state.board[self.x][y]

                if casa == '.':

                    d[(self.x, y)] = "move"

                    self.possible_moves.append(d)

                    d = {}
                
                else:

                    break

        # en passant

        if self.x + 1 < 8 and (isinstance(state.board[self.x + 1][self.y], Pawn) and state.board[self.x + 1][self.y].color != self.color and
            state.board[self.x + 1][self.y].first_moved and state.board[self.x + 1][self.y].first_double):

            if self.color == 'W':

                self.en_passant = (self.x + 1, self.y)

                d[(self.x + 1, self.y + 1)] = "capture"

                self.possible_moves.append(d)

                d = {}

            else:

                self.en_passant = (self.x + 1, self.y)

                d[(self.x + 1, self.y - 1)] = "capture"

                self.possible_moves.append(d)

                d = {}
        
        if 0 <= self.x - 1 and (isinstance(state.board[self.x - 1][self.y], Pawn) and state.board[self.x - 1][self.y].color != self.color and
            state.board[self.x - 1][self.y].first_moved and state.board[self.x - 1][self.y].first_double):

            if self.color == 'W':

                self.en_passant = (self.x - 1, self.y)

                d[(self.x - 1, self.y + 1)] = "capture"

                self.possible_moves.append(d)

                d = {}

            else:

                self.en_passant = (self.x - 1, self.y)

                d[(self.x - 1, self.y - 1)] = "capture"  

                self.possible_moves.append(d)

                d = {}

        # one foward

        if self.moved:

            if self.color == 'W':
                
                if self.y + 1 < 8 and state.board[self.x][self.y + 1] == '.':

                    d[(self.x, self.y + 1)] = "move"

                    self.possible_moves.append(d)

                    d = {}

                if self.x + 1 < 8 and self.y + 1 < 8 and state.board[self.x + 1][self.y +1] != '.':

                    if state.board[self.x + 1][self.y +1].color != self.color:

                        d[(self.x + 1, self.y + 1)] = "capture"

                        self.possible_moves.append(d)

                        d = {}
                
                if 0 <= self.x - 1 and self.y + 1 < 8 and state.board[self.x - 1][self.y +1] != '.':

                    if state.board[self.x - 1][self.y +1].color != self.color:

                        d[(self.x - 1, self.y + 1)] = "capture"

                        self.possible_moves.append(d)

                        d = {}
            
                
            else:
                
                if state.board[self.x][self.y - 1] == '.':

                    d = {}

                    d[(self.x, self.y - 1)] = "move"

                    self.possible_moves.append(d)


                if self.x + 1 < 8 and 0 <= self.y - 1 and state.board[self.x + 1][self.y -1] != '.':

                    if state.board[self.x + 1][self.y -1].color != self.color:

                        d = {}

                        d[(self.x + 1, self.y - 1)] = "capture"

                        self.possible_moves.append(d)


                if 0 <= self.x + 1 and 0 <= self.y + 1 and state.board[self.x - 1][self.y -1] != '.':

                    if state.board[self.x - 1][self.y -1].color != self.color:

                        d = {}

                        d[(self.x - 1, self.y - 1)] = "capture"

                        self.possible_moves.append(d)


        king = get_king(self.color)

        can_move(self, king)

class Hook:

    def __init__(self, color, x, y):
        
        self.color = color
        self.x = x
        self.y = y
        self.moved = False
        self.possible_moves = []
    
    def __str__(self):
        
        if self.color == 'W':

            return "♖"
        
        else:

            return "♜"

    def move(self):

        direcoes = [(1,0), (-1,0), (0, 1), (0, -1)]

        self.possible_moves = []

        for dx, dy in direcoes:

            x = self.x + dx
            y = self.y + dy

            while 0 <= x < 8 and 0 <= y < 8:

                casa = state.board[x][y]

                d = {}

                if casa == '.':

                    d[(x,y)] = "move"

                    self.possible_moves.append(d)

                elif casa.color != self.color:

                    d[(x,y)] = "capture"
                    self.possible_moves.append(d)

                    break

                else:

                    break
                
                x += dx
                y += dy

        king = get_king(self.color)

        can_move(self, king)
                    
                    



class Horse:

    def __init__(self, color, x, y):
        
        self.color = color
        self.x = x
        self.y = y
        self.moved = False
        self.possible_moves = []

    def __str__(self):
        
        if self.color == 'W':

            return "♘"
        
        else:

            return "♞"


    def move(self):

        direcoes = [(1,2), (2,1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

        self.possible_moves = []

        for dx, dy in direcoes:

            x = self.x + dx
            y = self.y + dy

            if 0 <= x < 8 and 0 <= y < 8:

                casa = state.board[x][y]

                d = {}

                if casa == '.':

                    d[(x,y)] = "move"

                    self.possible_moves.append(d)

                elif casa.color != self.color:

                    d[(x,y)] = "capture"
                    self.possible_moves.append(d)

        king = get_king(self.color)

        can_move(self, king)

class Bishop:

    def __init__(self, color, x, y):
        
        self.color = color
        self.x = x
        self.y = y
        self.moved = False
        self.possible_moves = []
    
    def __str__(self):
        
        if self.color == 'W':

            return "♗"
        
        else:

            return "♝"
        
    def move(self):

        direcoes = [(1,1), (-1,1), (-1, -1), (1, -1)]

        self.possible_moves = []

        for dx, dy in direcoes:

            x = self.x + dx
            y = self.y + dy

            while 0 <= x < 8 and 0 <= y < 8:

                casa = state.board[x][y]

                d = {}

                if casa == '.':

                    d[(x,y)] = "move"

                    self.possible_moves.append(d)

                elif casa.color != self.color:

                    d[(x,y)] = "capture"
                    self.possible_moves.append(d)

                    break

                else:

                    break
                
                x += dx
                y += dy

        king = get_king(self.color)

        can_move(self, king)
    

class Queen:

    def __init__(self, color, x, y):
        
        self.color = color
        self.x = x
        self.y = y
        self.moved = False
        self.possible_moves = []

    def __str__(self):
        
        if self.color == 'W':

            return "♕"
        
        else:

            return "♛"

    def move(self):

        direcoes = [(1,1), (-1,1), (-1, -1), (1, -1), (1,0), (-1,0), (0, 1), (0, -1)]

        self.possible_moves = []

        for dx, dy in direcoes:

            x = self.x + dx
            y = self.y + dy

            while 0 <= x < 8 and 0 <= y < 8:

                casa = state.board[x][y]

                d = {}

                if casa == '.':

                    d[(x,y)] = "move"

                    self.possible_moves.append(d)

                elif casa.color != self.color:

                    d[(x,y)] = "capture"
                    self.possible_moves.append(d)

                    break

                else:

                    break
                
                x += dx
                y += dy

        king = get_king(self.color)

        can_move(self, king)

class King:

    def __init__(self, color, x, y):
        
        self.color = color
        self.x = x
        self.y = y
        self.moved = False
        self.possible_moves = []
        self.check = False
        self.check_mate = False
        self.castle = {}

    def __str__(self):
        
        if self.color == 'W':

            return "♔"
        
        else:

            return "♚"

    def move(self):

        direcoes = [(1,1), (-1,1), (-1, -1), (1, -1), (1,0), (-1,0), (0, 1), (0, -1)]

        self.possible_moves = []

        for dx, dy in direcoes:

            x = self.x + dx
            y = self.y + dy

            if 0 <= x < 8 and 0 <= y < 8:

                casa = state.board[x][y]

                d = {}

                if casa == '.' and not king_under_attack(None, x, y, self.color):

                    d[(x,y)] = "move"

                    self.possible_moves.append(d)

                elif casa != '.' and casa.color != self.color and not king_under_attack(None, x, y, self.color):

                    d[(x,y)] = "capture"
                    self.possible_moves.append(d)

                    break
            
            if not self.moved:

                if self.color == 'W':

                    if (isinstance(state.board[0][0], Hook) and not state.board[0][0].moved):

                        if state.board[1][0] == '.' and state.board[2][0] == '.' and state.board[3][0] == '.' and castle(state.board[0][0], 3, 0, self, 2, 0):

                            d = {}

                            d[(2, 0)] = {"castle": ((3, 0), state.board[0][0])}
                            self.possible_moves.append(d)

                    if (isinstance(state.board[7][0], Hook) and not state.board[7][0].moved):

                        if state.board[5][0] == '.' and state.board[6][0] == '.' and castle(state.board[7][0], 5, 0, self, 6, 0):

                            d = {}

                            d[(6, 0)] = {"castle": ((5, 0), state.board[7][0])}
                            self.possible_moves.append(d)

                else:
                    
                    if (isinstance(state.board[0][7], Hook) and not state.board[0][7].moved):

                            if state.board[1][7] == '.' and state.board[2][7] == '.' and state.board[3][7] == '.' and castle(state.board[0][7], 3, 7, self, 2, 7):

                                d = {}

                                d[(2, 7)] = {"castle": ((3, 7), state.board[0][7])}
                                self.possible_moves.append(d)

                    if (isinstance(state.board[7][7], Hook) and not state.board[7][7].moved):

                        if state.board[5][7] == '.' and state.board[6][7] == '.' and castle(state.board[7][7], 5, 7, self, 6, 7):

                            d = {}

                            d[(6, 7)] = {"castle": ((5, 7), state.board[7][7])}
                            self.possible_moves.append(d)

        can_move(None, self)

                

def get_king(color):

    for x in range(8):
        for y in range(8):

            casa = state.board[x][y]

            if isinstance(casa, King) and casa.color == color:

                return casa

def king_under_attack(king: King=None, x=None, y=None, color=None, new_board=None):

    if new_board is None:

        new_board = state.board

    if king == None:

        king_x = x
        king_y = y
        color = color

    else:

        king_x = king.x
        king_y = king.y
        color = king.color

    if color == 'W':

        #pawn check
        if king_x - 1 >= 0  and king_y + 1 < 8 and isinstance(new_board[king_x - 1][king_y + 1], Pawn) and new_board[king_x - 1][king_y + 1].color != color:
            
            if not(king == None):

                king.check = True
                return True
            
            else:

                return True
        
        if king_x + 1 and king_y + 1 and isinstance(new_board[king_x + 1][king_y + 1], Pawn) and new_board[king_x + 1][king_y + 1].color != color:

            if not(king == None):

                king.check = True
                return True

            else:

                return True
            
        # horse
        direcoes = [(1,2), (2,1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

        for dx, dy in direcoes:

            x = king_x + dx
            y = king_y + dy

            if 0 <= x < 8 and 0 <= y < 8:

                casa = new_board[x][y]

                if isinstance(casa, Horse) and casa.color != color:

                    if not(king == None):

                        king.check = True
                        return True
            
                    else:

                        return True
        # hook/queen
        direcoes = [(1,0), (-1,0), (0, 1), (0, -1)]

        for dx, dy in direcoes:

            x = king_x + dx
            y = king_y + dy

            while 0 <= x < 8 and 0 <= y < 8:

                casa = new_board[x][y]

                if casa == '.':

                    pass

                elif casa.color != color and (isinstance(casa, Queen) or isinstance(casa, Hook)):

                    if not(king == None):

                        king.check = True
                        return True
            
                    else:

                        return True

                else:

                    break
                
                x += dx
                y += dy

        #Bishop/queen
        direcoes = [(1,1), (-1,1), (-1, -1), (1, -1)]

        for dx, dy in direcoes:

            x = king_x + dx
            y = king_y + dy

            while 0 <= x < 8 and 0 <= y < 8:

                casa = new_board[x][y]

                if casa == '.':

                    pass

                elif casa.color != color and (isinstance(casa, Queen) or isinstance(casa, Bishop)):

                    if not(king == None):

                        king.check = True
                        return True
            
                    else:

                        return True

                else:

                    break
                
                x += dx
                y += dy

        # king
        direcoes = [(1,1), (-1,1), (-1, -1), (1, -1), (1,0), (-1,0), (0, 1), (0, -1)]

        for dx, dy in direcoes:

            x = king_x + dx
            y = king_y + dy

            if not (0 <= x < 8 and 0 <= y < 8):

                continue

            casa = new_board[x][y]

            if casa == '.':

                pass

            elif casa.color != color and (isinstance(casa, King)):

                if not(king == None):

                    king.check = True
                    return True
            
                else:

                    return True

        if king == None:

            return False
    
        else:

            king.check = False


    #black
    else:

        #pawn check
        if 0 <= king_x -1 and 0 <= king_y - 1 and (isinstance(new_board[king_x - 1][king_y - 1], Pawn) and new_board[king_x - 1][king_y - 1].color != color):
            
            if not(king == None):

                king.check = True
                return True

            else:

                return True
            
        if king_x + 1 < 8 and 0 <= king_y and (isinstance(new_board[king_x + 1][king_y - 1], Pawn) and new_board[king_x + 1][king_y - 1].color != color):
            
            if not(king == None):

                king.check = True
                return True

            else:

                return True

        # horse
        direcoes = [(1,2), (2,1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

        for dx, dy in direcoes:

            x = king_x + dx
            y = king_y + dy

            if 0 <= x < 8 and 0 <= y < 8:

                casa = new_board[x][y]

                if isinstance(casa, Horse) and casa.color != color:

                    if not(king == None):

                        king.check = True
                        return True
            
                    else:

                        return True
        # hook/queen
        direcoes = [(1,0), (-1,0), (0, 1), (0, -1)]

        for dx, dy in direcoes:

            x = king_x + dx
            y = king_y + dy

            while 0 <= x < 8 and 0 <= y < 8:

                casa = new_board[x][y]

                if casa == '.':

                    pass

                elif casa.color != color and (isinstance(casa, Queen) or isinstance(casa, Hook)):

                    if not(king == None):

                        king.check = True
                        return True
            
                    else:

                        return True

                else:

                    break
                
                x += dx
                y += dy

        #Bishop/queen
        direcoes = [(1,1), (-1,1), (-1, -1), (1, -1)]

        for dx, dy in direcoes:

            x = king_x + dx
            y = king_y + dy

            while 0 <= x < 8 and 0 <= y < 8:

                casa = new_board[x][y]

                d = {}

                if casa == '.':

                    pass

                elif casa.color != color and (isinstance(casa, Queen) or isinstance(casa, Bishop)):

                    if not(king == None):

                        king.check = True
                        return True
            
                    else:

                        return True

                else:

                    break
                
                x += dx
                y += dy

        # king
        direcoes = [(1,1), (-1,1), (-1, -1), (1, -1), (1,0), (-1,0), (0, 1), (0, -1)]

        for dx, dy in direcoes:

            x = king_x + dx
            y = king_y + dy

            if not (0 <= x < 8 and 0 <= y < 8):

                continue

            casa = new_board[x][y]

            if casa == '.':

                pass

            elif casa.color != color and (isinstance(casa, King)):

                if not(king == None):

                    king.check = True
                    return True
            
                else:

                    return True
                
        if king == None:

            return False
    
        else:

            king.check = False

def can_move(piece: Pawn | Hook | Queen | Bishop | Horse | None, king: King):
        
        valid_moves = []

        if piece is None:

            piece = king

        for move in piece.possible_moves:

            for (x, y) in move.keys():

                new_board = copy.deepcopy(state.board)
                
                new_board[piece.x][piece.y] = '.'
                new_board[x][y] = piece

                if piece is not None:

                    attack = king_under_attack(king=None, x=king.x, y=king.y, color=king.color, new_board=new_board)

                else:

                    attack = king_under_attack(king=None, x=x, y=y, color=king.color, new_board=new_board)

                if not attack:

                    valid_moves.append(move)
        
        piece.possible_moves = valid_moves


def castle(hook: Hook, hook_x, hook_y, king: King, king_x, king_y):
        
        new_board = copy.deepcopy(state.board)
        
        new_board[king.x][king.y] = '.'
        new_board[king_x][king_y] = king
        new_board[hook.x][hook.y] = '.'
        new_board[hook.x][hook_y] = hook

        attack = king_under_attack(king=None, x=king_x, y=king_y, color=king.color, new_board=new_board)

        if not attack:

            return True

white_moves = []

black_moves = []

def checkmate():

    global white_moves 
    
    global black_moves

    white_moves = []

    black_moves = []

    for x in range(8):
        for y in range(8):

            casa = state.board[x][y]

            if casa != '.':

                casa.move()

            if casa != '.' and casa.color == 'W' and casa.possible_moves:

                white_moves.append(casa.possible_moves)

            elif casa != '.' and casa.color == 'B' and casa.possible_moves:

                black_moves.append(casa.possible_moves)

    king_under_attack(white_king)
    king_under_attack(black_king)

    if not white_moves and white_king.check:

        state.checkmate = True

        return "B"
    
    if not black_moves and black_king.check:

        state.checkmate = True

        return 'W'

    if not white_moves and not white_king.check:

        state.checkmate = False

        return "D"
    
    if not black_moves and not black_king.check:

        state.checkmate = False

        return 'D'
    
    return 'GO'

def create_pieces():

    pieces = []

    for x in range(8):

        white_pawn_y = 1
        black_pawn_y = 6
        white_pieces_y = 0
        black_pieces_y = 7

        pieces.append(Pawn("W", x, white_pawn_y))
        pieces.append(Pawn("B", x, black_pawn_y))
        
        if x == 0 or x == 7:

            pieces.append(Hook("W", x, white_pieces_y))
            pieces.append(Hook("B", x, black_pieces_y))
        
        elif x == 1 or x == 6:

            pieces.append(Horse("W", x, white_pieces_y))
            pieces.append(Horse("B", x, black_pieces_y))

        elif x == 2 or x == 5:

            pieces.append(Bishop("W", x, white_pieces_y))
            pieces.append(Bishop("B", x, black_pieces_y))

        elif x == 3:

            pieces.append(Queen("W", x, white_pieces_y))
            pieces.append(Queen("B", x, black_pieces_y))

        else:
            
            global white_king

            global black_king

            white_king = King("W", x, white_pieces_y)
            black_king = King("B", x, black_pieces_y)

            pieces.append(white_king)
            pieces.append(black_king)
    
    return pieces