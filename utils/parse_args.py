import argparse

# Parse args
parser = argparse.ArgumentParser(description='Exercise')
parser.add_argument('--pigpio_addr', type=str, help='Set host of remote gpio', required=False)
parser.add_argument('--mock_gpio', type=bool, nargs='?', const=True, default=False, help='Mock gpio', required=False)

args = parser.parse_args()

MOCK_GPIO = args.mock_gpio if args.mock_gpio != None else False
PIGPIO_ADDR = args.pigpio_addr if args.pigpio_addr != None else None