from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from ftp_users import ftp_users

# User and permission configuration
authorizer = DummyAuthorizer()

# Add user: login "user", pass "12345", read/write rights in dir "./ftp"
# authorizer.add_user("user", "12345", "./ftp", perm="elradfmw")

# Add User with only read rights
# authorizer.add_user(ftp_users, "12345", r".\ftp", perm="elr")
authorizer.add_user('viewer', ftp_users['viewer']['password'], r".\\", perm="elr")


# Server Settings
handler = FTPHandler
handler.authorizer = authorizer

# Set server FTP on port 2121
server = FTPServer(("0.0.0.0", 2121), handler)

print("Server FTP run on port 2121...")
server.serve_forever()
