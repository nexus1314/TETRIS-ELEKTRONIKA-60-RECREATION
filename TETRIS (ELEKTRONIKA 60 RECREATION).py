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

PIECES = [
    {"kind": "I", "mat": [[1,1,1,1]]},
    {"kind": "O", "mat": [[1,1],[1,1]]},
    {"kind": "T", "mat": [[0,1,0],[1,1,1]]},
    {"kind": "S", "mat": [[1,1,0],[0,1,1]]},
    {"kind": "Z", "mat": [[0,1,1],[1,1,0]]},
    {"kind": "J", "mat": [[1,0,0],[1,1,1]]},
    {"kind": "L", "mat": [[0,0,1],[1,1,1]]},
]

def init_screen():
    os.system("cls")
    print("\x1b[?25l", end="")

def reset_cursor():
    print("\x1b[H", end="")

def restore_cursor():
    print("\x1b[?25h", end="")

def rotate_cw(mat):
    return [list(row) for row in zip(*mat[::-1])]

def rotate_ccw(mat):
    return [list(row) for row in zip(*mat)][::-1]

def new_board():
    return [[0]*COLS for _ in range(ROWS)]

def copy_piece(p):
    return {"kind": p["kind"], "mat": [r[:] for r in p["mat"]]}

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

def render(board, piece, px, py, score, lines, level):
    reset_cursor()
    print("TETRIS (ELEKTRONIKA-60 RECREATION)")
    print("← → move | ↓ soft | SPACE hard | Z / X rotate | Q quit")
    print(f"SCORE: {score}   LINES: {lines}   LEVEL: {level}\n")

    for y in range(ROWS):
        row = [BLOCK if board[y][x] else EMPTY for x in range(COLS)]
        for x,yy in piece_cells(piece,px,py):
            if yy == y and 0 <= x < COLS:
                row[x] = BLOCK
        print(f"{LEFT_WALL}{''.join(row)}{RIGHT_WALL}")

    print(" " + BOTTOM*COLS)

def run_windows():
    board = new_board()
    bag = make_bag()
    piece = bag.pop()
    px, py = COLS//2 - 1, -1

    score = lines = level = 0
    last_fall = time.time()

    while True:
        if msvcrt.kbhit():
            k = msvcrt.getch()

            if k in (b"\x00", b"\xe0"):
                k = msvcrt.getch()

                if k == b"K" and not collides(board,piece,px-1,py):   # ←
                    px -= 1
                elif k == b"M" and not collides(board,piece,px+1,py): # →
                    px += 1
                elif k == b"P" and not collides(board,piece,px,py+1): # ↓
                    py += 1

            else:
                if k == b"z":
                    rotated = rotate_ccw(piece["mat"])
                    test = {"kind": piece["kind"], "mat": rotated}
                    if not collides(board,test,px,py):
                        piece["mat"] = rotated

                elif k == b"x":
                    rotated = rotate_cw(piece["mat"])
                    test = {"kind": piece["kind"], "mat": rotated}
                    if not collides(board,test,px,py):
                        piece["mat"] = rotated

                elif k == b" ":
                    while not collides(board,piece,px,py+1):
                        py += 1

                elif k == b"q":
                    return

        if time.time() - last_fall >= fall_time(level):
            last_fall = time.time()
            if not collides(board,piece,px,py+1):
                py += 1
            else:
                lock_piece(board,piece,px,py)
                board, cleared = clear_lines(board)
                lines += cleared
                score += LINE_CLEAR_POINTS.get(cleared,0)
                level = 1 + lines//10
                bag = bag or make_bag()
                piece = bag.pop()
                px, py = COLS//2 - 1, -1

        render(board,piece,px,py,score,lines,level)
        time.sleep(0.016)

def main():
    init_screen()
    try:
        run_windows()
    finally:
        restore_cursor()

if __name__ == "__main__":
    main()