import pieces as piecespy
import tkinter as tk
import state

turn = "W"
selected = None
higlihts = []
valid_targets = set()


def clean_board():

    global turn

    global selected

    global valid_targets

    valid_targets = set()

    state.game_over = False

    state.movement = None

    state.result = ''

    selected = None

    state.checkmate = False

    turn = "W"

    state.board = [['.' for _ in range(8)] for _ in range(8)]

    pieces = piecespy.create_pieces()

    print(pieces)

    for piece in pieces:

        state.board[piece.x][piece.y] = piece


CELL = 70

N = 8

def reset_game(event=None):
    global selected, valid_targets, turn

    state.game_over = False
    state.result = "GO"
    selected = None
    valid_targets = set()
    turn = "W"

    canvas.delete("end_text")
    clean_board()
    draw_board()

    canvas.bind("<Button-1>", click)
    canvas.bind("<Motion>", move)

root = tk.Tk()
canvas = tk.Canvas(root, width=N*CELL, height=N*CELL)
canvas.pack()
reset_btn = tk.Button(root, text="Recomeçar", command=reset_game)
reset_btn.pack()


def draw_board():

    canvas.delete("all")

    for x in range(N):
        for y in range(N):

            sr = 7 - y
            sc = x

            x0, y0 = sc*CELL, sr*CELL
            x1, y1 = x0+CELL, y0+CELL

            color = 'green' if (x+y) % 2 == 0 else '#EEE'
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='')

    for x in range(8):
        for y in range(8):
            piece = state.board[x][y]
            if piece != '.':
                cx = x*CELL + CELL/2
                cy = (7 - y)*CELL + CELL/2
                canvas.create_text(cx, cy, text=str(piece), font=("Arial", 24))

