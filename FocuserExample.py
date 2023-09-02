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
    subtitle = ""[:width - 1]
    keystr = "Last key pressed: {}".format(k)[:width - 1]

    focus_value = "Focus (Left-Right Arrow) : {}".format(focuser.get(Focuser.OPT_FOCUS))[:width - 1]
    zoom_value = "Zoom (Up-Down Arrow)      : {}".format(focuser.get(Focuser.OPT_ZOOM))[:width - 1]
    motor_x_val = "MotorX ('w'-'s' Key)     : {}".format(focuser.get(Focuser.OPT_MOTOR_X))[:width - 1]
    motor_y_val = "MotorY ('a'-'d' Key)     : {}".format(focuser.get(Focuser.OPT_MOTOR_Y))[:width - 1]
    ircut_val = "IRCUT    : {}".format(focuser.get(Focuser.OPT_IRCUT))[:width - 1]

    if k == 0:
        keystr = "No key press detected..."[:width - 1]

    start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
    start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
    start_x_device_info = int((width // 2) - (len("Focus    : 00000") // 2) - len("Focus    : 00000") % 2)
    start_y = int((height // 2) - 6)

    stdscr.attron(curses.color_pair(2))
    stdscr.attron(curses.A_BOLD)

    stdscr.attroff(curses.color_pair(2))
    stdscr.attroff(curses.A_BOLD)

    stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
    stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
    stdscr.addstr(start_y + 5, start_x_keystr, keystr)

    stdscr.addstr(start_y + 6, start_x_device_info, focus_value)
    stdscr.addstr(start_y + 7, start_x_device_info, zoom_value)
    stdscr.addstr(start_y + 8, start_x_device_info, motor_x_val)
    stdscr.addstr(start_y + 9, start_x_device_info, motor_y_val)
    stdscr.addstr(start_y + 10, start_x_device_info, ircut_val)


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
        height, width = stdscr.getmaxyx()

        parseKey(k, focuser)

        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        RenderStatusBar(stdscr)
        RenderMiddleText(stdscr, k, focuser)
        stdscr.refresh()

        k = stdscr.getch()


def main():
    curses.wrapper(draw_menu, 1)


if __name__ == "__main__":
    main()
