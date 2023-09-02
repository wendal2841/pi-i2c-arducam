import argparse
from RpiCamera import Camera

def parse_cmdline():
    parser = argparse.ArgumentParser(description='Arducam Controller.')

    parser.add_argument(
        '-i', '--i2c-bus', type=int, nargs=None, required=True,
        help='Set i2c bus, for A02 is 6, for B01 is 7 or 8, for Jetson Xavier NX it is 9 and 10.'
    )

    return parser.parse_args()

def main():
    args = parse_cmdline()
    camera = Camera()
    camera.start_preview(True)
    print(args.i2c_bus)
    camera.stop_preview()
    camera.close()


if __name__ == "__main__":
    main()