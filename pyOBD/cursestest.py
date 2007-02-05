import curses
import time

stdscr = curses.initscr()

curses.noecho()
curses.cbreak()

stdscr.clear()
stdscr.refresh()


time.sleep(5)

curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()
