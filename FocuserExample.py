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

    last_key_pressed = "Last key pressed: {}\n".format(k);
    focus = "Focus (Left-Right Arrow): {}\n".format(str(focuser.get(Focuser.OPT_FOCUS))[:width - 1]);
    zoom = "Zoom (Up-Down Arrow): {}\n".format(str(focuser.get(Focuser.OPT_ZOOM))[:width - 1]);
    motor_x = "MotorX ('w'-'s' Key): {}\n".format(str(focuser.get(Focuser.OPT_MOTOR_X))[:width - 1]);
    motor_y = "MotorY ('a'-'d' Key): {}\n".format(str(focuser.get(Focuser.OPT_MOTOR_Y))[:width - 1]);
    ircut = "IRCUT: {}\n".format(str(focuser.get(Focuser.OPT_IRCUT))[:width - 1]);

    combined_values = "{}{}{}{}{}{}".format(
        last_key_pressed,
        focus,
        zoom,
        motor_x,
        motor_y,
        ircut,
    );

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
