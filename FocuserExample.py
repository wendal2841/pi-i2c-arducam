from Focuser import Focuser
import curses

global image_count

image_count = 0


def RenderStatusBar(stdscr):
    height, width = stdscr.getmaxyx()
    statusbarstr = "Press 'q' to exit"
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height - 1, 0, statusbarstr)
    stdscr.addstr(height - 1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
    stdscr.attroff(curses.color_pair(3))


def RenderMiddleText(stdscr, k, focuser):
    height, width = stdscr.getmaxyx()

    combined_values = "Last key pressed: {} Focus (Left-Right Arrow): {} Zoom (Up-Down Arrow): {} MotorX ('w'-'s' Key): {} MotorY ('a'-'d' Key): {} IRCUT: {}".format(
        k,
        str(focuser.get(Focuser.OPT_FOCUS))[:width - 1],
        str(focuser.get(Focuser.OPT_ZOOM))[:width - 1],
        str(focuser.get(Focuser.OPT_MOTOR_X))[:width - 1],
        str(focuser.get(Focuser.OPT_MOTOR_Y))[:width - 1],
        str(focuser.get(Focuser.OPT_IRCUT))[:width - 1]
    )

    stdscr.addstr(0, 0, combined_values)


def parseKey(k, focuser):
    global image_count
    motor_step = 5
    focus_step = 100
    zoom_step = 100

    if k == ord('s'):
        focuser.set(Focuser.OPT_MOTOR_Y, focuser.get(Focuser.OPT_MOTOR_Y) + motor_step)
    elif k == ord('w'):
        focuser.set(Focuser.OPT_MOTOR_Y, focuser.get(Focuser.OPT_MOTOR_Y) - motor_step)
    elif k == ord('d'):
        focuser.set(Focuser.OPT_MOTOR_X, focuser.get(Focuser.OPT_MOTOR_X) - motor_step)
    elif k == ord('a'):
        focuser.set(Focuser.OPT_MOTOR_X, focuser.get(Focuser.OPT_MOTOR_X) + motor_step)

    if k == ord('r'):
        focuser.reset(Focuser.OPT_FOCUS)
        focuser.reset(Focuser.OPT_ZOOM)
    elif k == curses.KEY_UP:
        focuser.set(Focuser.OPT_ZOOM, focuser.get(Focuser.OPT_ZOOM) + zoom_step)
    elif k == curses.KEY_DOWN:
        focuser.set(Focuser.OPT_ZOOM, focuser.get(Focuser.OPT_ZOOM) - zoom_step)
    elif k == curses.KEY_RIGHT:
        focuser.set(Focuser.OPT_FOCUS, focuser.get(Focuser.OPT_FOCUS) + focus_step)
    elif k == curses.KEY_LEFT:
        focuser.set(Focuser.OPT_FOCUS, focuser.get(Focuser.OPT_FOCUS) - focus_step)
    elif k == 32:
        focuser.set(Focuser.OPT_IRCUT, focuser.get(Focuser.OPT_IRCUT) ^ 0x0001)


def draw_menu(stdscr, i2c_bus):
    focuser = Focuser(i2c_bus)
    k = 0
    stdscr.clear()
    stdscr.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while (k != ord('q')):
        stdscr.clear()
        curses.flushinp()

        parseKey(k, focuser)

        RenderStatusBar(stdscr)
        RenderMiddleText(stdscr, k, focuser)
        stdscr.refresh()

        k = stdscr.getch()


def main():
    curses.wrapper(draw_menu, 1)


if __name__ == "__main__":
    main()
