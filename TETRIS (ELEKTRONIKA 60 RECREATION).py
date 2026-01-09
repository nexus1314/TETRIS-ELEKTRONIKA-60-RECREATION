import os
import time
import random

IS_WINDOWS = (os.name == "nt")
if IS_WINDOWS:
    import msvcrt
else:
    raise SystemExit

COLS, ROWS = 10, 20

EMPTY = "· "
BLOCK = "██"

LEFT_WALL = "<|"
RIGHT_WALL = "|>"
BOTTOM = "\\/"

BASE_FALL = 0.85
MIN_FALL = 0.15

LINE_CLEAR_POINTS = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}

TSPIN_POINTS = {0: 400, 1: 800, 2: 1200, 3: 1600}

PIECES = [
    {"kind": "I", "mat": [[1, 1, 1, 1]]},
    {"kind": "O", "mat": [[1, 1], [1, 1]]},
    {"kind": "T", "mat": [[0, 1, 0], [1, 1, 1]]},
    {"kind": "S", "mat": [[0, 1, 1], [1, 1, 0]]},
    {"kind": "Z", "mat": [[1, 1, 0], [0, 1, 1]]},
    {"kind": "J", "mat": [[1, 0, 0], [1, 1, 1]]},
    {"kind": "L", "mat": [[0, 0, 1], [1, 1, 1]]},
]

I_ROTATIONS = {
    0: [
        [0,0,0,0],
        [1,1,1,1],
        [0,0,0,0],
        [0,0,0,0],
    ],
    1: [
        [0,0,1,0],
        [0,0,1,0],
        [0,0,1,0],
        [0,0,1,0],
    ],
    2: [
        [0,0,0,0],
        [0,0,0,0],
        [1,1,1,1],
        [0,0,0,0],
    ],
    3: [
        [0,1,0,0],
        [0,1,0,0],
        [0,1,0,0],
        [0,1,0,0],
    ],
}

O_ROTATIONS = {
    0: [[1,1],[1,1]],
    1: [[1,1],[1,1]],
    2: [[1,1],[1,1]],
    3: [[1,1],[1,1]],
}

T_ROTATIONS = {
    0: [
        [0,1,0],
        [1,1,1],
        [0,0,0],
    ],
    1: [
        [0,1,0],
        [0,1,1],
        [0,1,0],
    ],
    2: [
        [0,0,0],
        [1,1,1],
        [0,1,0],
    ],
    3: [
        [0,1,0],
        [1,1,0],
        [0,1,0],
    ],
}

S_ROTATIONS = {
    0: [
        [0,1,1],
        [1,1,0],
        [0,0,0],
    ],
    1: [
        [0,1,0],
        [0,1,1],
        [0,0,1],
    ],
    2: [
        [0,0,0],
        [0,1,1],
        [1,1,0],
    ],
    3: [
        [1,0,0],
        [1,1,0],
        [0,1,0],
    ],
}

Z_ROTATIONS = {
    0: [
        [1,1,0],
        [0,1,1],
        [0,0,0],
    ],
    1: [
        [0,0,1],
        [0,1,1],
        [0,1,0],
    ],
    2: [
        [0,0,0],
        [1,1,0],
        [0,1,1],
    ],
    3: [
        [0,1,0],
        [1,1,0],
        [1,0,0],
    ],
}

J_ROTATIONS = {
    0: [
        [1,0,0],
        [1,1,1],
        [0,0,0],
    ],
    1: [
        [0,1,1],
        [0,1,0],
        [0,1,0],
    ],
    2: [
        [0,0,0],
        [1,1,1],
        [0,0,1],
    ],
    3: [
        [0,1,0],
        [0,1,0],
        [1,1,0],
    ],
}

L_ROTATIONS = {
    0: [
        [0,0,1],
        [1,1,1],
        [0,0,0],
    ],
    1: [
        [0,1,0],
        [0,1,0],
        [0,1,1],
    ],
    2: [
        [0,0,0],
        [1,1,1],
        [1,0,0],
    ],
    3: [
        [1,1,0],
        [0,1,0],
        [0,1,0],
    ],
}

PIECE_ROTATIONS = {
    "I": I_ROTATIONS,
    "O": O_ROTATIONS,
    "T": T_ROTATIONS,
    "S": S_ROTATIONS,
    "Z": Z_ROTATIONS,
    "J": J_ROTATIONS,
    "L": L_ROTATIONS,
}


I_SRS_OFFSETS = {
    (0, 1): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (1, 2): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    (2, 3): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    (3, 0): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    (1, 0): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    (2, 1): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    (3, 2): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (0, 3): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
}