def click(event):

    global selected, valid_targets, turn

    if state.game_over:
        return

    x = event.x // CELL
    y = 7 - (event.y // CELL)

    x0 = x * CELL
    y0 = (7 - y) * CELL
    x1, y1 = x0+CELL, y0+CELL

    if not (0 <= x < 8 and 0 <= y < 8):
        
        return

    if selected is not None and (x, y) in valid_targets:

    
        state.movement = (x, y)

        print("Escolheu movimento para:", (x, y))

        sx, sy = selected
        piece = state.board[sx][sy]
        
        if isinstance(piece, piecespy.Pawn) and piece.en_passant:

            x, y = piece.en_passant

            piece.en_passant = False

            state.board[x][y] = '.'

            x, y = state.movement

        if isinstance(piece, piecespy.King) and (x, y) in piece.castle:

            hook_x, hook_y = piece.castle[(x, y)][0]

            hook = piece.castle[(x, y)][1]

            print("Torre:", hook)

            state.board[hook.x][hook.y] = '.'
            state.board[hook_x][hook_y] = hook
            hook.x, hook.y = hook_x, hook_y

        if isinstance(piece, piecespy.Pawn):

            if piece.color == 'W' and y == 7:

                choice = promotion("W")

                if choice == "Q":
        
                    piece = piecespy.Queen("W", piece.x, piece.y)

                if choice == "C":

                    piece = piecespy.Horse("W", piece.x, piece.y)

                if choice == "B":

                    piece = piecespy.Bishop("W", piece.x, piece.y)

                if choice == "H":

                    piece = piecespy.Hook("W", piece.x, piece.y)

            if piece.color == 'B' and y == 0:
        
                choice = promotion("W")

                if choice == "Q":
        
                    piece = piecespy.Queen("B", piece.x, piece.y)

                if choice == "C":

                    piece = piecespy.Horse("B", piece.x, piece.y)

                if choice == "B":

                    piece = piecespy.Bishop("B", piece.x, piece.y)

                if choice == "H":

                    piece = piecespy.Hook("B", piece.x, piece.y)


        if isinstance(piece, piecespy.Pawn) and not piece.moved:

            if abs(y - sy) == 2:

                piece.first_double = True

            piece.first_moved = True
                

        state.board[sx][sy] = '.'
        state.board[x][y] = piece

        piece.x, piece.y = x, y


        if isinstance(piece, piecespy.Pawn) and piece.moved and piece.first_moved:

            piece.first_moved = False

        piece.moved = True

        selected = None
        valid_targets = set()
        canvas.delete('selected')
        canvas.delete('move')
        draw_board()

        turn = 'B' if turn == 'W' else 'W'

        end = piecespy.checkmate()

        if end != "GO":
            
            end_game(end)
            return

        return

    casa = state.board[x][y]

    if casa != '.' and casa.color == turn and (x, y) != selected:

        casa.move()

        moves = casa.possible_moves

        valid_targets = {next(iter(m.keys())) for m in moves}  # pega (xH,yH)

        if isinstance(casa, piecespy.King):
        
            for m in moves:

                for k, v in m.items():

                    if isinstance(v, dict):

                        print("Esse é o M:", m)

                        hook_cord, hook = v["castle"]

                        casa.castle[k] = (hook_cord, hook)
        
        if not valid_targets:

            return

        selected = (x, y)

        print("Selecionou peça:", selected, "targets:", valid_targets)

        canvas.delete('selected')

        canvas.delete('move')

        outline = 'blue'
        canvas.create_rectangle(x0, y0, x1, y1, outline=outline, width=10, tags='selected')


        for move in moves:

            (xH, yH), kind = next(iter(move.items()))
            x0 = xH * CELL
            y0 = (7 - yH) * CELL
            x1, y1 = x0+CELL, y0+CELL
            outline = 'lime' if kind == "move" else "red"
            canvas.create_rectangle(x0, y0, x1, y1, outline=outline, width=10, tags='move')

        return

    
    else:

        selected = None

        canvas.delete('selected')

        canvas.delete('move')   

    print(selected)


def move(event):

    canvas.delete('hl')

    global selected

    x = event.x // CELL
    y = 7 - (event.y // CELL)

    if 0 <= x < 8 and 0 <= y < 8 and selected is None:

        casa = state.board[x][y]

        if casa != '.' and casa.color == turn:

            casa.move()

            moves = casa.possible_moves

            for move in moves:

                (xH, yH), kind = next(iter(move.items()))

                x0 = xH * CELL
                y0 = (7 - yH) * CELL
                x1, y1 = x0+CELL, y0+CELL

                outline = 'lime' if kind == "move" else "red"
                canvas.create_rectangle(x0, y0, x1, y1, outline=outline, width=10, tags='hl')

def end_game(result: str):
    state.game_over = True
    state.result = result

    if result == "W":
        msg = "CHECKMATE\nWHITE WON!"
    elif result == "B":
        msg = "CHECKMATE\nBLACK WON!"
    elif result == "D":
        msg = "STALEMATE"
    else:
        msg = str(result)

    # para input
    canvas.unbind("<Button-1>")
    canvas.unbind("<Motion>")

    # garante que nada vai apagar a msg depois:
    draw_board()

    # apaga qualquer overlay antigo
    canvas.delete("end_text")

    # "tela" por cima (sem transparência real, mas dá pra simular com stipple)
    canvas.create_rectangle(
        0, 0, N*CELL, N*CELL,
        fill="black", stipple="gray50", outline="",
        tags="end_text"
    )

    # texto por cima
    canvas.create_text(
        (N*CELL)//2, (N*CELL)//2,
        text=msg, font=("Arial", 32),
        fill="white",
        tags="end_text"
    )

    canvas.update_idletasks()

    print("END_GAME CHAMOU:", result)

def promotion(color):

    win = tk.Toplevel(root)

    win.title("Promotion")

    win.resizable(False,False)

    win.transient(root)

    win.update_idletasks()
    win.deiconify()
    win.update()

    win.grab_set()

    choice = tk.StringVar(value="Q")

    tk.Label(win, text="Promote to:").pack(padx=10, pady=(10, 6))

    frame = tk.Frame(win)
    frame.pack(padx=10, pady=(0, 10))

    options = [
        ("Q", piecespy.Queen),
        ("H", piecespy.Hook), 
        ("B", piecespy.Bishop),
        ("C", piecespy.Horse),  
    ]

    def pick(code):
        choice.set(code)
        win.destroy()

    for code, cls in options:
        p = cls(color, 0, 0)
        tk.Button(frame, text=str(p), font=("Arial", 28),
                  width=2, command=lambda c=code: pick(c)).pack(side="left", padx=6)
        
    win.protocol("WM_DELETE_WINDOW", lambda: pick("Q"))

    root.wait_window(win)

    return choice.get()
            
canvas.bind("<Button-1>", click)
canvas.bind("<Motion>", move)
    
