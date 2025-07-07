import sys, os, termios, tty, select, fcntl, struct, time, atexit
class novaio:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)
        atexit.register(self.restore)

    def restore(self):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    def get_key(self, timeout=0):
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            ch = os.read(self.fd, 32)
            try:
                return ch.decode(sys.stdin.encoding or 'utf-8', 'ignore')
            except:
                return None
        return None
