import curses
import time

class CursesInterface:

    input_buffer = []
    username = "PLACEHOLDER"

    #################################
    # Initializers 
    #################################

    def init_curses(self):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak() #React even when enter key is not pressed
        curses.curs_set(0)
        stdscr.keypad(1)
        curses.start_color()
        curses.use_default_colors()

        #setup colors for the app
        print(curses.can_change_color())
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_CYAN, -1)
        curses.init_pair(3, curses.COLOR_BLUE, -1)
        curses.init_pair(4, curses.COLOR_RED, -1)
        return stdscr

    def quit_curses(self, stdscr):
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def init_app(self, stdscr):
        channelwindow = None
        (y, x, ymax, xmax, ysize, xsize) = self.get_window_dimensions(stdscr)
        if self.channel_fullsize(stdscr):
            chatx = x + 30
            xsize = xmax - chatx
            chatwindow = stdscr.subwin(ysize, xsize, y, chatx)
            channelwindow = stdscr.subwin(ysize, chatx, y, x)
        else:
            chatwindow = stdscr.subwin(ysize, xsize, y, x)
        return (chatwindow, channelwindow)

    #################################
    # Utilities 
    #################################

    def get_window_dimensions(self, window):
        (y, x) = window.getyx()
        (ymax, xmax) = window.getmaxyx()
        ysize = ymax - y 
        xsize = xmax - x
        return (y, x, ymax, xmax, ysize, xsize)

    def channel_fullsize(self, stdscr):
        (y, x, ymax, xmax, ysize, xsize) = self.get_window_dimensions(stdscr)
        if xsize / ysize < 1 or xsize < 40:
            return False
        else:
            return True

    #################################
    # Rendering Methods
    #################################

    
    def draw_border(self, stdscr, chatwindow, channelwindow=None):
        if self.channel_fullsize(stdscr):
            channelwindow.border(0, 0, 0, 0, 0, curses.ACS_TTEE, 0, curses.ACS_BTEE)
            chatwindow.border(0, 0, 0, 0, curses.ACS_TTEE, 0, curses.ACS_BTEE, 0)
        else:
            chatwindow.border(0)
    
    #Still Needs line wrapping
    def render_text(self, chatwindow):
        for message in self.input_buffer:
            chatwindow.move(1, 1)
            chatwindow.deleteln()
            (y, x, ymax, xmax, ysize, xsize) = self.get_window_dimensions(chatwindow)
            chatwindow.move(ymax - 3, x + 1)
            if message[2]:
                chatwindow.addstr(message[0] + ": " + message[1], curses.color_pair(2))
            else: 
                chatwindow.addstr(message[0] + ": " + message[1], curses.color_pair(1))
        self.input_buffer = []

    def render(self, stdscr, chatwindow, channelwindow=None): 
        self.render_text(chatwindow)
        self.draw_border(stdscr, chatwindow, channelwindow)
        stdscr.refresh()

    #################################
    # Text Input Methods
    #################################

    def add_text(self, chatwindow, message, username, is_current_user=False):
        self.input_buffer.append([username, message, is_current_user])

    def add_user_text(self, chatwindow, message):
        add_text(chatwindow, message, self.username, True)

    def add_current_user_text(self, chatwindow, message, username):
        add_text(chatwindow, message, username)
    
    ##################################
    # Initializer
    ##################################
    def __init__(self):
        stdscr = self.init_curses()
        (chatwindow, channelwindow) = self.init_app(stdscr)
        self.add_text(chatwindow, "Hello", "BillyBob", False)
        self.add_text(chatwindow, "Wazzup", "Me", True)
        self.add_text(chatwindow, "Not a Lot", "BillyBob", False)
        self.render(stdscr, chatwindow, channelwindow)
        time.sleep(3)
        self.quit_curses(stdscr)

interface = CursesInterface()
