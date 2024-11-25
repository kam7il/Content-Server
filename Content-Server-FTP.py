import sys
import argparse

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from ftp_users import ftp_users
from auxiliary_functions import get_ip, get_pwd, is_path_valid

# argument parser
parser = argparse.ArgumentParser(description='Local FTP content server for Windows machines')
parser.add_argument('-ph', '--path',
                    required=False,
                    default="Current",
                    type=str,
                    help='Set path with content or use current working directory')
parser.add_argument('-ip', '--interface',
                    required=False,
                    default="all",
                    type=str,
                    # hostIP issue, it is possible that it will select the ip address of a non-connected network interface
                    choices=['hostIP', 'localhost', 'all'],
                    help='On which network interface should the server be available?')
parser.add_argument('-p', '--port',
                    required=False,
                    default=2121,
                    type=int,
                    choices=[2121, 4545, 5656],
                    help='Which port for the service? Ports to choose: 2121, 4545, 5656')
args = parser.parse_args()

# set arguments
# path
if args.path == 'Current':
    set_path = get_pwd()
elif is_path_valid(args.path):
    set_path = args.path
else:
    print('Invalid path')
    sys.exit(1)

# network interface
match args.interface:
    case 'hostIP':
        host = get_ip()
    case 'localhost':
        host = '127.0.0.1'
    case 'all':
        host = '0.0.0.0'
    case _:
        print('Invalid interface')
        sys.exit(1)

# port
port = args.port

# User and permission configuration
authorizer = DummyAuthorizer()

# Add user: login "user", pass "12345", read/write rights in dir "./ftp"
# authorizer.add_user("user", "12345", "./ftp", perm="elradfmw")

# Add Users from ftp_users
for user, auth in ftp_users.items():
    authorizer.add_user(user, auth['password'], set_path, perm=auth['permissions'])

# Server Settings
handler = FTPHandler
handler.authorizer = authorizer

# Set server FTP on port
server = FTPServer((host, port), handler)

print(f"Server FTP run on {host}, port {port}...")
print(f'Serves path: {set_path}')

server.serve_forever()
