import sys, os, termios, tty, select, fcntl, struct, time, atexit

class Cell:
    def __init__(self, ch=' ', style=''):
        self.ch = ch
        self.style = style

    def __str__(self):
        return f"{self.style}{self.ch}\x1b[0m" if self.style else self.ch

    def __eq__(self, other):
        return isinstance(other, Cell) and self.ch == other.ch and self.style == other.style

class Buffer:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]

    def clear(self):
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = Cell()

    def set_char(self, x, y, ch, style=''):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = Cell(ch, style)

    def get_cell(self, x, y):
        return self.grid[y][x]

class novascr:
    def __init__(self, height=None, width=None):
        try:
            import shutil
            ts = shutil.get_terminal_size()
            height = height or ts.lines
            width = width or ts.columns
        except:
            height = height or 24
            width = width or 80
        self.height = height
        self.width = width
        self.curr = Buffer(self.height, self.width)
        self.next = Buffer(self.height, self.width)
        sys.stdout.write("\x1b[?25l") 
        sys.stdout.flush()

    def clear(self):
        self.next.clear()

    def str(self, x, y, text, style=''):
        for i, ch in enumerate(text):
            self.next.set_char(x + i, y, ch, style)

    def refresh(self):
        out = []
        for y in range(self.height):
            for x in range(self.width):
                old = self.curr.get_cell(x, y)
                new = self.next.get_cell(x, y)
                if new != old:
                    out.append(f"\x1b[{y+1};{x+1}H")
                    out.append(str(new))
                    self.curr.grid[y][x] = Cell(new.ch, new.style)

        if out:
            sys.stdout.write(''.join(out))
            sys.stdout.flush()
        for y in range(self.height):
            for x in range(self.width):
                self.next.grid[y][x] = Cell(self.curr.grid[y][x].ch, self.curr.grid[y][x].style)

    def set_size(self, height, width):
        try:
            winsize = struct.pack("HHHH", height, width, 0, 0)
            fcntl.ioctl(sys.stdout.fileno(), termios.TIOCSWINSZ, winsize)
        except Exception:
            pass
        sys.stdout.write(f"\x1b[8;{height};{width}t")
        sys.stdout.flush()
        self.height, self.width = height, width
        self.curr = Buffer(self.height, self.width)
        self.next = Buffer(self.height, self.width)

    def close(self):
        sys.stdout.write("\x1b[?25h")
        sys.stdout.flush()

