from Focuser import Focuser
import curses

def RenderMiddleText(stdscr, k, focuser):
    last_key_pressed = "Last key pressed: {}".format(k);
    focus = "Focus (Left-Right Arrow): {}".format(str(focuser.get(Focuser.OPT_FOCUS)));
    zoom = "Zoom (Up-Down Arrow): {}".format(str(focuser.get(Focuser.OPT_ZOOM)));
    focus_and_zoom = "Reset Focus and Zoom ('r' Key)";
    motor_x = "MotorX ('w'-'s' Key): {}".format(str(focuser.get(Focuser.OPT_MOTOR_X)));
    motor_y = "MotorY ('a'-'d' Key): {}".format(str(focuser.get(Focuser.OPT_MOTOR_Y)));
    ircut = "IRCUT: {}".format(str(focuser.get(Focuser.OPT_IRCUT)));

    combined_values = "{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        last_key_pressed,
        focus,
        zoom,
        focus_and_zoom,
        motor_x,
        motor_y,
        ircut,
    );

    stdscr.addstr(0, 0, combined_values)


def parseKey(k, focuser):
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
        RenderMiddleText(stdscr, k, focuser)
        stdscr.refresh()
        k = stdscr.getch()


def main():
    curses.wrapper(draw_menu, 1)


if __name__ == "__main__":
    main()
