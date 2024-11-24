import argparse

def port_range(value):
    value = int(value)
    if 49152 <= value <= 65535:
        return value
    raise argparse.ArgumentTypeError(f"Port number must be in the range 49152-65535. Provided: {value}")

parser = argparse.ArgumentParser(description="Service Configuration")
parser.add_argument(
    '-p', '--port',
    required=False,
    default=55443,
    type=port_range,
    help='Which port for the service? Port range - (49152–65535)'
)

args = parser.parse_args()
print(f"Service will run on port: {args.port}")