T_SRS_OFFSETS = {
    (0, 1): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (1, 2): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (2, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    (3, 0): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (1, 0): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (2, 1): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (3, 2): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (0, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
}

STANDARD_SRS_OFFSETS = {
    (0, 1): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (1, 2): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (2, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    (3, 0): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (1, 0): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (2, 1): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (3, 2): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (0, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
}

def init_screen():
    os.system("cls")
    print("\x1b[?25l", end="")

def reset_cursor():
    print("\x1b[H", end="")

def restore_cursor():
    print("\x1b[?25h", end="")

def new_board():
    return [[0]*COLS for _ in range(ROWS)]

def copy_piece(p):
    return {"kind": p["kind"], "mat": [r[:] for r in p["mat"]], "rotation": 0}

def piece_cells(piece, px, py):
    return [(px+c, py+r)
            for r,row in enumerate(piece["mat"])
            for c,v in enumerate(row) if v]

def collides(board, piece, px, py):
    for x,y in piece_cells(piece,px,py):
        if x < 0 or x >= COLS or y >= ROWS:
            return True
        if y >= 0 and board[y][x]:
            return True
    return False

def try_rotate_with_wallkick(board, piece, px, py, clockwise):
    kind = piece["kind"]
    old_rot = piece.get("rotation", 0)
    new_rot = (old_rot + 1) % 4 if clockwise else (old_rot - 1) % 4

    rotated = [row[:] for row in PIECE_ROTATIONS[kind][new_rot]]
    test_piece = {"kind": kind, "mat": rotated, "rotation": new_rot}
    key = (old_rot, new_rot)

    if kind == "I":
        offsets = I_SRS_OFFSETS.get(key, [(0, 0)])
    elif kind == "T":
        offsets = T_SRS_OFFSETS.get(key, [(0, 0)])
    else:
        offsets = STANDARD_SRS_OFFSETS.get(key, [(0, 0)])

    for ox, oy in offsets:
        nx, ny = px + ox, py + oy
        if not collides(board, test_piece, nx, ny):
            return rotated, nx, ny, new_rot, True

    return None, px, py, old_rot, False

def is_blocked_corner(board, x, y):
    if x < 0 or x >= COLS or y >= ROWS:
        return True
    if y < 0:
        return False
    return board[y][x] == 1

def detect_tspin(board, piece, px, py, last_move_was_rotate):
    if piece["kind"] != "T" or not last_move_was_rotate:
        return False

    cx, cy = px + 1, py + 1
    corners = [(cx-1, cy-1), (cx+1, cy-1), (cx-1, cy+1), (cx+1, cy+1)]
    blocked = sum(1 for (x, y) in corners if is_blocked_corner(board, x, y))
    return blocked >= 3

def lock_piece(board, piece, px, py):
    for x,y in piece_cells(piece,px,py):
        if y < 0:
            return False
        board[y][x] = 1
    return True

def clear_lines(board):
    kept = [r for r in board if not all(r)]
    cleared = ROWS - len(kept)
    while len(kept) < ROWS:
        kept.insert(0, [0]*COLS)
    return kept, cleared

def fall_time(level):
    return max(MIN_FALL, BASE_FALL * (0.92 ** (level-1)))

def make_bag():
    bag = [copy_piece(p) for p in PIECES]
    random.shuffle(bag)
    return bag

def render_piece_preview(piece, size=4):
    grid = [[EMPTY for _ in range(size)] for _ in range(size)]
    if piece is None:
        return grid

    mat = piece["mat"]
    mat_h = len(mat)
    mat_w = len(mat[0]) if mat else 0

    start_y = (size - mat_h) // 2
    start_x = (size - mat_w) // 2

    for r, row in enumerate(mat):
        for c, cell in enumerate(row):
            if cell:
                if 0 <= start_y + r < size and 0 <= start_x + c < size:
                    grid[start_y + r][start_x + c] = BLOCK
    return grid

def render(board, piece, px, py, score, lines, level, held_piece=None, next_piece=None, last_text=""):
    reset_cursor()
    print("TETRIS (ELEKTRONIKA-60) || RECREATED BY NEXUS1314\n")
    print("← → - MOVE | ↓ - SOFT DROP | SPACE - HARD DROP | Z - LEFT ROTATE / X - RIGHT ROTATE | C - HOLD | R - RESET | P - PAUSE | Q - QUIT\n")
    if last_text:
        print(last_text + "\n")
    else:
        print()

    held_grid = render_piece_preview(held_piece)
    next_grid = render_piece_preview(next_piece)

    for y in range(ROWS):
        row = [BLOCK if board[y][x] else EMPTY for x in range(COLS)]
        for x,yy in piece_cells(piece,px,py):
            if yy == y and 0 <= x < COLS:
                row[x] = BLOCK
        board_line = f"{LEFT_WALL}{''.join(row)}{RIGHT_WALL}"

        if y == 0:
            board_line += "  SCORE: " + str(score)
        elif y == 1:
            board_line += "  LINES: " + str(lines)
        elif y == 2:
            board_line += "  LEVEL: " + str(level)
        elif y == 4:
            board_line += "  HOLD"
        elif 5 <= y < 9:
            board_line += "  " + "".join(held_grid[y - 5])
        elif y == 11:
            board_line += "  NEXT"
        elif 12 <= y < 16:
            board_line += "  " + "".join(next_grid[y - 12])

        print(board_line)

    print(" " + BOTTOM*COLS)

def run_windows():
    board = new_board()
    bag = make_bag()

    piece = bag.pop()
    next_piece = bag.pop() if bag else copy_piece(random.choice(PIECES))
    px, py = COLS//2 - 2, -1

    score = 0
    lines = 0
    level = 1
    last_fall = time.time()

    paused = False
    held_piece = None
    can_hold = True
    last_rotate_ok = False
    last_text = ""

    while True:
        if msvcrt.kbhit():
            k = msvcrt.getch()

            if k in (b"\x00", b"\xe0"):
                k = msvcrt.getch()

                if not paused:
                    if k == b"K":
                        if not collides(board, piece, px-1, py):
                            px -= 1
                            last_rotate_ok = False
                    elif k == b"M": 
                        if not collides(board, piece, px+1, py):
                            px += 1
                            last_rotate_ok = False
                    elif k == b"P": 
                        if not collides(board, piece, px, py+1):
                            py += 1
                            last_rotate_ok = False

            else:
                if k == b"z" and not paused:
                    rotated, nx, ny, nrot, ok = try_rotate_with_wallkick(board, piece, px, py, clockwise=False)
                    if ok:
                        piece["mat"] = rotated
                        piece["rotation"] = nrot
                        px, py = nx, ny
                        last_rotate_ok = True

                elif k == b"x" and not paused:
                    rotated, nx, ny, nrot, ok = try_rotate_with_wallkick(board, piece, px, py, clockwise=True)
                    if ok:
                        piece["mat"] = rotated
                        piece["rotation"] = nrot
                        px, py = nx, ny
                        last_rotate_ok = True

                elif k == b" " and not paused:
                    while not collides(board, piece, px, py+1):
                        py += 1
                    last_rotate_ok = False

                elif k == b"c" and not paused and can_hold:
                    temp = piece
                    if held_piece is None:
                        piece = next_piece
                        next_piece = bag.pop() if bag else copy_piece(random.choice(PIECES))
                        held_piece = temp
                    else:
                        piece = held_piece
                        held_piece = temp

                    # RESET POSITION
                    piece["rotation"] = 0
                    piece["mat"] = [row[:] for row in PIECE_ROTATIONS[piece["kind"]][0]]
                    px, py = COLS//2 - 2, -1
                    can_hold = False
                    last_rotate_ok = False

                elif k == b"r" and not paused:
                    board = new_board()
                    bag = make_bag()
                    piece = bag.pop()
                    next_piece = bag.pop() if bag else copy_piece(random.choice(PIECES))
                    px, py = COLS//2 - 2, -1
                    score = 0
                    lines = 0
                    level = 1
                    last_fall = time.time()
                    held_piece = None
                    can_hold = True
                    last_rotate_ok = False
                    last_text = ""

                elif k == b"p":
                    paused = not paused
                    last_fall = time.time()

                elif k == b"q":
                    return

        if not paused and (time.time() - last_fall >= fall_time(level)):
            last_fall = time.time()

            if not collides(board, piece, px, py+1):
                py += 1
                last_rotate_ok = False
            else:
                tspin = detect_tspin(board, piece, px, py, last_rotate_ok)

                ok = lock_piece(board, piece, px, py)
                if not ok:
                    last_text = "GAME OVER"
                    paused = True
                else:
                    board, cleared = clear_lines(board)
                    lines += cleared

                    # SCORING
                    base = LINE_CLEAR_POINTS.get(cleared, 0)
                    score += base
                    if tspin:
                        score += TSPIN_POINTS.get(cleared, 0)
                        last_text = f"T-SPIN! (+{TSPIN_POINTS.get(cleared, 0)})"
                    else:
                        last_text = f"{cleared} LINE CLEAR" if cleared > 0 else "LOCK"

                    level = 1 + lines // 10

                    # NEXT SPAWN
                    bag = bag or make_bag()
                    piece = next_piece
                    next_piece = bag.pop() if bag else copy_piece(random.choice(PIECES))

                    piece["rotation"] = 0
                    piece["mat"] = [row[:] for row in PIECE_ROTATIONS[piece["kind"]][0]]

                    px, py = COLS//2 - 2, -1
                    can_hold = True
                    last_rotate_ok = False

        render(board, piece, px, py, score, lines, level, held_piece, next_piece, last_text)
        time.sleep(0.016)

def main():
    init_screen()
    try:
        run_windows()
    finally:
        restore_cursor()

if __name__ == "__main__":
    main()