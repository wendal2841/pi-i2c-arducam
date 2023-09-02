from I2cProvider import I2cProvider
import curses

global spead
spead = 1


def RenderMiddleText(stdscr, key, i2c_provider):
    last_key_pressed = "Last key pressed: {}".format(chr(key))
    focus = "Focus (Left-Right Arrow): {}".format(str(i2c_provider.get(I2cProvider.OPT_FOCUS)))
    zoom = "Zoom (Up-Down Arrow): {}".format(str(i2c_provider.get(I2cProvider.OPT_ZOOM)))
    focus_and_zoom = "Reset Focus and Zoom ('r' Key)"
    motor_x = "MotorX ('w'-'s' Key): {}".format(str(i2c_provider.get(I2cProvider.OPT_MOTOR_X)))
    motor_y = "MotorY ('a'-'d' Key): {}".format(str(i2c_provider.get(I2cProvider.OPT_MOTOR_Y)))
    ircut = "IRCUT ('i' Key): {}".format(str(i2c_provider.get(I2cProvider.OPT_IRCUT)))
    speadInfo = "Spead ('+'-'-' Key): {}".format(spead)

    combined_values = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(
        last_key_pressed,
        focus,
        zoom,
        focus_and_zoom,
        motor_x,
        motor_y,
        ircut,
        speadInfo,
    )

    stdscr.addstr(0, 0, combined_values)


def parseKey(key, i2c_provider):
    global spead
    motor_step = 5 * spead
    focus_step = 100 * spead
    zoom_step = 100 * spead

    if key == ord('+') or key == ord('='): spead = spead + 1
    elif key == ord('-') and spead > 1: spead = spead - 1

    if key == ord('s'):
        i2c_provider.set(I2cProvider.OPT_MOTOR_Y, i2c_provider.get(I2cProvider.OPT_MOTOR_Y) + motor_step)
    elif key == ord('w'):
        i2c_provider.set(I2cProvider.OPT_MOTOR_Y, i2c_provider.get(I2cProvider.OPT_MOTOR_Y) - motor_step)
    elif key == ord('d'):
        i2c_provider.set(I2cProvider.OPT_MOTOR_X, i2c_provider.get(I2cProvider.OPT_MOTOR_X) - motor_step)
    elif key == ord('a'):
        i2c_provider.set(I2cProvider.OPT_MOTOR_X, i2c_provider.get(I2cProvider.OPT_MOTOR_X) + motor_step)

    if key == curses.KEY_UP:
        i2c_provider.set(I2cProvider.OPT_ZOOM, i2c_provider.get(I2cProvider.OPT_ZOOM) + zoom_step)
    elif key == curses.KEY_DOWN:
        i2c_provider.set(I2cProvider.OPT_ZOOM, i2c_provider.get(I2cProvider.OPT_ZOOM) - zoom_step)
    elif key == curses.KEY_RIGHT:
        i2c_provider.set(I2cProvider.OPT_FOCUS, i2c_provider.get(I2cProvider.OPT_FOCUS) + focus_step)
    elif key == curses.KEY_LEFT:
        i2c_provider.set(I2cProvider.OPT_FOCUS, i2c_provider.get(I2cProvider.OPT_FOCUS) - focus_step)

    if key == ord('r'):
        i2c_provider.reset(I2cProvider.OPT_FOCUS)
        i2c_provider.reset(I2cProvider.OPT_ZOOM)
    elif key == ord('i'):
        i2c_provider.set(I2cProvider.OPT_IRCUT, i2c_provider.get(I2cProvider.OPT_IRCUT) ^ 0x0001)


def draw_menu(stdscr, i2c_bus):
    i2c_provider = I2cProvider(i2c_bus)
    key = 0
    stdscr.clear()
    stdscr.refresh()

    while (key != ord('q')):
        stdscr.clear()
        curses.flushinp()
        parseKey(key, i2c_provider)
        RenderMiddleText(stdscr, key, i2c_provider)
        stdscr.refresh()
        key = stdscr.getch()


def main():
    curses.wrapper(draw_menu, 1)


if __name__ == "__main__":
    main()
